"""
Launch Cartographer 2D mapping for dax_robot.
Publishes sensor extrinsics from dax_robot_2d.urdf.

configuration_basename:
  - dax_robot_2d.lua         (PC bag replay, with IMU)
  - dax_robot_2d_onboard.lua (robot-side parameter port, no IMU)
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import os


def generate_launch_description():
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time', default_value='True')
    configuration_basename_arg = DeclareLaunchArgument(
        'configuration_basename', default_value='dax_robot_2d.lua')

    pkg_share = FindPackageShare('cartographer_ros').find('cartographer_ros')
    urdf_file = os.path.join(pkg_share, 'urdf', 'dax_robot_2d.urdf')
    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {'robot_description': robot_desc},
            {'use_sim_time': LaunchConfiguration('use_sim_time')},
        ],
        output='screen',
    )

    cartographer_node = Node(
        package='cartographer_ros',
        executable='cartographer_node',
        name='cartographer_node',
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
        arguments=[
            '-configuration_directory',
            os.path.join(pkg_share, 'configuration_files'),
            '-configuration_basename',
            LaunchConfiguration('configuration_basename'),
        ],
        remappings=[
            ('scan', '/scan'),
            ('imu', '/imu/data'),
            ('odom', '/odom'),
        ],
        output='screen',
    )

    occupancy_grid_node = Node(
        package='cartographer_ros',
        executable='cartographer_occupancy_grid_node',
        name='cartographer_occupancy_grid_node',
        parameters=[
            {'use_sim_time': LaunchConfiguration('use_sim_time')},
            {'resolution': 0.05},
            {'publish_period_sec': 1.0},
        ],
        output='screen',
    )

    return LaunchDescription([
        use_sim_time_arg,
        configuration_basename_arg,
        robot_state_publisher_node,
        cartographer_node,
        occupancy_grid_node,
    ])
