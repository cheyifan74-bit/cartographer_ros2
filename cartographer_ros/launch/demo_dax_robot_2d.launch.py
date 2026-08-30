"""
PC-side offline demo:
  1) start Cartographer + URDF extrinsics
  2) open RViz
  3) play a bag recorded on the robot

Example:
  ros2 launch cartographer_ros demo_dax_robot_2d.launch.py \
    bag_filename:=/path/to/your_bag

  # Use robot-side parameter port:
  ros2 launch cartographer_ros demo_dax_robot_2d.launch.py \
    bag_filename:=/path/to/your_bag \
    configuration_basename:=dax_robot_2d_onboard.lua
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription, Shutdown
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import os


def generate_launch_description():
    bag_filename_arg = DeclareLaunchArgument('bag_filename')
    use_rviz_arg = DeclareLaunchArgument('use_rviz', default_value='true')
    configuration_basename_arg = DeclareLaunchArgument(
        'configuration_basename', default_value='dax_robot_2d.lua')

    pkg_share = FindPackageShare('cartographer_ros').find('cartographer_ros')

    mapping_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, 'launch', 'dax_robot_2d.launch.py')),
        launch_arguments={
            'use_sim_time': 'True',
            'configuration_basename': LaunchConfiguration('configuration_basename'),
        }.items(),
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=[
            '-d',
            os.path.join(pkg_share, 'configuration_files', 'demo_2d.rviz'),
        ],
        parameters=[{'use_sim_time': True}],
        on_exit=Shutdown(),
        output='screen',
    )

    # Replay sensors only. Skip /tf: bag already has map->odom which conflicts
    # with Cartographer; sensor extrinsics come from URDF.
    ros2_bag_play_cmd = ExecuteProcess(
        cmd=[
            'ros2', 'bag', 'play',
            LaunchConfiguration('bag_filename'),
            '--clock',
            '--topics', '/scan', '/imu/data', '/odom',
        ],
        name='rosbag_play',
        output='screen',
    )

    return LaunchDescription([
        bag_filename_arg,
        use_rviz_arg,
        configuration_basename_arg,
        mapping_launch,
        rviz_node,
        ros2_bag_play_cmd,
    ])
