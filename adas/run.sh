#!/bin/bash
cd "$(dirname "$0")" || exit

# Source ROS 2 Humble environment
if [ -f /opt/ros/humble/setup.bash ]; then
    source /opt/ros/humble/setup.bash
fi

echo "Starting ADAS System on Raspberry Pi..."

# Run the python script (using python3 which is standard on Raspberry Pi)
python3 main.py "$@"
