"""ROS interface for the simulation motion supervisor."""
import json
import time

import rclpy
from rclpy.clock import Clock, ClockType
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
from std_srvs.srv import Trigger
from dog_ia.safety_core import MotionGuard


class SafetyNode(Node):
    def __init__(self):
        super().__init__('motion_supervisor')
        self.guard = MotionGuard()
        self.output = self.create_publisher(Twist, '/cmd_vel_supervised', 10)
        self.status = self.create_publisher(String, '/dog_ia/status', 10)
        self.create_subscription(Twist, '/cmd_vel', self.on_command, 10)
        self.create_subscription(LaserScan, '/scan', self.on_scan, qos_profile_sensor_data)
        self.create_subscription(Odometry, '/odom', self.on_odom, qos_profile_sensor_data)
        for action in ('pause', 'resume', 'emergency_stop', 'reset_emergency'):
            self.create_service(Trigger, '/dog_ia/'+action,
                                lambda req, res, name=action: self.control(name, res))
        self.timer = self.create_timer(0.05, self.tick,
            clock=Clock(clock_type=ClockType.STEADY_TIME))

    def on_command(self, msg):
        self.guard.set_command(msg.linear.x, msg.angular.z, time.monotonic())

    def on_scan(self, msg):
        age = (self.get_clock().now().nanoseconds-
               (msg.header.stamp.sec*1000000000+msg.header.stamp.nanosec))/1e9
        if age > 0.7 or age < -0.1 or msg.header.frame_id != 'lidar_link':
            self.guard.scan_at = None
            return
        self.guard.set_scan(msg.ranges, msg.angle_min, msg.angle_increment,
                            msg.range_min, msg.range_max, time.monotonic())

    def on_odom(self, msg):
        age = (self.get_clock().now().nanoseconds-
               (msg.header.stamp.sec*1000000000+msg.header.stamp.nanosec))/1e9
        self.guard.odom_at = time.monotonic() if -0.1 <= age <= 1 else None

    def control(self, action, response):
        self.guard.invalidate_command()
        if action == 'pause':
            self.guard.paused = True
        elif action == 'resume':
            self.guard.paused = False
        elif action == 'emergency_stop':
            self.guard.emergency = True
        elif action == 'reset_emergency':
            self.guard.emergency = False
            self.guard.paused = True
        response.success = True
        response.message = 'Operação aplicada. Movimento anterior descartado.'
        self.tick()
        return response

    def tick(self):
        now = time.monotonic()
        linear, angular, state, message = self.guard.evaluate(now)
        command = Twist()
        command.linear.x, command.angular.z = linear, angular
        self.output.publish(command)
        status = String()
        status.data = json.dumps({'state': state, 'message': message,
            'linear_velocity': linear, 'angular_velocity': angular,
            'paused': self.guard.paused, 'emergency': self.guard.emergency,
            'lidar_ok': self.guard.scan_at is not None and now-self.guard.scan_at <= 0.7,
            'odom_ok': self.guard.odom_at is not None and now-self.guard.odom_at <= 1,
            'front_distance': self.guard.front, 'rear_distance': self.guard.rear},
            ensure_ascii=False, allow_nan=False)
        self.status.publish(status)


def main(args=None):
    rclpy.init(args=args)
    node = SafetyNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.output.publish(Twist())
            node.destroy_node()
            rclpy.shutdown()
