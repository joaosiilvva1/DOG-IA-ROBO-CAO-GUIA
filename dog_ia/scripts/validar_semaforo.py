"""Exercise actual Gazebo lamps, camera detector, voice topic and motor gate."""
import json
import math
import time
import rclpy
from geometry_msgs.msg import Twist
from gazebo_msgs.msg import ModelStates
from gazebo_msgs.srv import SetEntityState
from std_msgs.msg import String
from std_srvs.srv import Trigger
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from rclpy.qos import qos_profile_sensor_data
import cv2
from pathlib import Path

rclpy.init();n=rclpy.create_node('validar_semaforo');status={};world={};spoken=[];frame={}
def on_status(msg):status.update(json.loads(msg.data))
def position(msg):
    if 'dog_ia' in msg.name:
        p=msg.pose[msg.name.index('dog_ia')].position;world.update(x=p.x,y=p.y)
n.create_subscription(String,'/dog_ia/status',on_status,10)
n.create_subscription(String,'/dog_ia/audio_text',lambda msg:spoken.append(msg.data),10)
n.create_subscription(ModelStates,'/gazebo/model_states',position,10)
n.create_subscription(Image,'/camera/image_raw',lambda msg:frame.update(image=msg),qos_profile_sensor_data)
pub=n.create_publisher(Twist,'/cmd_vel',10)
setter=n.create_client(SetEntityState,'/gazebo/set_entity_state')
resume=n.create_client(Trigger,'/dog_ia/resume')
def wait(seconds,drive=False):
    end=time.monotonic()+seconds
    while time.monotonic()<end:
        cmd=Twist();cmd.linear.x=.12 if drive else 0.0;pub.publish(cmd)
        rclpy.spin_once(n,timeout_sec=.05)
def lamp(active):
    assert setter.wait_for_service(timeout_sec=5)
    for i,color in enumerate(['red','yellow','green']):
        req=SetEntityState.Request();req.state.name='lamp_'+color;req.state.reference_frame='world';req.state.pose.orientation.w=1.0
        req.state.pose.position.x=3.0 if color==active else -5.0
        req.state.pose.position.y=0.0 if color==active else 3.0
        req.state.pose.position.z=1.3 if color==active else 3.0+i*.3
        f=setter.call_async(req);rclpy.spin_until_future_complete(n,f,timeout_sec=5)
        assert f.done() and f.result().success,'Could not change lamp'
    wait(1.5)
def request_resume():
    assert resume.wait_for_service(timeout_sec=3)
    f=resume.call_async(Trigger.Request());rclpy.spin_until_future_complete(n,f,timeout_sec=5)
    assert f.done();return f.result().success
try:
    wait(2)
    for color,expected in [('red','traffic_red'),('yellow','traffic_yellow')]:
        lamp(color);assert status['state']==expected,status
        assert not request_resume(),'Closed signal accepted resume'
        start=dict(world);wait(1,True)
        assert status['linear_velocity']==0 and math.hypot(world['x']-start['x'],world['y']-start['y'])<.02
    lamp('green');assert status['state']=='traffic_hold',status
    assert request_resume();start=dict(world);wait(1.5,True)
    moved=math.hypot(world['x']-start['x'],world['y']-start['y']);assert moved>.08,moved
    lamp('red');wait(.5,True);assert status['state']=='traffic_red' and status['linear_velocity']==0,status
    image=CvBridge().imgmsg_to_cv2(frame['image'],'bgr8')
    target=Path('/home/najoao/ros2_ws/src/DOG-IA-ROBO-CAO-GUIA/docs/evidencias/semaforo-camera.png')
    cv2.imwrite(str(target),image)
    lamp(None);assert status['state']=='traffic_unknown',status
    assert any('vermelho' in text.lower() for text in spoken),'No real audio event'
    print(json.dumps({'result':'PASS','red':'blocked','yellow':'blocked','green':'explicit resume required','unknown':'blocked','green_displacement_m':round(moved,3),'voice_event_received':True}))
finally:
    lamp('red');wait(.3);n.destroy_node();rclpy.shutdown()
