#!/usr/bin/python
import smbus


# ===========================================================================
#I2C Class
# ===========================================================================

class I2C(object):

    def __init__(self, address):
        self.address = address
        self.bus = smbus.SMBus(1)

    def write(self, reg, value):
        """Writes an 8-bit value to the specified register/address"""
        try:
            self.bus.write_byte_data(self.address, reg, value)
        except IOError:
            pass

    def readU8(self, reg):
        """Read an unsigned byte from the I2C device"""
        try:
            result = self.bus.read_byte_data(self.address, reg)
            return result
        except IOError:
            pass

    def readS8(self, reg):
        """Reads a signed byte from the I2C device"""
        try:
            result = self.bus.read_byte_data(self.address, reg)
            if result > 127:
                result -= 256
            return result
        except IOError:
            pass
