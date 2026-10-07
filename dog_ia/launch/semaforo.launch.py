"""Controlled camera signal test with supervised movement and native voice."""
from pathlib import Path
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    share=Path(get_package_share_directory('dog_ia'))
    return LaunchDescription([
        IncludeLaunchDescription(PythonLaunchDescriptionSource(str(share/'launch/simulacao.launch.py')),
            launch_arguments={'world':str(share/'worlds/semaforo.world'),'require_signal':'true'}.items()),
        Node(package='dog_ia',executable='semaforo',parameters=[{'use_sim_time':True}],output='screen'),
        Node(package='dog_ia',executable='audio',output='screen'),
    ])
