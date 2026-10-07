"""Keyboard teleoperation with a dead-man timeout for Ubuntu terminals."""
import select
import sys
import termios
import time
import tty

import rclpy
from geometry_msgs.msg import Twist


def main(args=None):
    if not sys.stdin.isatty():
        raise SystemExit('Abra este comando em um terminal Ubuntu interativo.')
    settings = termios.tcgetattr(sys.stdin)
    rclpy.init(args=args)
    node = rclpy.create_node('dog_ia_keyboard')
    publisher = node.create_publisher(Twist, '/cmd_vel', 10)
    linear, angular, last_key = 0.0, 0.0, 0.0
    bindings = {'i': (0.15, 0.0), ',': (-0.15, 0.0),
                'j': (0.0, 0.3), 'l': (0.0, -0.3), 'k': (0.0, 0.0)}
    print('DOG-IA: segure i para avançar, vírgula para recuar, j/l para girar.')
    print('k ou espaço: parar. Ctrl+C: sair. Sem teclas por 0,5 s: parada.')
    try:
        tty.setcbreak(sys.stdin.fileno())
        while rclpy.ok():
            if select.select([sys.stdin], [], [], 0.05)[0]:
                key = sys.stdin.read(1)
                if key == '\x03':
                    break
                linear, angular = bindings.get(key, (0.0, 0.0))
                last_key = time.monotonic()
            if time.monotonic()-last_key > 0.5:
                linear, angular = 0.0, 0.0
            msg = Twist()
            msg.linear.x, msg.angular.z = linear, angular
            publisher.publish(msg)
            rclpy.spin_once(node, timeout_sec=0)
    except KeyboardInterrupt:
        pass
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        if rclpy.ok():
            for _ in range(3):
                publisher.publish(Twist())
                time.sleep(0.05)
            node.destroy_node()
            rclpy.shutdown()
