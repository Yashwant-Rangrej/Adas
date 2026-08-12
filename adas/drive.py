class DriveController:
    def __init__(self, hardware):
        self.hw = hardware
        # Linear speed in m/s (increased for metal geared motors)
        self.speed = 0.35 
        # Angular turning speed
        self.turn_speed = 0.8 

    def move(self, direction):
        if direction == "STOP":
            # Stop the robot if lost line
            self.stop()
            print("Lost line - STOPPING")
        else:
            # Drive forward - calculate angular velocity based on direction string
            angular_z = 0.0
            
            # Extract turn speed based on severity
            current_turn_speed = self.turn_speed
            if "GENTLE" in direction:
                current_turn_speed = self.turn_speed * 0.5
            elif "SHARP" in direction:
                current_turn_speed = self.turn_speed * 1.5
                
            if "LEFT" in direction:
                angular_z = current_turn_speed
            elif "RIGHT" in direction:
                angular_z = -current_turn_speed

            # Front servo handles angle, rear wheels use differential speed
            self.hw.set_velocity(self.speed, angular_z)
            # print(f"Driving: {direction}") # Optional logging
            
    def stop(self):
        # Send zero velocity to stop
        self.hw.set_velocity(0.0, 0.0)
