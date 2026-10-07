"""Real depth-cloud tests for overhead box and depressed ground patch."""
import json
import time
import rclpy
from gazebo_msgs.srv import SetEntityState
from geometry_msgs.msg import Twist
from std_msgs.msg import String
rclpy.init();n=rclpy.create_node('validar_terreno');status={}
n.create_subscription(String,'/dog_ia/status',lambda msg:status.update(json.loads(msg.data)),10)
pub=n.create_publisher(Twist,'/cmd_vel',10);client=n.create_client(SetEntityState,'/gazebo/set_entity_state')
def wait(seconds,drive=False):
    end=time.monotonic()+seconds
    while time.monotonic()<end:
        cmd=Twist();cmd.linear.x=.12 if drive else 0.;pub.publish(cmd);rclpy.spin_once(n,timeout_sec=.05)
def move(name,x,y,z):
    assert client.wait_for_service(timeout_sec=5)
    req=SetEntityState.Request();req.state.name=name;req.state.reference_frame='world';req.state.pose.orientation.w=1.;req.state.pose.position.x=float(x);req.state.pose.position.y=float(y);req.state.pose.position.z=float(z)
    f=client.call_async(req);rclpy.spin_until_future_complete(n,f,timeout_sec=5);assert f.done() and f.result().success
    wait(2)
try:
    wait(3);assert status['terrain_state']=='clear',status
    move('placa_suspensa',1.0,0.,1.3)
    assert status['terrain_state']=='overhead_obstacle',status
    wait(.4,True);assert status['linear_velocity']==0,status
    move('placa_suspensa',3.,0.,1.3)
    move('dog_ia',.65,0.,.03)
    assert status['terrain_state']=='ground_hazard',status
    wait(.4,True);assert status['linear_velocity']==0,status
    print(json.dumps({'result':'PASS','clear_ground':'observed','overhead':'blocked from actual point cloud','ground_drop':'blocked from actual point cloud'}))
finally:
    move('placa_suspensa',3.,0.,1.3);move('dog_ia',0.,0.,.03);wait(.3);n.destroy_node();rclpy.shutdown()
