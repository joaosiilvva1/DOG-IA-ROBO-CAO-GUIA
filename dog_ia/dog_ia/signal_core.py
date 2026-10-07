"""Controlled simulated lamp classifier; not trained urban perception."""
import cv2
import numpy as np


def classify_lamp(bgr):
    # Only the forward central upper image is relevant in this calibrated scene.
    h,w=bgr.shape[:2]
    roi=bgr[int(h*.05):int(h*.75),int(w*.25):int(w*.75)]
    hsv=cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
    bounds={'red':[((0,130,100),(10,255,255)),((170,130,100),(179,255,255))],
            'yellow':[((18,130,100),(38,255,255))],
            'green':[((40,130,100),(90,255,255))]}
    candidates=[]
    for color,ranges in bounds.items():
        mask=np.zeros(hsv.shape[:2],dtype=np.uint8)
        for low,high in ranges:
            mask=cv2.bitwise_or(mask,cv2.inRange(hsv,np.array(low),np.array(high)))
        contours,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            area=cv2.contourArea(c);perimeter=cv2.arcLength(c,True)
            x,y,cw,ch=cv2.boundingRect(c)
            if area>=25 and perimeter>0 and .65<=cw/ch<=1.5 and 4*np.pi*area/(perimeter*perimeter)>=.65:
                candidates.append(color)
    return candidates[0] if len(candidates)==1 else 'unknown'


class SignalGate:
    def __init__(self):
        self.state='unknown';self.received=None;self.hold=True
    def update(self,state,now):
        self.state=state if state in ('red','yellow','green') else 'unknown'
        self.received=now
        if self.state!='green':self.hold=True
    def fresh_green(self,now):
        return self.received is not None and 0<=now-self.received<=.8 and self.state=='green'
    def resume(self,now):
        if not self.fresh_green(now):return False
        self.hold=False;return True
    def blocked(self,now):
        if self.received is None or not 0<=now-self.received<=.8:
            self.hold=True;return 'traffic_unknown'
        if self.state=='red':return 'traffic_red'
        if self.state=='yellow':return 'traffic_yellow'
        if self.state!='green':return 'traffic_unknown'
        return 'traffic_hold' if self.hold else None
