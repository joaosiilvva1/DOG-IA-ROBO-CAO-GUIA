"""Check real Nav2 action, map, TF, Gazebo displacement and supervised wiring."""
import json
import math
import time
import rclpy
from rclpy.action import ActionClient
from rclpy.qos import QoSProfile, DurabilityPolicy
from nav2_msgs.action import NavigateToPose
from nav_msgs.msg import OccupancyGrid
from gazebo_msgs.msg import ModelStates
from tf2_ros import Buffer, TransformListener

rclpy.init()
node=rclpy.create_node('validar_navegacao')
node.set_parameters([rclpy.parameter.Parameter('use_sim_time', value=True)])
world={}
map_info={}
def state(msg):
    if 'dog_ia' in msg.name:
        p=msg.pose[msg.name.index('dog_ia')].position
        world.update(x=p.x,y=p.y)
def grid(msg):
    map_info.update(width=msg.info.width,height=msg.info.height,known=sum(v>=0 for v in msg.data))
node.create_subscription(ModelStates,'/gazebo/model_states',state,10)
node.create_subscription(OccupancyGrid,'/map',grid,QoSProfile(depth=1,durability=DurabilityPolicy.TRANSIENT_LOCAL))
buffer=Buffer();listener=TransformListener(buffer,node)
client=ActionClient(node,NavigateToPose,'/navigate_to_pose')
try:
    end=time.monotonic()+20
    while time.monotonic()<end and (not world or not map_info):
        rclpy.spin_once(node,timeout_sec=.1)
    assert world and map_info['known']>100,'No real map or robot position'
    assert client.wait_for_server(timeout_sec=10),'Nav2 action unavailable'
    end=time.monotonic()+10
    transform=None
    while time.monotonic()<end:
        try:
            transform=buffer.lookup_transform('map','base_link',rclpy.time.Time());break
        except Exception:
            rclpy.spin_once(node,timeout_sec=.1)
    assert transform is not None,'No map -> base_link TF'
    initial=dict(world)
    goal=NavigateToPose.Goal();goal.pose.header.frame_id='map';goal.pose.header.stamp=node.get_clock().now().to_msg()
    goal.pose.pose.position.x=transform.transform.translation.x+1.0
    goal.pose.pose.position.y=transform.transform.translation.y-1.0
    goal.pose.pose.orientation.w=1.0
    sent=client.send_goal_async(goal);rclpy.spin_until_future_complete(node,sent,timeout_sec=10)
    assert sent.done(),'No goal response'
    handle=sent.result();assert handle.accepted,'Goal rejected'
    result=handle.get_result_async();end=time.monotonic()+90
    while not result.done() and time.monotonic()<end:
        rclpy.spin_once(node,timeout_sec=.1)
    if not result.done():
        cancel=handle.cancel_goal_async();rclpy.spin_until_future_complete(node,cancel,timeout_sec=5)
        raise AssertionError('Goal timed out and cancellation requested')
    assert result.result().status==4,f'Action status {result.result().status}'
    tf=buffer.lookup_transform('map','base_link',rclpy.time.Time())
    error=math.hypot(tf.transform.translation.x-goal.pose.pose.position.x,tf.transform.translation.y-goal.pose.pose.position.y)
    travel=math.hypot(world['x']-initial['x'],world['y']-initial['y'])
    assert error<.22 and travel>.8,(error,travel)
    motor_publishers=node.get_publishers_info_by_topic('/cmd_vel_safe')
    assert len(motor_publishers)==1 and motor_publishers[0].node_name=='actuator_watchdog','Nav2 bypasses watchdog'
    print(json.dumps({'result':'PASS','map':map_info,'initial_gazebo':initial,'final_gazebo':world,'goal_error_m':round(error,3),'displacement_m':round(travel,3),'motor_publisher':motor_publishers[0].node_name},ensure_ascii=False))
finally:
    node.destroy_node();rclpy.shutdown()
