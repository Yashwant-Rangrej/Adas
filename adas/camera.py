import cv2
import numpy as np
from sensor_msgs.msg import Image
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

class Camera:
    def __init__(self, use_sdk=False, node=None, topic_name=None, camera_index=0, width=320, height=240):
        self.use_sdk = use_sdk
        self.width = width
        self.height = height
        self.latest_frame = None
        self.use_mock = False
        self.subs = []

        if self.use_sdk:
            if node is None:
                raise ValueError("A ROS 2 node must be provided when use_sdk=True")
            self.node = node
            
            qos_profile = QoSProfile(
                reliability=QoSReliabilityPolicy.BEST_EFFORT,
                history=QoSHistoryPolicy.KEEP_LAST,
                depth=1
            )
            
            # Subscribe to all possible Angstrong/Orbbec topic namespaces just to be safe
            possible_topics = [
                '/ascamera_hp60c/camera_color/image_raw',
                '/ascamera_hp60c/rgb/image_raw',
                '/ascamera/camera_color/image_raw',
                '/ascamera/rgb/image_raw',
                '/camera/color/image_raw'
            ]
            
            for t in possible_topics:
                self.subs.append(self.node.create_subscription(Image, t, self.image_callback, qos_profile))
                
            print(f"Camera configured for SDK mode (Listening to {len(possible_topics)} possible topics)")
        else:
            self.cap = cv2.VideoCapture(camera_index)
            if not self.cap.isOpened():
                print(f"Warning: Could not open camera at index {camera_index}. Using mock camera instead.")
                self.use_mock = True
            print(f"Camera configured for direct OpenCV mode (Index: {camera_index})")

    def image_callback(self, msg):
        try:
            if msg.encoding in ['bgr8', 'rgb8']:
                frame = np.ndarray(shape=(msg.height, msg.width, 3), dtype=np.uint8, buffer=msg.data)
                if msg.encoding == 'rgb8':
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                self.latest_frame = cv2.resize(frame, (self.width, self.height))
            elif msg.encoding == 'mono8':
                frame = np.ndarray(shape=(msg.height, msg.width), dtype=np.uint8, buffer=msg.data)
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
                self.latest_frame = cv2.resize(frame, (self.width, self.height))
        except Exception as e:
            print(f"Error decoding SDK image: {e}")

    def get_frame(self):
        if self.use_sdk:
            if self.latest_frame is None:
                img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
                cv2.putText(img, "WAITING FOR SDK...", (30, self.height//2), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                return img
            return self.latest_frame.copy()
        else:
            if self.use_mock:
                img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
                cv2.putText(img, "MOCK CAMERA", (50, self.height//2), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                return img
                
            ret, frame = self.cap.read()
            if not ret:
                return None
            return cv2.resize(frame, (self.width, self.height))

    def release(self):
        if not self.use_sdk and not self.use_mock:
            self.cap.release()
