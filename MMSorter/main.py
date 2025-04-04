#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.iodevices import I2CDevice
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from time import sleep

# Parameters
VOLTAGE_REGISTER = 0x41
BELT_SPEED = 150
params = {
    'color_sensor': {
        'buffer_size': 10,            # Number of measurements for color
        'belt_threshold': 15,         # Number of measurements to detect the belt
        'stability_threshold': 0.7,   # Percentage of when color is declared stable
        'sample_interval_ms': 50,     # Interval between color measurements
        'reflection_threshold': 15,   # Reflection threshold to detect the object on belt
        'valid_colors': {
            Color.RED,
            Color.GREEN,
            Color.BLUE,
            Color.YELLOW,
            Color.BROWN,
            Color.WHITE
        }
    },
    'servo': {
        1: {
            'nxt_register': 0x42,
            'reset_position': 1500,
            'calibration': 0
        },
        2: {
            'nxt_register': 0x44,
            'reset_position': 1500,
            'calibration': 0
        },
        3: {
            'nxt_register': 0x46,
            'reset_position': 1500,
            'calibration': 0
        }
    },
    'sort_action': {
        Color.BLUE: {
            'servo': 1,
            'open': 2000,
            'close': 1500,
            'beep': 600,
            'wait_ms': 2500
        },
        Color.YELLOW: {
            'servo': 1,
            'open': 1000,
            'close': 1500,
            'beep': 800,
            'wait_ms': 2500
        },
        Color.GREEN: {
            'servo': 2,
            'open': 2000,
            'close': 1500,
            'beep': 700,
            'wait_ms': 3000
        },
        Color.WHITE : {
            'servo': 2,
            'open': 1000,
            'close': 1500,
            'beep': 900,
            'wait_ms': 3000
        },
        Color.RED: {
            'servo': 3,
            'open': 2000,
            'close': 1500,
            'beep': 500,
            'wait_ms': 4200
        },
        Color.BROWN: {
            'servo': 3,
            'open': 1000,
            'close': 1500,
            'beep': 1000,
            'wait_ms': 4200
        }
    }
}
#Initialize the EV3
nxtservo = I2CDevice(Port.S3, 0x58) # Create an I2C device on Port 3 with NXTServo's 7-bit address (0x58)
ev3_brick = EV3Brick()
ev3_touch = TouchSensor(Port.S1)
ev3_color = ColorSensor(Port.S4)
ev3_color_buffer = []
ev3_motor_belt = Motor(Port.A, Direction.COUNTERCLOCKWISE)

#
##
### Functions
##
#
def get_color(buffer):
    freq = {}
    for color in buffer:
        if color is not None:
            freq[color] = freq.get(color, 0) + 1
    if not freq:
        return None, 0
    get_color = max(freq.items(), key=lambda x: x[1])
    return get_color  # (color, count)

def get_sensor_color():
    ev3_color_buffer.clear()
    belt_detected = 0
    while (len(ev3_color_buffer) < params['color_sensor']['buffer_size'] and belt_detected < params['color_sensor']['belt_threshold']):
        current_color = ev3_color.color()
        if (current_color in params['color_sensor']['valid_colors']):
            ev3_color_buffer.append(current_color)
            belt_detected = 0
        else:
            belt_detected =+ 1
    color = None
    if (len(ev3_color_buffer) >= params['color_sensor']['buffer_size']):
        color, count = get_color(ev3_color_buffer)
        if count / len(ev3_color_buffer) < params['color_sensor']['stability_threshold']:
          color = None
    return color

def servo_reset():
    for i in range(1, 3):
        nxtservo_set_servo(i, params['servo'][i]['reset_positioin']+params['servo'][i]['calibration'])
    wait(100)

def nxtservo_set_servo(servo: int, position: int):
    position = position + params['servo'][servo]['calibration']
    if position < 500: position = 500
    if position > 2500: position = 2500
    high_byte = (position >> 8) & 0xFF
    low_byte = position & 0xFF
    nxtservo.write(params['servo'][servo]['nxt_register'],bytes([low_byte, high_byte]))

def read_voltage():
    volts = nxtservo.read(VOLTAGE_REGISTER)
    return volts

#
##
### Main program
##
#
print("Ready...")
# ev3.light.off()

while (True):
    if ev3_touch.pressed(): break

ev3_brick.speaker.beep(frequency=3000, duration=100)
servo_reset()
# ev3_brick.speaker.set_speech_options(language= 'de', voice='f2', pitch=1)
# ev3_brick.speaker.say("Acthung starting belt")
ev3_motor_belt.run(BELT_SPEED)

while (True):
    col = get_sensor_color()
    if col is not None:
        ev3_brick.speaker.beep(frequency=params['sort_action'][col]['beep'], duration=100)
        servo_reset()
        nxtservo_set_servo(params['sort_action'][col]['servo'], params['sort_action'][col]['open'])
        wait(nxtservo_set_servo(params['sort_action'][col]['servo'], params['sort_action'][col]['wait_ms']))
        ev3_brick.speaker.beep(frequency=300, duration=100)
        nxtservo_set_servo(params['sort_action'][col]['servo'], params['sort_action'][col]['close'])

    if ev3_touch.pressed(): break

#end of while
servo_reset()
