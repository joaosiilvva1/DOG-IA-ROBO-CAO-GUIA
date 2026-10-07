"""Conservative calibrated floor and overhead observation in simulation."""
import json
import time
import numpy as np
import rclpy
from rclpy.node import Node
from rclpy.clock import Clock, ClockType
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import PointCloud2
from sensor_msgs_py import point_cloud2
from std_msgs.msg import String
from tf2_ros import Buffer, TransformListener

class TerrainNode(Node):
    def __init__(self):
        super().__init__('terrain_detector')
        self.buffer=Buffer();self.listener=TransformListener(self.buffer,self)
        self.floor='unknown';self.overhead='unknown';self.floor_at=0;self.overhead_at=0
        self.pub=self.create_publisher(String,'/dog_ia/terrain',10)
        self.create_subscription(PointCloud2,'/ground/points',lambda m:self.cloud(m,True),qos_profile_sensor_data)
        self.create_subscription(PointCloud2,'/camera/points',lambda m:self.cloud(m,False),qos_profile_sensor_data)
        self.create_timer(.1,self.tick,clock=Clock(clock_type=ClockType.STEADY_TIME))
    def cloud(self,msg,ground):
        state='unknown';now=time.monotonic()
        try:
            age=self.get_clock().now().nanoseconds/1e9-msg.header.stamp.sec-msg.header.stamp.nanosec/1e9
            if not -.1<=age<=.5:raise ValueError('old cloud')
            tf=self.buffer.lookup_transform('base_footprint',msg.header.frame_id,rclpy.time.Time.from_msg(msg.header.stamp))
            raw=point_cloud2.read_points(msg,field_names=('x','y','z'),skip_nans=False)
            pts=np.column_stack((raw['x'],raw['y'],raw['z']))[::16].astype(float)
            pts=pts[np.isfinite(pts).all(axis=1)]
            if len(pts)<20:raise ValueError('insufficient cloud')
            q=tf.transform.rotation;x,y,z,w=q.x,q.y,q.z,q.w
            rot=np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],
                          [2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],
                          [2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])
            t=tf.transform.translation;pts=pts@rot.T+np.array([t.x,t.y,t.z])
            pts=pts[np.isfinite(pts).all(axis=1)]
            if ground:
                corridor=pts[(pts[:,0]>=.45)&(pts[:,0]<1.5)&(abs(pts[:,1])<.3)]
                if np.sum(corridor[:,2]<-.10)>=8 or np.sum(corridor[:,2]>.12)>=12:
                    state='hazard'
                else:
                    floor=corridor[abs(corridor[:,2])<.07]
                    cells={(min(2,int((v[0]-.45)/.35)),min(2,int((v[1]+.3)/.2))) for v in floor}
                    if len(floor)>=60 and len(cells)==9:state='clear'
            else:
                corridor=pts[(pts[:,0]>.35)&(pts[:,0]<1.8)&(abs(pts[:,1])<.35)&(pts[:,2]>.55)&(pts[:,2]<1.9)]
                state='hazard' if len(corridor)>=12 else 'clear'
        except Exception as error:
            self.get_logger().warning(str(error), throttle_duration_sec=5.0)
            state='unknown'
        if ground:self.floor,self.floor_at=state,now
        else:self.overhead,self.overhead_at=state,now
    def tick(self):
        now=time.monotonic();floor=self.floor if now-self.floor_at<.8 else 'unknown';overhead=self.overhead if now-self.overhead_at<.8 else 'unknown'
        state='ground_hazard' if floor=='hazard' else 'overhead_obstacle' if overhead=='hazard' else 'terrain_unknown' if floor=='unknown' or overhead=='unknown' else 'clear'
        self.pub.publish(String(data=json.dumps({'state':state,'floor':floor,'overhead':overhead})))

def main(args=None):
    rclpy.init(args=args);node=TerrainNode()
    try:rclpy.spin(node)
    except KeyboardInterrupt:pass
    finally:
        node.destroy_node()
        if rclpy.ok():rclpy.shutdown()
