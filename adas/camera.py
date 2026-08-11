import cv2
import numpy as np

class Camera:
    def __init__(self, camera_index=0, width=320, height=240):
        self.use_mock = False
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            print(f"Warning: Could not open camera at index {camera_index}. Using mock camera instead.")
            self.use_mock = True
        else:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            
        self.width = width
        self.height = height

    def get_frame(self):
        if self.use_mock:
            # Generate a blank image to avoid crashing the rest of the pipeline
            img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            cv2.putText(img, "MOCK CAMERA", (50, self.height//2), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            return img
            
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def release(self):
        if not self.use_mock:
            self.cap.release()
