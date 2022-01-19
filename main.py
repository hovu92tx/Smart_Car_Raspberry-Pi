# 07-16-2021. Author VU HO
import time
import random
from pynput import keyboard
from ultrasonic import Ultrasonic
from MotorHAT import MotorHAT

ultrasonic = Ultrasonic()
list_of_direction = []
distances = []
START_RADIUS = 65
END_RADIUS = 115
mh = MotorHAT(addr=0x6f)
motor_1 = mh.getMotor(1)
motor_2 = mh.getMotor(2)
motor_1.setSpeed(250)
motor_2.setSpeed(250)


def tank_run(command):
    motor_right = motor_1
    motor_left = motor_2
    if command == 'right':
        motor_right.run(MotorHAT.BACKWARD)
        motor_left.run(MotorHAT.FORWARD)
    elif command == 'left':
        motor_right.run(MotorHAT.BACKWARD)
        motor_left.run(MotorHAT.FORWARD)
    elif command == 'forward':
        motor_right.run(MotorHAT.FORWARD)
        motor_left.run(MotorHAT.FORWARD)
    elif command == 'backward':
        motor_right.run(MotorHAT.BACKWARD)
        motor_left.run(MotorHAT.BACKWARD)
    else:
        self.motor_right.run(MotorHAT.RELEASE)
        self.motor_left.run(MotorHAT.RELEASE)


def autorun():
    try:
        while True:
            for angle in range(START_RADIUS, END_RADIUS, 20):

                distance = ultrasonic.distance()
                if distance > 30:

                    print('going forward')
                else:

                    if ultrasonic.distance() > 30:
                        list_of_direction.append('right')
                    else:
                        pass

                    if ultrasonic.distance() > 30:
                        list_of_direction.append('mid_right')
                    else:
                        pass

                    if ultrasonic.distance() > 30:
                        list_of_direction.append('mid_left')
                    else:
                        pass

                    if ultrasonic.distance() > 30:
                        list_of_direction.append('left')
                    else:
                        pass
                    if len(list_of_direction) != 0:
                        choice = random.choice(list_of_direction)
                        if choice == 'right':
                            print('turning right')

                            list_of_direction.clear()
                        elif choice == 'mid_right':
                            print('turning mid right')

                            list_of_direction.clear()
                        elif choice == 'mid_left':
                            print('turning mid left')

                            list_of_direction.clear()
                        else:
                            print('turning left')

                            list_of_direction.clear()
                    else:
                        print('turning around')
    except KeyboardInterrupt:
        print('Robot is stopped!')


def robot_control():
    try:
        with keyboard.Events() as events:
            for event in events:
                if type(event) == keyboard.Events.Press:
                    if event.key == keyboard.Key.up:
                        print('going forward')
                        tank_run('forward')
                    elif event.key == keyboard.Key.down:
                        print('going backward')
                        tank_run('backward')
                    elif event.key == keyboard.Key.left:
                        print('going left')
                        tank_run('left')
                    elif event.key == keyboard.Key.right:
                        print('going right')
                        tank_run('right')
                    elif event.key == keyboard.Key.esc:
                        print('Stop manual mode!')
                        tank_run('stop')
                        main_menu()
                elif type(event) == keyboard.Events.Release:
                    tank_run('stop')

    except KeyboardInterrupt:
        print('Stop manual mode!')


def main_menu():
    try:
        while True:
            print('Chose mode: 1: manual control, 2: self-control, q: quit')
            cmd = input('Run: ')
            if cmd == '1':
                print('press Ctrl+C to end mode')
                robot_control()
            elif cmd == '2':
                print('press Ctrl+C to end mode')
                autorun()
            elif cmd == 'q':

                break
            else:
                print('Wrong command. Please choose again!')
    finally:
        print('Program closed!')


if __name__ == "__main__":
    main_menu()
