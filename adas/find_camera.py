import cv2

def test_formats():
    print("Testing different video formats on Camera Index 0...")
    
    # Common formats for 3D/RGB cameras
    formats = [
        ('DEFAULT', 0),
        ('YUYV', cv2.VideoWriter_fourcc(*'YUYV')),
        ('YUY2', cv2.VideoWriter_fourcc(*'YUY2')),
        ('MJPG', cv2.VideoWriter_fourcc(*'MJPG')),
        ('NV12', cv2.VideoWriter_fourcc(*'NV12')),
        ('RGB3', cv2.VideoWriter_fourcc(*'RGB3'))
    ]
    
    print("\nPress 'SPACE' to try the next format.")
    print("Press 'q' or 'ESC' to quit.")
    
    current_idx = 0
    
    def open_camera(fmt_name, fmt_code):
        cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        if fmt_code != 0:
            cap.set(cv2.CAP_PROP_FOURCC, fmt_code)
        # Try setting a standard high-res in case the low-res is depth-only
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        return cap

    fmt_name, fmt_code = formats[current_idx]
    cap = open_camera(fmt_name, fmt_code)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            # Create a blank frame if it fails to read this format
            import numpy as np
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, f"Format {fmt_name} FAILED", (50, 240), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            cv2.putText(frame, f"Format: {fmt_name}", (20, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
        cv2.imshow("Camera Format Tester", frame)
        
        key = cv2.waitKey(30) & 0xFF
        if key == ord('q') or key == 27: # ESC
            break
        elif key == ord(' '): # SPACE
            cap.release()
            current_idx = (current_idx + 1) % len(formats)
            fmt_name, fmt_code = formats[current_idx]
            print(f"Trying format: {fmt_name}...")
            cap = open_camera(fmt_name, fmt_code)
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_formats()
