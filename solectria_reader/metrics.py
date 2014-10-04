import comms
import struct

class Metric(object):
    def __init__(self, name, unit, code, response_length, unit_conversion=None):
        assert response_length == 2 or response_length == 4

        self.name = name
        self.unit = unit
        self.code = code
        self.response_length = response_length
        self.unit_conversion = unit_conversion

    def fetch(self, connection):
        connection.send(self.code)
        
        try:
            response = connection.read(7 + self.response_length)
        except comms.NoResultException:
            return 0

        if self.response_length == 2:
            ctype = 'H'
        elif self.response_length == 4:
            ctype = 'L'

        code, length, value = struct.unpack('>BB%s' % ctype, response)
        if length != self.response_length:
            raise comms.ResultException('Response not expected length: was %d, expected %d' % (length, self.response_length))

        if self.unit_conversion:
            value = self.unit_conversion(value)

        return value

Vpv    = Metric('Vpv', 'Volts', '03 00 BA 00 01', 2, unit_conversion=lambda x: x/10.0)
Wac    = Metric('Wac', 'Watts', '03 00 C1 00 01', 2)
Aac    = Metric('Aac', 'Amps', '03 00 C2 00 01', 2, unit_conversion=lambda x: x/10.0)
Wtotal = Metric('Wtotal', 'kWh', '03 00 C4 00 02', 4, unit_conversion=lambda x: x/10.0)
Htotal = Metric('Htotal', 'Hours', '03 00 D1 00 01', 2)
Vac    = Metric('Vac', 'Volts', '03 00 C0 00 01', 2, unit_conversion=lambda x: x/10.0)

all_metrics = [Vpv, Wac, Aac, Vac, Wtotal, Htotal]

