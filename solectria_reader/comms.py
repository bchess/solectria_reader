import binascii
import struct

import crcmod
import serial

VERSION = '0A'
SOLAR_ID = '0A'
TERMINATOR = '0D'

calculate_crc = crcmod.predefined.mkCrcFun('modbus')

class ResultException(Exception):
    pass

class NoResultException(ResultException):
    pass

class Connection(object):
    def __init__(self):
        self.serial = serial.Serial()
        self.serial.port = '/dev/ttyUSB0'
        self.serial.baudrate = 19200
        self.serial.bytesize = serial.EIGHTBITS
        self.serial.parity = serial.PARITY_NONE
        self.serial.stopbits = serial.STOPBITS_ONE
        self.serial.timeout = 0.1
        self.serial.xonxoff = False
        self.serial.rtscts = False
        self.serial.dsrdtr = False
        self.serial.writeTimeout = 2

    def __enter__(self):
        self.serial.open()
        return self

    def __exit__(self, type, value, traceback):
        self.serial.close()

    def send(self, code):
        to_send = compute_to_send(SOLAR_ID, code)

        self.serial.flushInput()
        self.serial.flushOutput()

        self.serial.write(to_send)

    def read(self):
        result = self.serial.read(size=16)
        if len(result) == 0:
            raise NoResultException()

        # Strip prefix, crc, and terminator
        return parse_result(SOLAR_ID, result)

def compute_to_send(solar_id, code):
    cmd = solar_id + code
    cmd_hex = str(bytearray.fromhex(cmd))

    crc = '%04x' % calculate_crc(cmd_hex)
    # flip the bytes of the crc
    crc = crc[2:4] + crc[0:2]

    return bytearray.fromhex(VERSION + cmd + crc + TERMINATOR)

def parse_result(solar_id, response):
    if len(response) <= 5:
        raise ResultException('Response not long enough, is only %d bytes' % len(response))

    solar_id = int(solar_id, 16)
    version_code, result_solar_id = struct.unpack_from('>BB', response)
    if result_solar_id != solar_id:
        raise ResultException('Solar IDs do not match: was %s, expected %s' % (hex(result_solar_id), hex(solar_id)))

    result = response[2:-3]
    result_for_crc = response[1:-3]
    calculated_crc = '%04x' % calculate_crc(result_for_crc)

    result_crc, terminator = struct.unpack_from('>HB', response, offset=len(response)-3)
    result_crc = '%04x' % result_crc
    result_crc = result_crc[2:4] + result_crc[0:2]
    if calculated_crc != result_crc:
        raise ResultException('CRC does not match: was %s, expected %s' % (result_crc, calculated_crc))

    return result

def test_parse_result():
    result = parse_result('01', str(bytearray.fromhex('0A 01 03 04 00 00 08 AC FD 8E 0D')))
    assert result == bytearray.fromhex('03 04 00 00 08 AC')

if __name__ == '__main__':
    test_parse_result()
