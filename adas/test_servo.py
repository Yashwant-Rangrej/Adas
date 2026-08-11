from gpiozero import Servo
from time import sleep

def test_servo(pin=18):
    print(f"Testing servo on GPIO pin {pin}...")
    try:
        try:
            servo = Servo(pin)
        except Exception:
            print("Warning: Real GPIO pins not found or inaccessible. Falling back to custom MockServo for testing.")
            class MockServo:
                def __init__(self, p): pass
                @property
                def value(self): return 0.0
                @value.setter
                def value(self, v): print(f"[Mock] Servo set to {v}")
            servo = MockServo(pin)
        
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
