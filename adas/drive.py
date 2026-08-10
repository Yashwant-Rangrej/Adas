class DriveController:
    def __init__(self, hardware):
        self.hw = hardware
        # Linear speed in m/s (0.15 is a safe default for MentorPi)
        self.speed = 0.15 
        # Angular turning speed
        self.turn_speed = 0.5 

    def move(self, direction):
        if direction == "RIGHT":
            # Drive forward and steer right
            self.hw.set_velocity(self.speed, -self.turn_speed)
            print("Driving RIGHT")
        elif direction == "LEFT":
            # Drive forward and steer left
            self.hw.set_velocity(self.speed, self.turn_speed)
            print("Driving LEFT")
        elif direction == "STRAIGHT":
            # Drive straight ahead
            self.hw.set_velocity(self.speed, 0.0)
            print("Driving STRAIGHT")
        else:
            # Stop the robot if lost line
            self.stop()
            print("Lost line - STOPPING")
            
    def stop(self):
        # Send zero velocity to stop
        self.hw.set_velocity(0.0, 0.0)
