import serial
import struct
import time




class arduComm():

    def __init__(self):
    
        self.arduino = serial.Serial("COM3", timeout=1, baudrate=9600)
        time.sleep(3) # Arduino will be reset when serial port is opened, wait it to boot
    

    def calc_checksum(self,data):
        calculated_checksum = 0
        for byte in data:
            calculated_checksum ^= byte
        return calculated_checksum

    def read_packet(self):
        '''
        :return received data in the packet if read sucessfully, else return None
        '''
        # check start sequence
        if self.arduino.read() != b'\x10':
            return None

        if self.arduino.read() != b'\x02':
            return None

        payload_len = self.arduino.read()[0]
        if payload_len != 9:
            # could be other type of packet, but not implemented for now
            return None

        # we don't know if it is valid yet
        payload = self.arduino.read(payload_len)

        checksum = self.arduino.read()[0]
        if checksum != self.calc_checksum(payload):
            return None # checksum error

        # check end sequence
        if self.arduino.read() != b'\x10':
            return None
        if self.arduino.read() != b'\x03':
            return None    

        # yeah valid packet received
        return payload

    def send_packet(self,angles,speeds):
        tx = b'\x10\x02' # start sequence
        tx += struct.pack("<B", 9) # length of data
        packed_data = struct.pack("<BBBhhh", *angles, *speeds)
        tx += packed_data
        tx += struct.pack("<B", self.calc_checksum(packed_data))
        tx += b'\x10\x03' # end sequence
        print("Sending:", tx.hex())
        self.arduino.write(tx)

