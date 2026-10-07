"""Local accessible app prototype connected to ROS; loopback only."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import threading
import time

from ament_index_python.packages import get_package_share_directory
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image, PointCloud2
from std_msgs.msg import String
from std_srvs.srv import Trigger


class AppNode(Node):
    def __init__(self):
        super().__init__('accessible_app')
        self.lock = threading.Lock()
        self.robot = None
        self.received = 0.0
        self.sensor_times = {}
        self.create_subscription(String, '/dog_ia/status', self.status, 10)
        for topic, kind, label in (('/camera/image_raw', Image, 'rgb'),
                                  ('/camera/depth/image_raw', Image, 'depth'),
                                  ('/camera/points', PointCloud2, 'points')):
            self.create_subscription(kind, topic,
                lambda msg, key=label: self.sensor(key), qos_profile_sensor_data)
        self.control_clients = {action: self.create_client(Trigger, '/dog_ia/'+action)
            for action in ('pause', 'resume', 'emergency_stop', 'reset_emergency')}

    def status(self, msg):
        try:
            status = json.loads(msg.data)
        except (ValueError, TypeError):
            return
        with self.lock:
            self.robot, self.received = status, time.monotonic()

    def sensor(self, name):
        with self.lock:
            self.sensor_times[name] = time.monotonic()

    def snapshot(self):
        now = time.monotonic()
        with self.lock:
            connected = self.robot is not None and now-self.received < 0.8
            robot = dict(self.robot) if connected else {
                'state': 'disconnected', 'message': 'Conexão com o supervisor indisponível.',
                'linear_velocity': 0, 'angular_velocity': 0,
                'lidar_ok': False, 'odom_ok': False, 'paused': False, 'emergency': False}
            return {'connected': connected, 'robot': robot,
                'sensors': {key: now-self.sensor_times.get(key, -100) < 1.2
                            for key in ('rgb', 'depth', 'points')},
                'traffic_light': {'available': False, 'message': 'Detector ainda não implementado'},
                'ground_hazards': {'available': False, 'message': 'Detector ainda não implementado'},
                'mode': 'simulation'}

    def control(self, action):
        client = self.control_clients[action]
        if not client.wait_for_service(timeout_sec=0.5):
            return False, 'Supervisor indisponível. Ação não confirmada.'
        future = client.call_async(Trigger.Request())
        end = time.monotonic()+2
        while not future.done() and time.monotonic() < end:
            time.sleep(0.01)
        if not future.done():
            return False, 'Sem confirmação. Verifique o estado do robô.'
        try:
            result = future.result()
            return result.success, result.message
        except Exception:
            return False, 'Falha ao confirmar a ação.'


def handler_for(node):
    page = Path(get_package_share_directory('dog_ia'))/'web/index.html'

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def send(self, code, body, content_type='application/json; charset=utf-8'):
            body = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False).encode()
            self.send_response(code)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(body)

        def valid_host(self):
            return self.headers.get('Host') in ('localhost:8765', '127.0.0.1:8765')

        def do_GET(self):
            if not self.valid_host():
                return self.send(403, {'error': 'Host não permitido'})
            if self.path == '/':
                return self.send(200, page.read_bytes(), 'text/html; charset=utf-8')
            if self.path == '/api/status':
                return self.send(200, node.snapshot())
            return self.send(404, {'error': 'Não encontrado'})

        def do_POST(self):
            if (not self.valid_host() or self.headers.get('Origin') not in
                    ('http://localhost:8765', 'http://127.0.0.1:8765')):
                return self.send(403, {'error': 'Origem não permitida'})
            if self.path != '/api/control':
                return self.send(404, {'error': 'Não encontrado'})
            try:
                size = int(self.headers.get('Content-Length', '0'))
                if not 0 < size <= 1024:
                    raise ValueError('Tamanho inválido')
                body = json.loads(self.rfile.read(size))
                action = body.get('action')
                if action not in node.control_clients:
                    raise ValueError('Ação inválida')
            except (ValueError, AttributeError):
                return self.send(400, {'error': 'Solicitação inválida'})
            ok, message = node.control(action)
            return self.send(200 if ok else 503, {'ok': ok, 'message': message})
    return Handler


def main(args=None):
    rclpy.init(args=args)
    node = AppNode()
    server = ThreadingHTTPServer(('127.0.0.1', 8765), handler_for(node))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    node.get_logger().info('Aplicativo local: http://localhost:8765')
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()
        server.server_close()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
