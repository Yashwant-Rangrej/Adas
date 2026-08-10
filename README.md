# 🚗 MentorPi ADAS (Advanced Driver Assistance System)

Welcome to the MentorPi ADAS project! This repository contains Python-based software to run an autonomous driving system on a Raspberry Pi (MentorPi hardware). The system utilizes OpenCV for vision processing and ROS 2 for hardware control.

## ✨ Features
- **Lane Tracking:** Uses a camera to detect red lines and calculate steering angles to follow paths autonomously.
- **Traffic Sign Recognition:** Uses ORB feature matching to detect traffic signs like STOP, LEFT, RIGHT, DEADEND, SLOW, and SPEED_LIMIT.
- **Hardware Integration:** Communicates with MentorPi hardware via ROS 2 to control servos (steering) and DC motors (drive).
- **Obstacle Detection:** Stops automatically when an obstacle is detected by the hardware sensors.

## 📁 Project Structure
- `main.py` - The core script that runs the state machine and integrates all components.
- `camera.py` - Handles capturing video frames from the USB/Pi camera.
- `vision.py` - Processes images to find the track/line and calculates the center.
- `signs.py` - Detects traffic signs using computer vision (ORB).
- `steering.py` - Calculates steering commands based on line detection.
- `drive.py` - Controls vehicle speed and stopping.
- `hardware.py` - ROS 2 node that communicates directly with the MentorPi hardware (motors/servos).
- `setup.sh` / `run.sh` - Helper scripts for easy setup and execution.
- `assets/` - Reference images for traffic sign detection.

---

## 🚀 Getting Started

Follow these steps to set up your Raspberry Pi and run the system.

### Phase 1: Install Ubuntu on the Raspberry Pi
1. Download and open **Raspberry Pi Imager**.
2. Select your device (e.g., Raspberry Pi 4).
3. Under "Choose OS", go to **Other general-purpose OS** -> **Ubuntu** -> **Ubuntu 22.04 LTS (64-bit)**.
4. Flash this to your SD card.
5. Boot up the Raspberry Pi, connect it to a monitor, and connect to Wi-Fi.

### Phase 2: Install ROS 2 (Humble)
Open the terminal on your Raspberry Pi and run the following commands to install ROS 2:

**1. Setup Locale and Sources**
```bash
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

sudo apt install software-properties-common
sudo add-apt-repository universe

sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

**2. Install ROS 2 Core Packages**
```bash
sudo apt update
sudo apt install ros-humble-ros-base
```

### Phase 3: Transfer the Code
1. Copy your `Adas-1` folder to a USB Flash Drive.
2. Plug the USB Drive into the Raspberry Pi.
3. Drag and drop the `Adas-1` folder into your Home directory (or wherever you prefer).

### Phase 4: Install Dependencies & Run
Open a terminal on the Raspberry Pi, navigate into the folder, and run the setup scripts:

```bash
# 1. Navigate to the folder
cd ~/Adas-1

# 2. Make the scripts executable (only need to do this once)
chmod +x setup.sh run.sh

# 3. Run the setup script to install OpenCV and Numpy
./setup.sh

# 4. Start the ADAS system!
./run.sh
```

## 🛠 Troubleshooting
- **Camera Error:** Make sure your camera is properly connected. You might need to change `camera_index=0` in `main.py` if your camera mounts to a different `/dev/videoX` index.
- **ROS Errors:** Make sure `setup.sh` correctly sourced your ROS installation.
