import cv2
import os

class SignDetector:
    def __init__(self, sign_dir="assets"):
        # Initialize ORB detector. 500 features is a good balance of speed and accuracy for Pi
        self.orb = cv2.ORB_create(nfeatures=500)
        
        # Load reference images
        self.reference_signs = {}
        sign_files = {
            "STOP": "Stop.png",
            "LEFT": "Left.png",
            "RIGHT": "Right.png",
            "DEADEND": "deadend.png",
            "SLOW": "slow.png",
            "SPEED_LIMIT": "speed_limit.png"
        }
        
        print("--- Loading Road Signs ---")
        for sign_name, filename in sign_files.items():
            path = os.path.join(sign_dir, filename)
            if os.path.exists(path):
                # Read the sign image in grayscale
                img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    # Resize to a standard size so features are consistent
                    img = cv2.resize(img, (200, 200))
                    # Compute keypoints and descriptors
                    kp, des = self.orb.detectAndCompute(img, None)
                    if des is not None:
                        self.reference_signs[sign_name] = (kp, des)
                        print(f"[*] Loaded {sign_name} successfully")
            else:
                print(f"[!] Warning: {filename} not found.")
        print("--------------------------")
                
        # Brute Force Matcher with Hamming distance for ORB
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
        
        # Cooldown prevents spamming detections of the same sign over and over
        self.cooldown = 0
        
    def detect(self, frame):
        if self.cooldown > 0:
            self.cooldown -= 1
            return None
            
        # Convert camera frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # OPTIONAL: Crop the top half of the frame where signs usually are
        # This doubles processing speed and ignores the red line/floor!
        h, w = gray.shape
        top_half = gray[0:int(h/2), :]
        
        kp_frame, des_frame = self.orb.detectAndCompute(top_half, None)
        
        if des_frame is None or len(kp_frame) < 10:
            return None
            
        best_match = None
        max_good_matches = 0
        
        # Compare frame with all loaded signs
        for sign_name, (kp_ref, des_ref) in self.reference_signs.items():
            # knnMatch gets the top 2 matches for each descriptor
            matches = self.bf.knnMatch(des_ref, des_frame, k=2)
            
            # Apply Lowe's ratio test to filter out bad matches
            good_matches = []
            for m_n in matches:
                if len(m_n) == 2:
                    m, n = m_n
                    if m.distance < 0.75 * n.distance:
                        good_matches.append(m)
            
            if len(good_matches) > max_good_matches:
                max_good_matches = len(good_matches)
                best_match = sign_name
                
        # If we have a solid number of matching features (heuristic threshold)
        if max_good_matches > 15:
            # Set a cooldown of roughly 30 frames (about 1 second)
            self.cooldown = 30
            return best_match
            
        return None
