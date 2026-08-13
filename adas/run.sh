#!/bin/bash
cd "$(dirname "$0")" || exit

# Start the Hardware PWM daemon on a safe DMA channel to prevent USB mouse crashing!
sudo pigpiod -t 0 -d 10 || true

# Source ROS 2 Humble environment and local workspaces
if [ -f /opt/ros/humble/setup.bash ]; then
    source /opt/ros/humble/setup.bash
fi
if [ -f ~/ros2_ws/install/setup.bash ]; then
    source ~/ros2_ws/install/setup.bash
fi
if [ -f ~/ascam_ros2_ws/install/setup.bash ]; then
    source ~/ascam_ros2_ws/install/setup.bash
fi

echo "Starting ADAS System on Raspberry Pi..."

# Run the python script (using python3 which is standard on Raspberry Pi)
python3 main.py "$@"
