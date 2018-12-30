import serial
import time
import sys
from struct import *
import codecs


class pms5003():
    """This class handles the serial connection between the PMS5003 and a Raspberry PI
    """
    
    def __init__(self, baudrate=9600, device='/dev/ttyS0', start_chars=b'424d', start_size=2, data_size=32, checksum_size=2):
        self.endian = sys.byteorder
        self.baudrate = baudrate
        self.device = device
        self.start_chars = start_chars
        self.start_size = start_size
        self.data_size = data_size
        self.checksum_size = checksum_size
    
    def conn_serial_port(self):
        """Define the connection with the serial port"""
        self.serial = serial.Serial(self.device, baudrate=self.baudrate)

    def find_start_chars(self):
        # TODO: Add a timeout, if nothing is read, report an error
        while True:
            buff = self.serial.read(self.start_size)
            buff_hex = codecs.encode(buff, 'hex_codec')
            if buff_hex == self.start_chars:
                return True

    def get_data(self, data_size=30):
        if self.find_start_chars:
            buff = self.serial.read(data_size)
            buff_hex = codecs.encode(buff, 'hex_codec')
            if self.verify_checksum(buff_hex):
                #TODO: read the rest of the data
                print("It's time to read the data")
            else:
                print("handle this error")
            
    def verify_checksum(self, buff_hex):
        """According to the specs, the checksum is stored in the last 4 bytes
        """
        checksum = 0
        checksum_size_nibble = 2*self.checksum_size
        data = self.start_chars + buff_hex[:-checksum_size_nibble]
        for x in range(0, len(data), 2):
            checksum += int(data[x:x+2], 16)
        if checksum == int(buff_hex[-checksum_size_nibble:], 16):
            return True
        else:
            return False
    
