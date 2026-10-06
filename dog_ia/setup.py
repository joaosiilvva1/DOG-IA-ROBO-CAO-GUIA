from glob import glob
from setuptools import find_packages, setup

package_name = 'dog_ia'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        *[('share/' + package_name + '/' + folder, glob(folder + '/*'))
          for folder in ('launch', 'urdf', 'worlds', 'rviz', 'scripts')],
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='najoao',
    maintainer_email='najoao@todo.todo',
    description='Simulated assistive mobile robot with differential drive, LiDAR and RGB-D',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        ],
    },
)
