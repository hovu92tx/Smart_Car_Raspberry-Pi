#!/usr/bin/python

import time
import math
from i2c import I2C


# ============================================================================
# Raspi PCA9685 16-Channel PWM Servo Driver
# ============================================================================

class PWM:
    # Registers/etc.
    __MODE1 = 0x00
    __MODE2 = 0x01
    __PRESCALE = 0xFE
    __LED0_ON_L = 0x06
    __LED0_ON_H = 0x07
    __LED0_OFF_L = 0x08
    __LED0_OFF_H = 0x09
    __ALL_LED_ON_L = 0xFA
    __ALL_LED_ON_H = 0xFB
    __ALL_LED_OFF_L = 0xFC
    __ALL_LED_OFF_H = 0xFD

    # Bits
    __RESTART = 0x80
    __SLEEP = 0x10
    __ALLCALL = 0x01
    __INVRT = 0x10
    __OUTDRV = 0x04

    def __init__(self, address=0x40):
        self.i2c = I2C(address)
        self.address = address
        self.setAllPWM(0, 0)
        self.i2c.write(self.__MODE2, self.__OUTDRV)
        self.i2c.write(self.__MODE1, self.__ALLCALL)
        time.sleep(0.005)  # wait for oscillator

        mode1 = self.i2c.readU8(self.__MODE1)
        mode1 = mode1 & ~self.__SLEEP  # wake up (reset sleep)
        self.i2c.write(self.__MODE1, mode1)
        time.sleep(0.005)  # wait for oscillator

    def setPWMFreq(self, freq):
        """Sets the PWM frequency"""
        prescaleval = 25000000.0  # 25MHz
        prescaleval /= 4096.0  # 12-bit
        prescaleval /= float(freq)
        prescaleval -= 1.0
        prescale = math.floor(prescaleval + 0.5)

        oldmode = self.i2c.readU8(self.__MODE1)
        newmode = (oldmode & 0x7F) | 0x10  # sleep
        self.i2c.write(self.__MODE1, newmode)  # go to sleep
        self.i2c.write(self.__PRESCALE, int(math.floor(prescale)))
        self.i2c.write(self.__MODE1, oldmode)
        time.sleep(0.005)
        self.i2c.write(self.__MODE1, oldmode | 0x80)

    def setPWM(self, channel, on, off):
        """Sets a single PWM channel"""
        self.i2c.write(self.__LED0_ON_L + 4 * channel, on & 0xFF)
        self.i2c.write(self.__LED0_ON_H + 4 * channel, on >> 8)
        self.i2c.write(self.__LED0_OFF_L + 4 * channel, off & 0xFF)
        self.i2c.write(self.__LED0_OFF_H + 4 * channel, off >> 8)

    def setAllPWM(self, on, off):
        """Sets a all PWM channels"""
        self.i2c.write(self.__ALL_LED_ON_L, on & 0xFF)
        self.i2c.write(self.__ALL_LED_ON_H, on >> 8)
        self.i2c.write(self.__ALL_LED_OFF_L, off & 0xFF)
        self.i2c.write(self.__ALL_LED_OFF_H, off >> 8)
