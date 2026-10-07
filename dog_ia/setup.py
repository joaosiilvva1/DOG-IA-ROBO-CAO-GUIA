from glob import glob
from os.path import isfile
from setuptools import find_packages, setup

package_name = 'dog_ia'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        *[('share/' + package_name + '/' + folder, [path for path in glob(folder + '/*') if isfile(path)])
          for folder in ('launch', 'urdf', 'worlds', 'rviz', 'scripts', 'web', 'config')],
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='João Vitor da Silva Batista',
    maintainer_email='Developer.joaosilva@gmail.com',
    description='Simulated assistive mobile robot with differential drive, LiDAR and RGB-D',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'watchdog = dog_ia.actuator_watchdog:main',
            'supervisor = dog_ia.safety_node:main',
            'aplicativo = dog_ia.app_server:main',
            'teclado = dog_ia.teleop:main',
        ],
    },
)
