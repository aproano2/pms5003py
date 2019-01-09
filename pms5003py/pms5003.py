import serial
import sys
import codecs
import yaml
import signal
import yaml
import logging

logger = logging.getLogger(__name__)

# PMS5003 transport protocol-Active Mode
# Each field has a list indicating the field position
# in the frame. (e.g., [start_byte, num_bytes])
frame_info = { 'frame_size': 32, 'data_size': 30, 
               'fields':{'start_char': [0,2],
                         'frame_length': [2,2],
                         'PM1_std': [4,2],
                         'PM25_std': [6,2],
                         'PM10_std': [8,2],
                         'PM1_env': [10,2],
                         'PM25_env': [12,2],
                         'PM10_env': [14,2],
                         'P03': [16,2],
                         'P05': [18,2],
                         'P1': [20,2],
                         'P25': [22,2],
                         'P5': [24,2],
                         'P10': [26,2],
                         'reserved': [28,2],
                         'checksum': [30,2],
                         }
               }


class Timeout(Exception):
    """ Timeout decorator obtained from 
        https://www.saltycrane.com/blog/
    """
    def __init__(self, value = "Timed Out"):
        self.value = value
    def __str__(self):
        return repr(self.value)


class ChecksumError(Exception):
    def __init__(self, value = "Checksum failed"):
        self.value = value
    def __str__(self):
        return repr(self.value)


def timeout(seconds_before_timeout):
    """ Timeout decorator obtained from 
        https://www.saltycrane.com/blog
    """
    def decorate(f):
        def handler(signum, frame):
            raise Timeout()
        def new_f(*args, **kwargs):
            old = signal.signal(signal.SIGALRM, handler)
            signal.alarm(seconds_before_timeout)
            try:
                result = f(*args, **kwargs)
            finally:
                signal.signal(signal.SIGALRM, old)
                signal.alarm(0)
            return result
        new_f.__name__ = f.__name__
        return new_f
    return decorate


class pms5003():
    """This class handles the serial connection between the PMS5003 and 
       a Raspberry PI
    """
    
    def __init__(self, baudrate=9600, device='/dev/ttyS0', timeout=20):
        self.endian = sys.byteorder
        self.baudrate = baudrate
        self.device = device
        self.timeout = timeout
        self.start_char = b'424d'
        self.data = dict()
        self.frame = frame_info

            
    def conn_serial_port(self):
        """Define the connection with the serial port"""
        self.serial = serial.Serial(self.device, baudrate=self.baudrate)

        
    @timeout(20)
    def find_start_chars(self):
        while True:
            buff = self.serial.read(self.frame['fields']['start_char'][1])
            buff_hex = codecs.encode(buff, 'hex_codec')
            if buff_hex == self.start_char:
                return True

            
    def read_frame(self, data_size=30):
        try:
            self.conn_serial_port()
            if self.find_start_chars():
                buff = self.serial.read(data_size)
                buff_hex = self.start_char + codecs.encode(buff, 'hex_codec')
                try:
                    self.verify_checksum(buff_hex)
                    self.get_data(buff_hex)
                except ChecksumError:
                    logger.error("Checksum does not match", exc_info=True)
        except Timeout:
            logger.error("Timeout! No data collected in %s seconds",
                          self.timeout, exc_info=True)
            raise Timeout()

                
    def verify_checksum(self, buff_hex):
        """According to the specs, the checksum is stored in the last 4 bytes
        """
        checksum = 0
        checksum_size_nibble = 2*self.frame['fields']['checksum'][1]
        data = buff_hex[:-checksum_size_nibble]
        for x in range(0, len(data), 2):
            checksum += int(data[x:x+2], 16)
        if checksum != int(buff_hex[-checksum_size_nibble:], 16):
            raise ChecksumError()

        
    def get_data(self, buff_hex):
        no_data = ['start_char', 'frame_length', 'reserved', 'checksum']
        for k,v in self.frame['fields'].items():
            if k not in no_data:
                # Start and end points need to be in nibbles
                st = 2*v[0]
                nd = st + 2*v[1]
                self.data[k] = int(buff_hex[st:nd], 16)
