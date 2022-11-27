from riemann_client.transport import TCPTransport
from riemann_client.client import QueuedClient
import time
import subprocess
import sys
from random import random

#target_ip = sys.argv[1]
target_ip = '10.65.132.155'

prefixf = 'Grafana_Test'
#host = subprocess.check_output('hostname').split('\n')[0]
host = 'Nloader100'



components = ['cpu', 'memory', 'disk', 'thread', 'queue', 'nic', 'bw', 'latency', 'pid' ]
apps = ['manager', 'streamer', 'storage', 'gui', 'database', 'monitor']
services = []
services = []

for i in range(0,11):
    for component in components:
        for app in apps:
            services.append(app+"."+component+"."+str(i))


while True:
        with QueuedClient(TCPTransport(target_ip, '15555')) as client:
            now = int(time.time())
            for service in services:
                metric_f = int(random()*100)
                print('==============> service is {} with value: {}'.format(service, metric_f))
                client.event(service=service , metric_f=metric_f, host=host, time=now, ttl=60, attributes={'prefix':prefixf})
                client.flush()
        time.sleep(2)
