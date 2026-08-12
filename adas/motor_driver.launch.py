import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # Set the machine type environment variable required by odom_publisher
    os.environ['MACHINE_TYPE'] = 'MentorPi_Acker'

    return LaunchDescription([
        Node(
            package='ros_robot_controller',
            executable='ros_robot_controller',
            name='ros_robot_controller',
            output='screen'
        ),
        Node(
            package='controller',
            executable='odom_publisher',
            name='odom_publisher',
            output='screen'
        )
    ])
