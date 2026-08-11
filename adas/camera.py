import cv2
import numpy as np
from sensor_msgs.msg import Image
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

class Camera:
    def __init__(self, node, topic_name='/ascamera/camera_color/image_raw', width=320, height=240):
        self.node = node
        self.width = width
        self.height = height
        self.latest_frame = None
        
        # Best effort QoS is usually best for high bandwidth video streams
        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1
        )
        
        self.sub = self.node.create_subscription(
            Image,
            topic_name,
            self.image_callback,
            qos_profile
        )
        print(f"Subscribed to camera SDK topic: {topic_name}")

    def image_callback(self, msg):
        try:
            # Convert ROS Image message to numpy array (OpenCV format)
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
            print(f"Error decoding image: {e}")

    def get_frame(self):
        if self.latest_frame is None:
            # Generate a blank loading image while waiting for the SDK to publish
            img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            cv2.putText(img, "WAITING FOR SDK...", (30, self.height//2), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            return img
            
        return self.latest_frame.copy()

    def release(self):
        # The node handles subscription cleanup
        pass
