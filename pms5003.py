import serial
import time
import sys
from struct import *
import codecs
import yaml


class pms5003():
    """This class handles the serial connection between the PMS5003 and a Raspberry PI
    """
    
    def __init__(self, baudrate=9600, device='/dev/ttyS0'):
        self.endian = sys.byteorder
        self.baudrate = baudrate
        self.device = device
        self.data = dict()
        with open('pms5003_transport.yml', 'r') as fp:
            self.frame = yaml.load(fp)

            
    def conn_serial_port(self):
        """Define the connection with the serial port"""
        self.serial = serial.Serial(self.device, baudrate=self.baudrate)

        
    def find_start_chars(self):
        # TODO: Add a timeout, if nothing is read, report an error
        while True:
            buff = self.serial.read(self.frame['fields']['start_char'][1])
            buff_hex = codecs.encode(buff, 'hex_codec')
            if buff_hex == hex(self.frame['start_char']):
                return True

            
    def read_frame(self, data_size=30):
        if self.find_start_chars:
            buff = self.serial.read(data_size)
            buff_hex = hex(self.frame['start_char']) + codecs.encode(buff, 'hex_codec')
            if self.verify_checksum(buff_hex):
                self.get_data(buff_hex)
            else:
                print("handle this error")

                
    def verify_checksum(self, buff_hex):
        """According to the specs, the checksum is stored in the last 4 bytes
        """
        checksum = 0
        checksum_size_nibble = 2*self.frame['fields']['checksum'][1]
        data = buff_hex[:-checksum_size_nibble]
        for x in range(0, len(data), 2):
            checksum += int(data[x:x+2], 16)
        if checksum == int(buff_hex[-checksum_size_nibble:], 16):
            return True
        else:
            return False

        
    def get_data(self, buff_hex):
        no_data = ['start_char', 'frame_length', 'reserved', 'checksum']
        for k,v in self.frame['fields'].items():
            if k not in no_data:
                # Start and end points need to be in nibbles
                st = 2*v[0]
                nd = st + 2*v[1]
                self.data[k] = int(buff_hex[st:nd], 16)
            
        
        
