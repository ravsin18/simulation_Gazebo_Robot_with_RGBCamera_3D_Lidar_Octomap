import os
import yaml
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch_ros.actions import Node
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Load YAML file
    config_file = os.path.join(get_package_share_directory('my_robot_bringup'), 'config', 'config.yaml')
    with open(config_file, 'r') as f:
        config_params = yaml.safe_load(f)

    urdf_path = config_params['robot_description']
    my_config_path = config_params['rviz_config']
    my_gazebo_path = config_params['gazebo_world']

    return LaunchDescription([
        # Robot state publisher node
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{'robot_description': Command(['xacro ', urdf_path])}]
        ),

        # Gazebo launch node
        Node(
            package='gazebo_ros',
            executable='gzserver',
            name='gazebo',
            output='screen',
            arguments=['-s', 'libgazebo_ros_factory.so', my_gazebo_path]
        ),

        # RViz node
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', my_config_path]
        ),
    ])
