# 🤖 Complete Robot Setup Guide (Ubuntu)

This document contains the exact, start-to-finish commands required to set up the 3D depth camera and run the ADAS system on your physical Ubuntu robot.

---

### Phase 1: Install Base Dependencies
**Directory:** Open a terminal (any directory is fine).
This installs the required ROS 2 build tools (`colcon`) and the Point Cloud/Vision libraries required by the 3D camera.
```bash
sudo apt update
sudo apt install -y python3-colcon-common-extensions libgflags-dev nlohmann-json3-dev libgoogle-glog-dev ros-humble-image-transport ros-humble-image-publisher ros-humble-pcl-conversions ros-humble-pcl-ros ros-humble-cv-bridge
```

### Phase 2: Download the Camera SDK
**Directory:** Navigate to your Home directory.
Download the raw C++ source code for the manufacturer's ROS 2 SDK.
```bash
cd ~
git clone https://github.com/virensompura/ascam_ros2_ws.git
```

### Phase 3: Patch the Hardcoded Username Bug
**Directory:** Any directory is fine.
**CRITICAL:** The developer of this camera SDK hardcoded their personal username (`admin1`) into the C++ source code. If your robot's username is `ats`, the camera will crash because it can't find the configuration files. Run this command to search all of their code and replace `admin1` with `ats`:
```bash
find ~/ascam_ros2_ws/src/ascamera -type f -exec sed -i 's|/home/admin1|/home/ats|g' {} +
```

### Phase 4: Configure USB Permissions (UDEV)
**Directory:** Navigate into the SDK's script folder.
Linux blocks raw USB access by default. You must install these rules to allow the SDK to talk to the camera hardware.
```bash
cd ~/ascam_ros2_ws/src/ascamera/scripts
sudo bash create_udev_rules.sh
```
**🚨 IMPORTANT:** After running this, you **MUST** physically unplug the camera's USB cable from the robot and plug it back in so the new rules activate!

### Phase 5: Compile the SDK
**Directory:** Navigate to the root of the workspace.
Now that the bug is patched and dependencies are installed, compile the C++ source code into ROS 2 executables.
```bash
cd ~/ascam_ros2_ws
source /opt/ros/humble/setup.bash
colcon build --symlink-install
```

---

### Phase 6: Run the ADAS System! (Daily Routine)
*(Note: Phases 1 through 5 only need to be done **exactly once**! The `colcon build` command permanently compiles the software. From tomorrow onwards, you only ever need to run the Terminal 1 and Terminal 2 commands in Phase 6!)*

*(Make sure you have copied the `Adas-1` folder from your PC onto the robot's `Desktop` before running this!)*

To run the car, you must open **two separate terminal windows** on the robot.

**Terminal 1 (Start the Camera SDK):**
**Directory:** Navigate to your Home folder.
```bash
cd ~
source /opt/ros/humble/setup.bash && source ~/ascam_ros2_ws/install/setup.bash && ros2 launch ascamera hp60c.launch.py
```
*(Leave this running in the background. It connects to the camera and publishes the video).*

**Terminal 2 (Start ADAS):**
**Directory:** You MUST navigate into the `adas` folder inside your project.
```bash
cd ~/Desktop/Adas-1/adas
source /opt/ros/humble/setup.bash && ./run.sh
```
