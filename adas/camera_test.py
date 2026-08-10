import cv2
import numpy as np


def access_camera():
    # '0' is the default camera index. Change to 1 or -1 if 0 doesn't work.
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open the camera.")
        return

    # Optional: Set a lower resolution to make processing faster (great for Raspberry Pi)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    print("Camera is running! Press the 'q' key on your keyboard to quit.")

    try:
        while True:
            # Capture the video frame by frame
            ret, frame = cap.read()
            
            # If the frame was not read correctly, break the loop
            if not ret:
                print("Error: Can't receive frame.")
                break

            # --- RED LINE DETECTION ---
            # 1. Convert the frame to HSV color space
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # 2. Define the range for red color in HSV
            # Red color wraps around the hue circle in OpenCV (0-10 and 170-180)
            lower_red1 = np.array([0, 70, 50])
            upper_red1 = np.array([10, 255, 255])
            lower_red2 = np.array([170, 70, 50])
            upper_red2 = np.array([180, 255, 255])
            
            # 3. Create a mask that only keeps the red pixels
            mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
            mask = mask1 + mask2
            
            # 4. Optional: Clean up the mask with some morphological operations (removes noise)
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.erode(mask, kernel, iterations=1)
            mask = cv2.dilate(mask, kernel, iterations=2)
            
            # 5. Find contours (outlines) of the red areas
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # 6. If a red line is found, find its center
            if len(contours) > 0:
                # Find the largest contour (assuming the line is the biggest red object)
                c = max(contours, key=cv2.contourArea)
                
                # Calculate the center of the contour using image moments
                M = cv2.moments(c)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    
                    # Draw the contour and center point on the original frame
                    cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)  # Draw green outline
                    cv2.circle(frame, (cx, cy), 5, (255, 255, 255), -1) # Draw white dot at center
                    
                    # (Steering is handled by ROS 2 in the main ADAS program, not here)
            
            # Display the original video stream and the black/white mask
            cv2.imshow('Camera Feed', frame)
            cv2.imshow('Red Mask', mask)

            # Wait 1 millisecond for the 'q' key to be pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    finally:
        # Release the camera and close the window when done
        cap.release()
        cv2.destroyAllWindows()
        print("Camera closed.")

if __name__ == '__main__':
    access_camera()
