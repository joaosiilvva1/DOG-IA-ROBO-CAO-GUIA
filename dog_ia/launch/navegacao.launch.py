"""Attach SLAM and supervised Nav2 to the already running simulation."""
from pathlib import Path
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    share = Path(get_package_share_directory('dog_ia'))
    slam = Path(get_package_share_directory('slam_toolbox'))
    nav = Path(get_package_share_directory('nav2_bringup'))
    return LaunchDescription([
        IncludeLaunchDescription(PythonLaunchDescriptionSource(str(slam/'launch/online_async_launch.py')),
            launch_arguments={'use_sim_time': 'true', 'slam_params_file': str(share/'config/slam.yaml')}.items()),
        IncludeLaunchDescription(PythonLaunchDescriptionSource(str(nav/'launch/navigation_launch.py')),
            launch_arguments={'use_sim_time': 'true', 'autostart': 'true', 'use_composition': 'False',
                              'params_file': str(share/'config/nav2.yaml')}.items()),
    ])
