import json
import os
import socket
import subprocess
import sys
import inspect
from urllib import request

from detect_probe import presto


class ProbeService:

    def __init__(self, token=None, account_id=os.getenv('PRELUDE_ACCOUNT_ID'), account_secret=os.getenv('PRELUDE_ACCOUNT_SECRET')):
        self.token = token
        self.account_id = account_id
        self.account_secret = account_secret
        self.proc = None

    def start(self):
        self.proc = subprocess.Popen([sys.executable, '-c', inspect.getsource(presto)], env=dict(PRELUDE_TOKEN=self.token))

    def stop(self):
        self.proc.terminate()

    def register(self, name=socket.gethostname()):
        api = f"{os.getenv('PRELUDE_HQ', 'https://detect.prelude.org')}/account/endpoint"
        r = request.Request(api, data=str.encode(json.dumps(dict(id=name))), headers={'account': self.account_id, 'token': self.account_secret,
                                                                                      'Content-Type': 'application/json'})
        with request.urlopen(r) as rs:
            self.token = rs.read().decode('utf8')
