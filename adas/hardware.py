import rclpy
import os
os.environ['GPIOZERO_PIN_FACTORY'] = 'pigpio'
import math
import numpy as np
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from rclpy.qos import QoSProfile, QoSReliabilityPolicy
try:
    from ros_robot_controller_msgs.msg import SetPWMServoState, PWMServoState
    YAHBOOM_MSGS_AVAILABLE = True
except ImportError:
    print("WARNING: ros_robot_controller_msgs not found. Servo commands via ROS will be ignored.")
    YAHBOOM_MSGS_AVAILABLE = False

from gpiozero import Servo

class MockServo:
    def __init__(self, p): pass
    @property
    def value(self): return 0.0
    @value.setter
    def value(self, v): pass

class MentorPiHardware(Node):
    def __init__(self):
        super().__init__('custom_line_follower_hardware')
        
        # Publishers
        if YAHBOOM_MSGS_AVAILABLE:
            self.pwm_pub = self.create_publisher(SetPWMServoState, 'ros_robot_controller/pwm_servo/set_state', 10)
        else:
            self.pwm_pub = None
            
        self.cmd_vel_pub = self.create_publisher(Twist, '/controller/cmd_vel', 1)
        
        # Hardware GPIO Servo (Directly plugged into Raspberry Pi)
        try:
            from gpiozero import Servo
            self.gpio_servo = Servo(18)
        except Exception as e:
            print(f"Failed to initialize real GPIO Servo: {e}. Falling back to custom mock Servo.")
            self.gpio_servo = MockServo(18)
        
        # Lidar Subscriber for Obstacle Detection
        qos = QoSProfile(depth=1, reliability=QoSReliabilityPolicy.BEST_EFFORT)
        self.lidar_sub = self.create_subscription(LaserScan, '/scan_raw', self.lidar_callback, qos)
        
        # Obstacle State
        self.obstacle_detected = False
        self.stop_threshold = 0.4 # Stop if obstacle is within 40cm (0.4 meters)
        
    def lidar_callback(self, msg):
        """
        Processes lidar data to detect obstacles directly in front of the robot.
        """
        ranges = np.array(msg.ranges)
        # Replace inf and nan values
        ranges = np.nan_to_num(ranges, posinf=10.0, neginf=10.0)
        
        # We want to check a 60-degree cone in front of the robot.
        # For MentorPi, index 0 is typically straight ahead.
        angle_30_idx = int(math.radians(30) / msg.angle_increment)
        
        # Get the front-left and front-right slices
        front_left = ranges[0:angle_30_idx]
        front_right = ranges[-angle_30_idx:]
        
        front_ranges = np.concatenate((front_left, front_right))
        
        # Filter out 0.0 values (which usually mean invalid/too close to read)
        valid_ranges = front_ranges[front_ranges > 0.1]
        
        if len(valid_ranges) > 0:
            min_dist = valid_ranges.min()
            if min_dist < self.stop_threshold:
                self.obstacle_detected = True
            else:
                self.obstacle_detected = False

    def set_servo(self, servo_id, position, duration=0.2):
        # Hardware GPIO Control
        if servo_id == 1 and self.gpio_servo:
            # Map Yahboom PWM (1200 to 1800) to gpiozero (-1.0 to 1.0)
            val = (position - 1500) / 500.0
            val = max(min(val, 1.0), -1.0) # Clamp between -1.0 and 1.0
            self.gpio_servo.value = val
            
        # Optional: Send to Yahboom ROS Driver (if installed)
        if not YAHBOOM_MSGS_AVAILABLE:
            return
            
        msg = SetPWMServoState()
        msg.duration = float(duration)
        pos = PWMServoState()
        pos.id = [int(servo_id)]
        pos.position = [int(position)]
        msg.state = [pos]
        self.pwm_pub.publish(msg)
        
    def set_velocity(self, linear_x, angular_z):
        twist = Twist()
        twist.linear.x = float(linear_x)
        twist.angular.z = float(angular_z)
        self.cmd_vel_pub.publish(twist)
