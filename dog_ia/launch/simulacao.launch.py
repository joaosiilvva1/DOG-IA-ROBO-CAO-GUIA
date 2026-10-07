"""Start the DOG-IA robot, Gazebo Classic and optional RViz2."""
from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import xacro


def generate_launch_description():
    share = Path(get_package_share_directory('dog_ia'))
    gazebo_share = Path(get_package_share_directory('gazebo_ros'))
    description = xacro.process_file(str(share / 'urdf/dog_ia.urdf.xacro')).toxml()
    return LaunchDescription([
        DeclareLaunchArgument('gui', default_value='true'),
        DeclareLaunchArgument('rviz', default_value='true'),
        DeclareLaunchArgument('app', default_value='true'),
        DeclareLaunchArgument('world', default_value=str(share / 'worlds/teste.world')),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(str(gazebo_share / 'launch/gazebo.launch.py')),
            launch_arguments={'world': LaunchConfiguration('world'),
                              'gui': LaunchConfiguration('gui')}.items()),
        Node(package='dog_ia', executable='watchdog', output='screen'),
        Node(package='dog_ia', executable='supervisor',
             parameters=[{'use_sim_time': True}], output='screen'),
        Node(package='dog_ia', executable='aplicativo',
             condition=IfCondition(LaunchConfiguration('app')), output='screen'),
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             parameters=[{'robot_description': description, 'use_sim_time': True}],
             output='screen'),
        Node(package='gazebo_ros', executable='spawn_entity.py',
             arguments=['-entity', 'dog_ia', '-topic', 'robot_description',
                        '-x', '0', '-y', '0', '-z', '0.03'], output='screen'),
        Node(package='rviz2', executable='rviz2',
             arguments=['-d', str(share / 'rviz/dog_ia.rviz')],
             parameters=[{'use_sim_time': True}],
             condition=IfCondition(LaunchConfiguration('rviz')), output='screen'),
    ])
