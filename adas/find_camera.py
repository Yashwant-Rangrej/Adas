import cv2

def test_cameras():
    print("Searching for available cameras...")
    available = []
    
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"Found working camera at index {i} (Resolution: {frame.shape[1]}x{frame.shape[0]})")
                available.append(i)
            cap.release()
            
    if not available:
        print("No cameras found!")
        return
        
    print("\nPress 'SPACE' to cycle to the next camera.")
    print("Press 'q' or 'ESC' to quit.")
    
    current_idx = 0
    cap = cv2.VideoCapture(available[current_idx])
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        cv2.putText(frame, f"Camera Index: {available[current_idx]}", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Camera Finder", frame)
        
        key = cv2.waitKey(30) & 0xFF
        if key == ord('q') or key == 27: # ESC
            break
        elif key == ord(' '): # SPACE
            cap.release()
            current_idx = (current_idx + 1) % len(available)
            cap = cv2.VideoCapture(available[current_idx])
            print(f"Switched to camera index {available[current_idx]}")
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_cameras()
