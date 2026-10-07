"""Publish camera-based lamp observations with three-frame green confirmation."""
import json
import time
from cv_bridge import CvBridge
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image
from std_msgs.msg import String
from dog_ia.signal_core import classify_lamp

class SignalNode(Node):
    def __init__(self):
        super().__init__('signal_detector')
        self.bridge=CvBridge();self.last='unknown';self.count=0
        self.publisher=self.create_publisher(String,'/dog_ia/signal',10)
        self.create_subscription(Image,'/camera/image_raw',self.image,qos_profile_sensor_data)
    def image(self,msg):
        age=(self.get_clock().now().nanoseconds-msg.header.stamp.sec*1000000000-msg.header.stamp.nanosec)/1e9
        try:
            state=classify_lamp(self.bridge.imgmsg_to_cv2(msg,'bgr8')) if -.1<=age<=.5 else 'unknown'
        except Exception:
            state='unknown'
        self.count=self.count+1 if state==self.last else 1;self.last=state
        if state=='green' and self.count<3:state='unknown'
        out=String();out.data=json.dumps({'state':state,'stamp':msg.header.stamp.sec+msg.header.stamp.nanosec/1e9})
        self.publisher.publish(out)

def main(args=None):
    rclpy.init(args=args);node=SignalNode()
    try:rclpy.spin(node)
    except KeyboardInterrupt:pass
    finally:
        node.destroy_node()
        if rclpy.ok():rclpy.shutdown()
