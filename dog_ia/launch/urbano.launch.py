"""Complete bounded navigation laboratory; not a real urban map."""
from pathlib import Path
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    share = Path(get_package_share_directory('dog_ia'))
    return LaunchDescription([
        DeclareLaunchArgument('gui', default_value='true'),
        IncludeLaunchDescription(PythonLaunchDescriptionSource(str(share/'launch/simulacao.launch.py')),
            launch_arguments={'world':str(share/'worlds/navegacao.world'),
                              'gui':LaunchConfiguration('gui'), 'rviz':'false'}.items()),
        IncludeLaunchDescription(PythonLaunchDescriptionSource(str(share/'launch/navegacao.launch.py'))),
        Node(package='rviz2', executable='rviz2', arguments=['-d',str(share/'rviz/navegacao.rviz')],
             parameters=[{'use_sim_time':True}], output='screen'),
    ])
