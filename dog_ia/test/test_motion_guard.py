"""Tests for failure behavior, not just the nominal movement path."""
import math
from dog_ia.safety_core import MotionGuard


def ready():
    g = MotionGuard()
    g.set_scan([10.0]*360, -math.pi, 2*math.pi/359, 0.12, 10, 10)
    g.odom_at = 10
    g.set_command(0.15, 0, 10)
    return g


def test_no_sensor_blocks_movement():
    g = MotionGuard()
    g.set_command(0.15, 0, 10)
    assert g.evaluate(10)[:3] == (0, 0, 'sensor_lost')


def test_stale_command_stops_even_with_fresh_sensors():
    g = ready()
    g.scan_at = g.odom_at = 11
    assert g.evaluate(11)[:3] == (0, 0, 'idle')


def test_lost_scan_stops_with_fresh_command():
    g = ready()
    g.odom_at = 11
    g.set_command(0.15, 0, 11)
    assert g.evaluate(11)[2] == 'sensor_lost'


def test_lost_odometry_stops():
    g = ready()
    g.odom_at = None
    assert g.evaluate(10)[2] == 'odom_lost'


def test_front_obstacle_blocks_forward():
    g = ready()
    g.front = 0.35
    assert g.evaluate(10)[:3] == (0, 0, 'obstacle')


def test_rear_obstacle_blocks_reverse():
    g = ready()
    g.rear = 0.6
    g.set_command(-0.15, 0, 10)
    assert g.evaluate(10)[2] == 'obstacle'


def test_nearby_obstacle_blocks_turn():
    g = ready()
    g.nearest = 0.45
    g.set_command(0, 0.3, 10)
    assert g.evaluate(10)[2] == 'obstacle'


def test_nan_scan_is_not_free_space():
    g = ready()
    g.set_scan([math.nan]*360, -math.pi, 2*math.pi/359, 0.12, 10, 10)
    assert g.evaluate(10)[2] == 'scan_invalid'


def test_positive_infinite_scan_is_range_limit_not_nan():
    g = ready()
    g.set_scan([math.inf]*360, -math.pi, 2*math.pi/359, 0.12, 10, 10)
    assert g.evaluate(10)[2] == 'moving'


def test_partial_scan_has_no_rear_coverage():
    g = ready()
    g.set_scan([10.0]*90, -0.5, 1/89, 0.12, 10, 10)
    g.set_command(-0.15, 0, 10)
    assert g.evaluate(10)[2] == 'scan_invalid'


def test_speed_limits_and_invalid_command():
    g = ready()
    g.set_command(100, 100, 10)
    assert g.evaluate(10)[:2] == (0.2, 0.5)
    g.set_command(math.nan, 0, 10)
    assert g.evaluate(10)[:2] == (0, 0)


def test_emergency_cannot_be_resumed_by_unpausing():
    g = ready()
    g.emergency = True
    g.paused = False
    assert g.evaluate(10)[2] == 'emergency'


def test_resume_needs_new_command():
    g = ready()
    g.paused = True
    g.invalidate_command()
    g.paused = False
    assert g.evaluate(10)[2] == 'idle'
