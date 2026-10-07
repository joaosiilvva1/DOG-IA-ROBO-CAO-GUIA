import json
import time
from urllib.request import urlopen

import rclpy
from geometry_msgs.msg import Twist
from gazebo_msgs.srv import SetEntityState
from gazebo_msgs.msg import ModelStates

rclpy.init()
node=rclpy.create_node('obstacle_validation')
pub=node.create_publisher(Twist,'/cmd_vel',10)
client=node.create_client(SetEntityState,'/gazebo/set_entity_state')
latest={}
sub=node.create_subscription(ModelStates,'/gazebo/model_states',lambda m:latest.update(states=m),10)


def wait(seconds):
    end=time.monotonic()+seconds
    while time.monotonic()<end:
        rclpy.spin_once(node,timeout_sec=0.05)


def place(x):
    assert client.wait_for_service(timeout_sec=3)
    request=SetEntityState.Request()
    request.state.name='dog_ia'
    request.state.reference_frame='world'
    request.state.pose.position.x=float(x)
    request.state.pose.position.z=0.03
    request.state.pose.orientation.w=1.0
    future=client.call_async(request)
    rclpy.spin_until_future_complete(node,future,timeout_sec=3)
    assert future.done() and future.result().success
    wait(1)


try:
    place(1.0)
    cmd=Twist();cmd.linear.x=0.15
    end=time.monotonic()+4
    while time.monotonic()<end:
        pub.publish(cmd)
        rclpy.spin_once(node,timeout_sec=0.05)
    with urlopen('http://localhost:8765/api/status',timeout=2) as response:
        status=json.load(response)
    assert status['robot']['state']=='obstacle',status
    assert status['robot']['linear_velocity']==0
    states=latest['states']
    x=states.pose[states.name.index('dog_ia')].position.x
    assert 1.03<x<1.35,x
    print(f'PASS: stopped before box at x={x:.3f} m, without physical collision')
finally:
    pub.publish(Twist());wait(0.4)
    place(0)
    node.destroy_node();rclpy.shutdown()
