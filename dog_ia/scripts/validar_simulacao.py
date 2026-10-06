"""Smoke test for the running simulated DOG-IA; moves it briefly in free space."""
import math
import time

import rclpy
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import CameraInfo, Image, JointState, LaserScan, PointCloud2
from rclpy.qos import qos_profile_sensor_data
from tf2_ros import Buffer, TransformListener

rclpy.init()
node = rclpy.create_node('dog_ia_validation')
data = {}
subscriptions = []
for name, kind in (
    ('/scan', LaserScan), ('/odom', Odometry), ('/joint_states', JointState),
    ('/camera/image_raw', Image), ('/camera/depth/image_raw', Image),
    ('/camera/points', PointCloud2), ('/camera/camera_info', CameraInfo),
    ('/gazebo/model_states', ModelStates),
):
    subscriptions.append(node.create_subscription(
        kind, name, lambda msg, key=name: data.update({key: msg}),
        qos_profile_sensor_data))
buffer = Buffer()
listener = TransformListener(buffer, node)
publisher = node.create_publisher(Twist, '/cmd_vel', 10)


def wait(seconds):
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        rclpy.spin_once(node, timeout_sec=0.05)


def model_pose():
    states = data['/gazebo/model_states']
    return states.pose[states.name.index('dog_ia')]


def move(seconds, linear=0.0, angular=0.0):
    cmd = Twist()
    cmd.linear.x = linear
    cmd.angular.z = angular
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        publisher.publish(cmd)
        rclpy.spin_once(node, timeout_sec=0.05)
    publisher.publish(Twist())
    wait(0.5)


try:
    wait(12)
    required = ('/scan', '/odom', '/joint_states', '/camera/image_raw',
                '/camera/depth/image_raw', '/camera/points',
                '/camera/camera_info', '/gazebo/model_states')
    missing = [key for key in required if key not in data]
    assert not missing, f'No messages: {missing}'
    scan = data['/scan']
    assert len(scan.ranges) == 360
    assert any(math.isfinite(v) and 0.12 < v < 5 for v in scan.ranges)
    assert data['/camera/image_raw'].width == 320
    assert data['/camera/depth/image_raw'].encoding == '32FC1'
    assert data['/camera/points'].width * data['/camera/points'].height > 0
    assert set(data['/joint_states'].name) == {'left_wheel_joint', 'right_wheel_joint'}
    for frame in ('base_footprint', 'base_link', 'left_wheel_link',
                  'right_wheel_link', 'caster_link', 'lidar_link',
                  'camera_link', 'camera_optical_frame'):
        assert buffer.can_transform('odom', frame, rclpy.time.Time()), frame
    print('PASS: LiDAR, RGB, depth, point cloud, odometry, wheel states and TF')
    start = model_pose()
    initial_odom = data['/odom'].pose.pose
    move(3, linear=0.15)
    finish = model_pose()
    distance = math.hypot(finish.position.x-start.position.x,
                          finish.position.y-start.position.y)
    odom = data['/odom'].pose.pose
    odom_distance = math.hypot(odom.position.x-initial_odom.position.x,
                               odom.position.y-initial_odom.position.y)
    assert distance > 0.15, f'Actual displacement too small: {distance}'
    assert abs(distance-odom_distance) < 0.1
    assert abs(finish.orientation.x) < 0.1 and abs(finish.orientation.y) < 0.1
    print(f'PASS: forward motion {distance:.3f} m; odometry {odom_distance:.3f} m')
    q0 = finish.orientation
    yaw0 = math.atan2(2*(q0.w*q0.z+q0.x*q0.y), 1-2*(q0.y*q0.y+q0.z*q0.z))
    move(2, angular=0.3)
    q1 = model_pose().orientation
    yaw1 = math.atan2(2*(q1.w*q1.z+q1.x*q1.y), 1-2*(q1.y*q1.y+q1.z*q1.z))
    delta = math.atan2(math.sin(yaw1-yaw0), math.cos(yaw1-yaw0))
    assert delta > 0.2, f'Turn too small or reversed: {delta}'
    print(f'PASS: left turn {delta:.3f} rad')
    before_stop = model_pose()
    wait(1)
    after_stop = model_pose()
    drift = math.hypot(after_stop.position.x-before_stop.position.x,
                       after_stop.position.y-before_stop.position.y)
    assert drift < 0.03, f'Robot did not stop: {drift}'
    print(f'PASS: zero command stops robot; drift {drift:.4f} m')
finally:
    publisher.publish(Twist())
    wait(0.2)
    node.destroy_node()
    rclpy.shutdown()
