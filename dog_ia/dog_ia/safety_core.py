"""Conservative motion rules for the simulation; not a certified safety system."""
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Limits:
    max_linear: float = 0.20
    max_angular: float = 0.50
    command_timeout: float = 0.60
    scan_timeout: float = 0.70
    odom_timeout: float = 1.0
    margin: float = 0.30
    braking_acceleration: float = 0.50


class MotionGuard:
    def __init__(self, limits=None):
        self.limits = limits or Limits()
        self.command = (0.0, 0.0)
        self.command_at = None
        self.scan_at = None
        self.odom_at = None
        self.front = self.rear = self.nearest = None
        self.paused = False
        self.emergency = False

    def set_command(self, linear, angular, now):
        if not math.isfinite(linear) or not math.isfinite(angular):
            self.command_at = None
            self.command = (0.0, 0.0)
            return
        self.command = (max(-self.limits.max_linear, min(self.limits.max_linear, linear)),
                        max(-self.limits.max_angular, min(self.limits.max_angular, angular)))
        self.command_at = now

    def invalidate_command(self):
        self.command_at = None
        self.command = (0.0, 0.0)

    def set_scan(self, ranges, angle_min, angle_increment, range_min, range_max, now):
        self.front = self.rear = self.nearest = None
        self.scan_at = now
        if (len(ranges) < 30 or not all(math.isfinite(v) for v in
                (angle_min, angle_increment, range_min, range_max))
                or angle_increment <= 0 or not 0 < range_min < range_max):
            return
        front, rear, all_values = [], [], []
        for i, value in enumerate(ranges):
            angle = angle_min + i*angle_increment
            angle = math.atan2(math.sin(angle), math.cos(angle))
            valid = value == math.inf or (math.isfinite(value) and range_min <= value <= range_max)
            distance = min(value, range_max) if valid else None
            all_values.append(distance)
            if abs(angle) <= math.radians(35):
                front.append(distance)
            if abs(angle) >= math.radians(145):
                rear.append(distance)

        def minimum(values):
            valid = [v for v in values if v is not None]
            if len(values) < 5 or len(valid) < 0.95*len(values):
                return None
            return min(valid)
        self.front, self.rear, self.nearest = map(minimum, (front, rear, all_values))

    def evaluate(self, now):
        if self.emergency:
            return 0.0, 0.0, 'emergency', 'Parada de emergência acionada.'
        if self.paused:
            return 0.0, 0.0, 'paused', 'Robô pausado.'
        if self.scan_at is None or now-self.scan_at > self.limits.scan_timeout:
            return 0.0, 0.0, 'sensor_lost', 'LiDAR indisponível. Robô parado.'
        if self.odom_at is None or now-self.odom_at > self.limits.odom_timeout:
            return 0.0, 0.0, 'odom_lost', 'Odometria indisponível. Robô parado.'
        if self.command_at is None or now-self.command_at > self.limits.command_timeout:
            return 0.0, 0.0, 'idle', 'Robô parado, aguardando comando.'
        linear, angular = self.command
        if linear == 0 and angular == 0:
            return 0.0, 0.0, 'idle', 'Robô parado, aguardando comando.'
        threshold = self.limits.margin + abs(linear)*0.2 + linear*linear/(2*self.limits.braking_acceleration)
        if linear != 0:
            clearance = self.front if linear > 0 else self.rear
            # LiDAR is 0.15 m ahead of base center; rear extends 0.40 m behind it.
            offset = 0.10 if linear > 0 else 0.40
            if clearance is None:
                return 0.0, 0.0, 'scan_invalid', 'Leitura incompleta na direção do movimento.'
            if clearance < threshold+offset:
                return 0.0, 0.0, 'obstacle', 'Obstáculo próximo. Robô parado.'
        if angular != 0:
            if self.nearest is None:
                return 0.0, 0.0, 'scan_invalid', 'Leitura incompleta para realizar o giro.'
            if self.nearest < 0.55:
                return 0.0, 0.0, 'obstacle', 'Obstáculo próximo. Giro bloqueado.'
        return linear, angular, 'moving', 'Robô em movimento supervisionado.'
