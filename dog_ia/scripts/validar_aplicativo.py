import json
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError

import rclpy
from geometry_msgs.msg import Twist

BASE='http://localhost:8765'


def status():
    with urlopen(BASE+'/api/status',timeout=2) as response:
        return json.load(response)


def control(action):
    request=Request(BASE+'/api/control',data=json.dumps({'action':action}).encode(),
                    headers={'Content-Type':'application/json','Origin':BASE})
    with urlopen(request,timeout=4) as response:
        assert json.load(response)['ok']
    time.sleep(0.2)


rclpy.init()
node=rclpy.create_node('app_integration_test')
pub=node.create_publisher(Twist,'/cmd_vel',10)
time.sleep(1)
try:
    control('reset_emergency')
    assert status()['robot']['state']=='paused'
    control('resume')
    assert status()['connected']
    assert status()['robot']['state']=='idle'
    cmd=Twist();cmd.linear.x=0.1
    for _ in range(5):
        pub.publish(cmd);time.sleep(0.05)
    assert status()['robot']['state']=='moving'
    time.sleep(0.85)
    assert status()['robot']['linear_velocity']==0
    print('PASS: command timeout stops motion')
    control('pause')
    pub.publish(cmd);time.sleep(0.15)
    assert status()['robot']['state']=='paused'
    assert status()['robot']['linear_velocity']==0
    control('resume')
    assert status()['robot']['state']=='idle'
    print('PASS: pause blocks and resume discards old command')
    control('emergency_stop')
    control('resume')
    pub.publish(cmd);time.sleep(0.15)
    assert status()['robot']['state']=='emergency'
    assert status()['robot']['linear_velocity']==0
    control('reset_emergency')
    assert status()['robot']['state']=='paused'
    print('PASS: emergency remains latched; reset keeps paused')
    control('resume')
    assert not status()['traffic_light']['available']
    assert not status()['ground_hazards']['available']
    request=Request(BASE+'/api/control',data=b'{"action":"resume"}',
                    headers={'Content-Type':'application/json','Origin':'https://untrusted.example'})
    try:
        urlopen(request,timeout=2)
        raise AssertionError('Untrusted origin accepted')
    except HTTPError as error:
        assert error.code==403
    print('PASS: unknown origin blocked; perception availability is explicit')
finally:
    pub.publish(Twist())
    node.destroy_node();rclpy.shutdown()
