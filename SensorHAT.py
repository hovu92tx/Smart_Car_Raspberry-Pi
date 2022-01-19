import time
from i2c import I2C


class SensorHat:

    def __init__(self, address=0x04):
        self.i2c = I2C(address)
        self.i2c.write(address, 0x05)
        self.i2c.write(address, 0x06)
