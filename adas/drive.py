class DriveController:
    def __init__(self, hardware):
        self.hw = hardware
        # Linear speed in m/s (0.15 is a safe default for MentorPi)
        self.speed = 0.15 
        # Angular turning speed
        self.turn_speed = 0.5 

    def move(self, direction):
        if direction == "STOP":
            # Stop the robot if lost line
            self.stop()
            print("Lost line - STOPPING")
        else:
            # Drive forward - front servo is dynamically handling the angle
            self.hw.set_velocity(self.speed, 0.0)
            # print(f"Driving: {direction}") # Optional logging
            
    def stop(self):
        # Send zero velocity to stop
        self.hw.set_velocity(0.0, 0.0)
