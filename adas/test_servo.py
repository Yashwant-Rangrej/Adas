from gpiozero import Servo
from time import sleep

def test_servo(pin=18):
    print(f"Testing servo on GPIO pin {pin}...")
    try:
        # Initialize servo
        servo = Servo(pin)
        
        # Test positions
        print("Moving to center (0.0)")
        servo.value = 0.0
        sleep(1)
        
        print("Moving to min (-1.0)")
        servo.value = -1.0
        sleep(1)
        
        print("Moving to max (1.0)")
        servo.value = 1.0
        sleep(1)
        
        print("Moving back to center (0.0)")
        servo.value = 0.0
        sleep(1)
        
        # Disable servo
        servo.value = None
        print("Test completed successfully!")
        
    except Exception as e:
        print(f"Error testing servo: {e}")

if __name__ == "__main__":
    test_servo()
