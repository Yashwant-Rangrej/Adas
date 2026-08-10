import cv2
import numpy as np

class LineDetector:
    def __init__(self):
        # Define the range for red color in HSV
        self.lower_red1 = np.array([0, 70, 50])
        self.upper_red1 = np.array([10, 255, 255])
        self.lower_red2 = np.array([170, 70, 50])
        self.upper_red2 = np.array([180, 255, 255])
        
        self.kernel = np.ones((5, 5), np.uint8)
        
        # Track the last known position of our primary line
        self.last_cx = None
        self.last_cy = None

    def process_frame(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        mask1 = cv2.inRange(hsv, self.lower_red1, self.upper_red1)
        mask2 = cv2.inRange(hsv, self.lower_red2, self.upper_red2)
        mask = mask1 + mask2
        
        mask = cv2.erode(mask, self.kernel, iterations=1)
        mask = cv2.dilate(mask, self.kernel, iterations=2)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        cx, cy = None, None
        
        if len(contours) > 0:
            best_contour = None
            
            # If we haven't locked onto a line yet, just find the biggest red object
            if self.last_cx is None:
                best_contour = max(contours, key=cv2.contourArea)
            else:
                # We already have a target line. 
                # Find the contour closest to where it was last seen to ignore other lines.
                min_dist = float('inf')
                
                for c in contours:
                    # Ignore tiny red specs (noise) to prevent jumping
                    if cv2.contourArea(c) < 200:
                        continue
                        
                    M = cv2.moments(c)
                    if M["m00"] != 0:
                        curr_x = int(M["m10"] / M["m00"])
                        curr_y = int(M["m01"] / M["m00"])
                        
                        # Calculate distance from last known center
                        dist = ((curr_x - self.last_cx)**2 + (curr_y - self.last_cy)**2)**0.5
                        
                        if dist < min_dist:
                            min_dist = dist
                            best_contour = c
                            
                # If all other contours were too small, fallback to the largest
                if best_contour is None:
                    best_contour = max(contours, key=cv2.contourArea)

            # Calculate the final center of our chosen tracking line
            M = cv2.moments(best_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                # Remember this position for the next frame so we don't jump to other lines
                self.last_cx = cx
                self.last_cy = cy
                
                # Draw the tracked line in green so we know it's locked on
                cv2.drawContours(frame, [best_contour], -1, (0, 255, 0), 2)
                cv2.circle(frame, (cx, cy), 5, (255, 255, 255), -1)
        else:
            # No red seen at all, reset tracking so it can find a new line
            self.last_cx = None
            self.last_cy = None
                
        return frame, mask, cx
