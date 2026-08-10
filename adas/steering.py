import numpy as np

class SteeringController:
    def __init__(self, hardware):
        self.hw = hardware
        self.servo_id = 1 # Assuming the front steering servo is plugged into ID 1
        
        # Center the servo initially (1500 is center)
        self.hw.set_servo(self.servo_id, 1500, duration=0.5)

    def steer(self, cx):
        if cx is None:
            return "STOP"
            
        center = 160
        error = cx - center
        abs_error = abs(error)
        
        # Deadzone for straight
        if abs_error < 15:
            self.hw.set_servo(self.servo_id, 1500)
            return "STRAIGHT"
            
        # Map pixel error (15 to 160) to degrees (5 to 45)
        angle = np.interp(abs_error, [15, 160], [5, 45])
        
        # Convert angle to PWM offset (Assuming 45 degrees = 500 PWM)
        pwm_offset = int(angle * (500.0 / 45.0))
        
        if error > 0:
            # Turn Right -> Adjust 1500 - offset depending on servo mount
            self.hw.set_servo(self.servo_id, 1500 - pwm_offset)
            
            if angle <= 15:
                return f"GENTLE RIGHT ({int(angle)}deg)"
            elif angle <= 30:
                return f"STD RIGHT ({int(angle)}deg)"
            else:
                return f"SHARP RIGHT ({int(angle)}deg)"
        else:
            # Turn Left -> Adjust 1500 + offset depending on servo mount
            self.hw.set_servo(self.servo_id, 1500 + pwm_offset)
            
            if angle <= 15:
                return f"GENTLE LEFT ({int(angle)}deg)"
            elif angle <= 30:
                return f"STD LEFT ({int(angle)}deg)"
            else:
                return f"SHARP LEFT ({int(angle)}deg)"
