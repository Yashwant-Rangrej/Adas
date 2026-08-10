# ADAS Raspberry Pi Setup Guide

This guide contains all the steps and commands required to set up your MentorPi (Raspberry Pi) from scratch and run the ADAS Python code.

## Phase 1: Install Ubuntu on the Raspberry Pi
1. Download and open **Raspberry Pi Imager**.
2. Select your device (e.g., Raspberry Pi 4).
3. Under "Choose OS", go to **Other general-purpose OS** -> **Ubuntu** -> **Ubuntu 22.04 LTS (64-bit)**.
4. Flash this to your SD card.
5. Put the SD card into the Raspberry Pi, power it on, connect it to a monitor, and connect to Wi-Fi.

## Phase 2: Install ROS 2 (Humble)
Once you are logged into the Ubuntu desktop on the Raspberry Pi, open the terminal and run the following commands one by one to install ROS 2 (which includes `rclpy` and `geometry_msgs`):

### 1. Setup Locale and Sources
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

### 2. Install ROS 2 Core Packages
```bash
sudo apt update
sudo apt install ros-humble-ros-base
```

## Phase 3: Transfer the Code
1. Copy your `adas` folder to a USB Flash Drive.
2. Plug the USB Drive into the Raspberry Pi.
3. Drag and drop the `adas` folder onto the Raspberry Pi's Desktop.

## Phase 4: Install Dependencies & Run
Open a terminal on the Raspberry Pi, navigate into the folder, and run the setup scripts:

```bash
# 1. Navigate to the folder
cd Desktop/adas

# 2. Make the scripts executable (only need to do this once)
chmod +x setup.sh run.sh

# 3. Run the setup script to install OpenCV and Numpy
./setup.sh

# 4. Start the ADAS system!
./run.sh
```
