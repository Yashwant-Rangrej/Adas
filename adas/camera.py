import cv2

class Camera:
    def __init__(self, camera_index=0, width=320, height=240):
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise Exception("Error: Could not open the camera.")
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def release(self):
        self.cap.release()
