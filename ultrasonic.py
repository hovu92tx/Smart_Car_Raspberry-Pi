import RPi.GPIO as gpio
import time


class Ultrasonic:

    def __init__(self):
        self.trigger = 23
        self.echo = 24
        gpio.setmode(gpio.BCM)
        gpio.setup(self.trigger, gpio.OUT)
        gpio.setup(self.echo, gpio.IN)

    def enable_ultrasonic(self):
        gpio.setmode(gpio.BCM)
        gpio.setup(self.trigger, gpio.OUT)
        gpio.setup(self.echo, gpio.IN)

    def distance(self):
        gpio.output(self.trigger, True)
        time.sleep(0.00001)
        gpio.output(self.trigger, False)
        stop_time = time.time()
        start_time = time.time()
        while gpio.input(self.echo) == 0:
            start_time = time.time()

        while gpio.input(self.echo) == 1:
            stop_time = time.time()

        total_time = stop_time - start_time

        dist = (total_time * 34300) / 2
        result = round(dist, 2)
        return result
