import socket
import time

CARBON_SERVER = '0.0.0.0'
CARBON_PORT = 2003

class CarbonEmitter(object):
    def emit(self, metric, value):
        key = "solectria." + metric.name + "." + metric.unit
        message = '%s %s %d\n' % (key, str(value), int(time.time()))

        sock = socket.socket()
        sock.connect((CARBON_SERVER, CARBON_PORT))
        sock.sendall(message)
        sock.close()


