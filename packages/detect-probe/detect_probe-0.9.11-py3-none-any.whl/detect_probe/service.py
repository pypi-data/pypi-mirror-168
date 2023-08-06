import subprocess
import inspect
from detect_probe import presto


class ProbeService:

    def __init__(self, token=None):
        self.token = token
        self.proc = None

    def start(self):
        self.proc = subprocess.Popen(['python3', '-c', inspect.getsource(presto)], env=dict(PRELUDE_TOKEN=self.token))

    def stop(self):
        self.proc.terminate()
