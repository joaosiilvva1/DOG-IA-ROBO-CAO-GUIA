#!/usr/bin/env python3

import cv2
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from std_msgs.msg import String


class ValidaAmbienteNode(Node):
    """Nó de validação inicial do ambiente ROS 2 do DOG-IA."""

    def __init__(self):
        super().__init__('valida_ambiente_node')
        self.bridge = CvBridge()
        self.publisher_ = self.create_publisher(String, 'dog_ia/status', 10)
        self.timer = self.create_timer(2.0, self.publica_status)
        self.get_logger().info('Nó de Validação do DOG-IA iniciado com sucesso!')

    def publica_status(self):
        msg = String()
        msg.data = 'DOG-IA Operacional: ROS 2 + OpenCV Prontos!'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Mensagem Publicada: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    node = ValidaAmbienteNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()