import cv2
import rclpy
import time
import os
import sys
from camera import Camera
from vision import LineDetector
from hardware import MentorPiHardware
from steering import SteeringController
from drive import DriveController
from signs import SignDetector

def main():
    print("Initializing components...")
    
    # Initialize the ROS 2 node required for MentorPi hardware
    rclpy.init()
    hardware = MentorPiHardware()
    
    camera_idx = 0
    if len(sys.argv) > 1:
        try:
            camera_idx = int(sys.argv[1])
        except ValueError:
            pass
            
    print(f"Using camera index: {camera_idx}")
    
    try:
        cam = Camera(camera_index=camera_idx)
    except Exception as e:
        print("Camera Error:", e)
        hardware.destroy_node()
        rclpy.shutdown()
        return
        
    detector = LineDetector()
    steering = SteeringController(hardware)
    drive = DriveController(hardware)
    sign_detector = SignDetector()
    
    print("System running! Press 'q' to quit (if display is active).")
    
    # Check if a monitor is attached so we don't crash when running on boot
    has_display = bool(os.environ.get('DISPLAY'))
    
    # State machine variables
    current_state = "FOLLOW_LINE"
    state_start_time = 0
    
    try:
        while True:
            # Spin the ROS node so it can process messages
            rclpy.spin_once(hardware, timeout_sec=0.01)
            
            frame = cam.get_frame()
            if frame is None:
                print("Error: Can't receive frame.")
                break
                
            # Process the frame for the red line regardless of state (for visualization)
            processed_frame, mask, cx = detector.process_frame(frame)
                
            # --- 1. Sign Detection ---
            # Only scan for new signs if we are currently following the line
            if current_state == "FOLLOW_LINE":
                detected_sign = sign_detector.detect(frame)
                
                if detected_sign is not None:
                    print(f"\n!!! DETECTED SIGN: {detected_sign} !!!")
                    
                    if detected_sign == "STOP":
                        current_state = "STOP_SIGN"
                        state_start_time = time.time()
                    elif detected_sign == "DEADEND":
                        current_state = "DEAD_END_STOP"
                        state_start_time = time.time()
                    elif detected_sign == "LEFT":
                        current_state = "FORCE_LEFT"
                        state_start_time = time.time()
                    elif detected_sign == "RIGHT":
                        current_state = "FORCE_RIGHT"
                        state_start_time = time.time()
                    elif detected_sign == "SLOW":
                        drive.speed = 0.08  # Slow down
                    elif detected_sign == "SPEED_LIMIT":
                        drive.speed = 0.20  # Speed up

            # --- 2. State Machine Handling ---
            if current_state == "STOP_SIGN":
                drive.stop()
                cv2.putText(processed_frame, "ACTION: STOPPING (3s)", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
                # Stop for 3 seconds, then resume
                if time.time() - state_start_time > 3.0:
                    current_state = "FOLLOW_LINE"
                    
            elif current_state == "DEAD_END_STOP":
                drive.stop()
                cv2.putText(processed_frame, "ACTION: DEAD END - STOPPED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
                # The robot will stay stopped until restarted
                    
            elif current_state == "FORCE_LEFT":
                steering.hw.set_servo(steering.servo_id, 1800) # Hard Left
                drive.hw.set_velocity(0.15, 0.0) # Back wheels drive forward
                cv2.putText(processed_frame, "ACTION: FORCE LEFT", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
                if time.time() - state_start_time > 1.5:
                    current_state = "FOLLOW_LINE"
                    
            elif current_state == "FORCE_RIGHT":
                steering.hw.set_servo(steering.servo_id, 1200) # Hard Right
                drive.hw.set_velocity(0.15, 0.0) # Back wheels drive forward
                cv2.putText(processed_frame, "ACTION: FORCE RIGHT", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
                if time.time() - state_start_time > 1.5:
                    current_state = "FOLLOW_LINE"
                    
            elif current_state == "FOLLOW_LINE":
                if hardware.obstacle_detected:
                    cv2.putText(processed_frame, "OBSTACLE DETECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
                    drive.stop()
                else:
                    direction = steering.steer(cx)
                    drive.move(direction)
                    cv2.putText(processed_frame, f"LINE TRACKING: {direction}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                    
            # Display results if a screen is attached
            if has_display:
                cv2.imshow('Camera Feed', processed_frame)
                cv2.imshow('Red Mask', mask)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
    finally:
        drive.stop()
        cam.release()
        cv2.destroyAllWindows()
        hardware.destroy_node()
        rclpy.shutdown()
        print("System shutdown complete.")

if __name__ == '__main__':
    main()
