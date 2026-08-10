#!/bin/bash

cd "$(dirname "$0")" || exit
echo "=== ADAS Environment Setup ==="

# 1. Source the ROS 2 installation (Assuming Humble, change if using Foxy/Galactic)
if [ -f /opt/ros/humble/setup.bash ]; then
    echo "Sourcing ROS 2 Humble..."
    source /opt/ros/humble/setup.bash
else
    echo "Warning: ROS 2 Humble setup.bash not found. Please ensure ROS 2 is installed."
fi

# 2. Install required ROS 2 packages
echo "Installing ROS 2 dependencies..."
sudo apt update
sudo apt install -y ros-humble-geometry-msgs ros-humble-sensor-msgs ros-humble-ros-robot-controller-msgs

# 3. Install pip dependencies (OpenCV, Numpy, and GPIO)
echo "Installing Python dependencies..."
# Ensure pip and gpiozero are installed on Ubuntu/Debian
sudo apt install python3-pip python3-gpiozero -y

# Use --break-system-packages for newer Ubuntu/Debian versions (like Raspberry Pi OS Bookworm)
# If it fails, it will fall back to standard pip install
pip3 install -r requirements.txt --break-system-packages || pip3 install -r requirements.txt

# Ensure run and test scripts are executable
chmod +x run.sh test_servo.py main.py

echo "Setup complete. You can now test the servo using: python3 test_servo.py"
echo "And run the system using: ./run.sh"
