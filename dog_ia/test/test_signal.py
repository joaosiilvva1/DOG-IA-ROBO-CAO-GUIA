import cv2
import numpy as np
from dog_ia.signal_core import classify_lamp, SignalGate


def image(color):
    img=np.zeros((240,320,3),np.uint8)
    cv2.circle(img,(160,80),12,color,-1)
    return img


def test_controlled_colors():
    for bgr,state in [((0,0,255),'red'),((0,255,255),'yellow'),((0,255,0),'green')]:
        assert classify_lamp(image(bgr))==state


def test_no_light_or_ambiguous():
    assert classify_lamp(np.zeros((240,320,3),np.uint8))=='unknown'
    img=image((0,0,255));cv2.circle(img,(190,80),12,(0,255,0),-1)
    assert classify_lamp(img)=='unknown'


def test_gate_requires_fresh_green_and_explicit_resume():
    g=SignalGate();assert g.blocked(0)=='traffic_unknown'
    g.update('red',0);assert not g.resume(.1)
    g.update('yellow',.1);assert g.blocked(.2)=='traffic_yellow'
    g.update('green',.2);assert g.blocked(.3)=='traffic_hold'
    assert g.resume(.3);assert g.blocked(.3) is None
    assert g.blocked(1.1)=='traffic_unknown'
    g.update('green',1.2);assert g.blocked(1.3)=='traffic_hold'


def test_unknown_relocks_and_old_green_cannot_resume():
    g=SignalGate();g.update('green',0);assert g.resume(.1)
    g.update('bad',.2);assert g.blocked(.3)=='traffic_unknown'
    g.update('green',.4);assert not g.resume(2)
