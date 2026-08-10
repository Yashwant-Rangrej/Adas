#!/bin/bash

cd "$(dirname "$0")" || exit
echo "=== ADAS Environment Setup ==="

# 1. Source the ROS 2 installation (Assuming Humble, change if using Foxy/Galactic)
# If ROS 2 is installed system-wide, this makes its libraries available.
if [ -f /opt/ros/humble/setup.bash ]; then
    echo "Sourcing ROS 2 Humble..."
    source /opt/ros/humble/setup.bash
else
    echo "Warning: ROS 2 Humble setup.bash not found. Please ensure ROS 2 is installed."
fi

# 2. Install pip dependencies (OpenCV and Numpy)
echo "Installing Python dependencies..."
# Ensure pip is installed on Ubuntu
sudo apt install python3-pip -y
pip3 install -r requirements.txt

echo "Setup complete. You can now run the system using ./run.sh"
