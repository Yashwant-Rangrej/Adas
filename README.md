# 🚗 MentorPi ADAS (Advanced Driver Assistance System)

Welcome to the MentorPi ADAS project! This repository contains Python-based software to run an autonomous driving system on a Raspberry Pi (MentorPi hardware). The system utilizes OpenCV for vision processing and ROS 2 for hardware control.

## ✨ Features
- **Proportional Lane Tracking:** Uses a camera to detect lines and calculate precise dynamic steering angles (Gentle, Standard, Sharp) ranging from 5 to 45 degrees.
- **Traffic Sign Recognition:** Uses ORB feature matching to detect traffic signs like STOP, LEFT, RIGHT, DEADEND, SLOW, and SPEED_LIMIT.
- **Hardware Integration:** Communicates with MentorPi hardware via ROS 2 to control servos (Ackermann steering) and DC motors (drive).
- **Obstacle Detection:** Stops automatically when an obstacle is detected by the hardware sensors.

## 📁 Project Structure
- `main.py` - The core script that runs the state machine and integrates all components.
- `camera.py` - Handles capturing video frames from the USB/Pi camera.
- `vision.py` - Processes images to find the track/line and calculates the center.
- `signs.py` - Detects traffic signs using computer vision (ORB).
- `steering.py` - Calculates proportional steering commands based on line detection error.
- `drive.py` - Controls vehicle speed, seamlessly handling forward motion during turns.
- `hardware.py` - ROS 2 node that communicates directly with the MentorPi hardware (motors/servos).
- `test_servo.py` - Standalone hardware test script for the steering servo.
- `setup.sh` / `run.sh` - Helper scripts for easy setup and execution.
- `assets/` - Reference images for traffic sign detection.

---

## 🚀 Getting Started

Follow these steps to set up your Raspberry Pi/Robot and run the ADAS system.

### Phase 1: Install Dependencies & ROS 2 Tools
**Directory:** Open a brand new terminal. It does not matter which directory you are in.
Run this to install the required system libraries, vision packages, and the `colcon` build tool:
```bash
sudo apt update
sudo apt install -y python3-colcon-common-extensions libgflags-dev nlohmann-json3-dev libgoogle-glog-dev ros-humble-image-transport ros-humble-image-publisher ros-humble-pcl-conversions ros-humble-pcl-ros ros-humble-cv-bridge
```

### Phase 2: Install the 3D Camera SDK (Angstrong / Nuwa HP60C)
Because 3D Depth cameras encrypt their data, you must install the manufacturer's ROS 2 SDK to extract the color video stream.
1. **Directory:** Navigate to your Home folder to download the SDK:
   ```bash
   cd ~
   git clone https://github.com/virensompura/ascam_ros2_ws.git
   ```
2. **Directory:** Any directory is fine. **Patch the Hardcoded Username Bug:**
   ```bash
   find ~/ascam_ros2_ws/src/ascamera -type f -exec sed -i 's|/home/admin1|/home/ats|g' {} +
   ```
   *(The manufacturer hardcoded `admin1` into their code. This changes it to `ats` so it doesn't crash).*
3. **Directory:** Navigate into the newly downloaded scripts folder to grant USB permissions:
   ```bash
   cd ~/ascam_ros2_ws/src/ascamera/scripts
   sudo bash create_udev_rules.sh
   ```
   **🚨 IMPORTANT:** Physically unplug the camera's USB cable from the robot and plug it back in so these permissions take effect!
4. **Directory:** Navigate to the root of the workspace to compile the SDK:
   ```bash
   cd ~/ascam_ros2_ws
   source /opt/ros/humble/setup.bash
   colcon build --symlink-install
   ```

### Phase 3: Transfer the ADAS Code
1. Copy the `Adas-1` folder from your PC to a USB Flash Drive.
2. Plug the USB Drive into the robot.
3. Drag and drop the `Adas-1` folder onto the robot's `Desktop` folder (so the path becomes `~/Desktop/Adas-1`).

### Phase 4: Run the System! (Daily Routine)
*(Note: Phases 1, 2, and 3 only need to be done **exactly once** during initial setup. From tomorrow onwards, you only ever need to run Phase 4!)*

This project uses a **Hybrid Camera System**. By default, it connects to the ROS 2 SDK. 

To run the car, open **three** separate terminal windows on the robot:

**Terminal 1 (Start the Camera SDK):**
**Directory:** Navigate to your Home folder (or run it from anywhere):
```bash
cd ~
source /opt/ros/humble/setup.bash && source ~/ascam_ros2_ws/install/setup.bash && ros2 launch ascamera hp60c.launch.py
```
*(Leave this running in the background. It talks to the USB port and goes into Power-Saving Lazy Streaming mode.)*

**Terminal 2 (Start the Motor Driver):**
**Directory:** You **MUST** navigate into the `adas` folder inside your project!
```bash
cd ~/Desktop/Adas-1/adas
source ~/ros2_ws/install/setup.bash
ros2 launch ./motor_driver.launch.py
```
*(This wakes up the robot's physical wheels so they can receive drive commands).*

**Terminal 3 (Start ADAS):**
**Directory:** You **MUST** navigate into the `adas` folder inside your project!
```bash
cd ~/Desktop/Adas-1/adas
source /opt/ros/humble/setup.bash && ./run.sh
```
*(This tells the motor driver how fast to spin the wheels and where to steer the servo).*

---

## 🛠 Troubleshooting & Testing

### "Waiting for SDK..." Error
If you run `./run.sh` and the screen is black with red text saying "WAITING FOR SDK...", it means Terminal 2 cannot find the camera feed from Terminal 1. 
- Make sure you ran the `ros2 launch` command in Terminal 1.
- Make sure `ascamera` successfully built without errors.

### Testing on a PC without the SDK (OpenCV Mode)
If you want to test the ADAS logic on a Windows/Mac PC using a standard webcam (without installing the heavy ROS 2 SDK), you can use the built-in fallback mode:
1. Run `python3 find_camera.py` to find your webcam's index number (e.g. `0` or `1`).
2. Run the ADAS system and pass that number:
   ```bash
   ./run.sh 0
   ```
This instantly disables the SDK requirement and reads your webcam directly!
