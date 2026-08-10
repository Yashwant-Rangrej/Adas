class SteeringController:
    def __init__(self, hardware):
        self.hw = hardware
        self.servo_id = 1 # Assuming the front steering servo is plugged into ID 1
        
        # Center the servo initially (1500 is center)
        self.hw.set_servo(self.servo_id, 1500, duration=0.5)

    def steer(self, cx):
        # Returns the current direction so the drive motors can match it
        if cx is None:
            return "STOP"
            
        # Deadzone between 130 and 190
        if cx > 190:
            # Turn Right -> Adjust the 1200 depending on which way your servo mounts!
            self.hw.set_servo(self.servo_id, 1200)
            return "RIGHT"
        elif cx < 130:
            # Turn Left -> Adjust the 1800 depending on which way your servo mounts!
            self.hw.set_servo(self.servo_id, 1800)
            return "LEFT"
        else:
            # Go Straight
            self.hw.set_servo(self.servo_id, 1500)
            return "STRAIGHT"
