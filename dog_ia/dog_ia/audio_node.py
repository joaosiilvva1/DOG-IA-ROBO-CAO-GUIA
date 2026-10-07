"""Python audio node: offline native TTS in WSL/Windows or espeak on Linux."""
import base64
import json
from pathlib import Path
import queue
import shutil
import subprocess
import threading
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class AudioNode(Node):
    def __init__(self):
        super().__init__('assistive_audio')
        self.last=None;self.queue=queue.Queue(maxsize=1)
        self.event=self.create_publisher(String,'/dog_ia/audio_text',10)
        self.windows=Path('/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe')
        self.espeak=shutil.which('espeak-ng') or shutil.which('espeak')
        self.enabled=self.declare_parameter('enabled',True).value
        self.create_subscription(String,'/dog_ia/status',self.status,10)
        threading.Thread(target=self.worker,daemon=True).start()
    def status(self,msg):
        try:
            state=json.loads(msg.data)
            if state['state']==self.last:return
            self.last=state['state'];text=state['message']
        except (ValueError,KeyError):return
        self.event.publish(String(data=text))
        if not self.enabled:return
        try:self.queue.get_nowait()
        except queue.Empty:pass
        self.queue.put_nowait(text)
    def worker(self):
        while rclpy.ok():
            try:text=self.queue.get(timeout=.2)
            except queue.Empty:continue
            try:
                if self.windows.exists():
                    # Quote data as a PowerShell string, never interpret ROS text as code.
                    literal=text.replace("'", "''")
                    script="Add-Type -AssemblyName System.Speech; $s=New-Object System.Speech.Synthesis.SpeechSynthesizer; $v=$s.GetInstalledVoices() | Where-Object {$_.VoiceInfo.Culture.Name -eq 'pt-BR'} | Select-Object -First 1; if ($v) {$s.SelectVoice($v.VoiceInfo.Name)}; $s.Speak('"+literal+"'); $s.Dispose()"
                    encoded=base64.b64encode(script.encode('utf-16le')).decode()
                    subprocess.run([str(self.windows),'-NoProfile','-NonInteractive','-EncodedCommand',encoded],check=True,timeout=45,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                elif self.espeak:
                    subprocess.run([self.espeak,'-v','pt-br','-s','155','--stdin'],input=text.encode(),check=True,timeout=45)
                else:
                    self.get_logger().error('Voz indisponível. Instale espeak-ng para Linux nativo.')
            except (subprocess.SubprocessError,OSError):
                self.get_logger().error('Falha ao reproduzir aviso de voz.')

def main(args=None):
    rclpy.init(args=args);node=AudioNode()
    try:rclpy.spin(node)
    except KeyboardInterrupt:pass
    finally:
        node.destroy_node()
        if rclpy.ok():rclpy.shutdown()
