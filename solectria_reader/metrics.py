import comms
import struct

class Metric(object):
    def __init__(self, name, code, response_length):
        assert response_length == 2 or response_length == 4

        self.name = name
        self.code = code
        self.response_length = response_length

    def fetch(self, connection):
        connection.send(self.code)
        
        try:
            response = connection.read()
        except comms.NoResultException:
            return 0

        if self.response_length == 2:
            ctype = 'H'
        elif self.response_length == 4:
            ctype = 'L'

        code, length, value = struct.unpack('>BB%s' % ctype, response)
        if length != self.response_length:
            raise comms.ResultException('Response not expected length: was %d, expected %d' % (length, self.response_length))

        return value

Wac = Metric('Wac', '03 00 C1 00 01', 2)

all_metrics = [Wac]

