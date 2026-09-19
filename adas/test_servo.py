import rclpy
from rclpy.node import Node
import time

try:
    from ros_robot_controller_msgs.msg import SetPWMServoState, PWMServoState
except ImportError:
    print("Error: ros_robot_controller_msgs not found. Cannot test servo.")
    exit(1)

class ServoTester(Node):
    def __init__(self):
        super().__init__('servo_tester')
        self.pwm_pub = self.create_publisher(SetPWMServoState, 'ros_robot_controller/pwm_servo/set_state', 10)

    def set_servo(self, servo_id, position, duration=0.5):
        msg = SetPWMServoState()
        msg.duration = float(duration)
        pos = PWMServoState()
        pos.id = [int(servo_id)]
        pos.position = [int(position)]
        msg.state = [pos]
        self.pwm_pub.publish(msg)

def test_servo(servo_id=3):
    rclpy.init()
    tester = ServoTester()
    
    # Wait for publisher to establish connection
    time.sleep(1)
    
    print(f"Testing servo ID {servo_id} via MentorPi Expansion Board...")
    try:
        # Test positions
        print("Moving to center (1500)")
        tester.set_servo(servo_id, 1500)
        time.sleep(1.5)
        
        print("Turning Right (1100us)...")
        tester.set_servo(servo_id, 1100)
        time.sleep(1.5)
        
        print("Turning Left (1900us)...")
        tester.set_servo(servo_id, 1900)
        time.sleep(1.5)
        
        print("Moving back to center (1500)")
        tester.set_servo(servo_id, 1500)
        time.sleep(1.5)
        
        print("Test completed successfully!")
        
    except KeyboardInterrupt:
        pass
    finally:
        tester.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    test_servo()
