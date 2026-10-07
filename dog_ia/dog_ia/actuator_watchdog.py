"""Independent simulated actuator watchdog; real motors need a hardware watchdog."""
import math
import time

import rclpy
from rclpy.clock import Clock, ClockType
from rclpy.node import Node
from geometry_msgs.msg import Twist


class ActuatorWatchdog(Node):
    def __init__(self):
        super().__init__('actuator_watchdog')
        self.received_at = None
        self.command = Twist()
        self.publisher = self.create_publisher(Twist, '/cmd_vel_safe', 10)
        self.create_subscription(Twist, '/cmd_vel_supervised', self.receive, 1)
        self.create_timer(0.05, self.tick,
            clock=Clock(clock_type=ClockType.STEADY_TIME))

    def receive(self, msg):
        if not math.isfinite(msg.linear.x) or not math.isfinite(msg.angular.z):
            self.received_at = None
            self.command = Twist()
            return
        self.command = Twist()
        self.command.linear.x = max(-0.2, min(0.2, msg.linear.x))
        self.command.angular.z = max(-0.5, min(0.5, msg.angular.z))
        self.received_at = time.monotonic()

    def tick(self):
        if self.received_at is None or time.monotonic()-self.received_at > 0.25:
            self.publisher.publish(Twist())
        else:
            self.publisher.publish(self.command)


def main(args=None):
    rclpy.init(args=args)
    node = ActuatorWatchdog()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.publisher.publish(Twist())
            node.destroy_node()
            rclpy.shutdown()
