#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from collections import deque


# Sensor and Motor Setup
sensor = ColorSensor(Port.S2)
belt_motor = Motor(Port.A)

# Parameters
BUFFER_SIZE = 8
STABILITY_THRESHOLD = 0.7
SAMPLE_INTERVAL_MS = 50
REFLECTION_THRESHOLD = 15
VALID_COLORS = {Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW, Color.BROWN, Color.WHITE}

# Start the belt
belt_motor.run(200)

# Initialize buffer as a list
color_buffer = []

# Manual mode function (replaces Counter)
def most_common_color(buffer):
    freq = {}
    for color in buffer:
        if color is not None:
            freq[color] = freq.get(color, 0) + 1
    if not freq:
        return None, 0
    most_common = max(freq.items(), key=lambda x: x[1])
    return most_common  # (color, count)

def get_stable_color():
    # Object presence check via reflection
    if sensor.reflection() < REFLECTION_THRESHOLD:
        color_buffer.clear()
        return None

    current_color = sensor.color()

    # Ignore black (belt) and unknown colors
    if current_color == Color.BLACK or current_color not in VALID_COLORS:
        return None

    # Add to buffer
    color_buffer.append(current_color)

    # Keep buffer at fixed size
    if len(color_buffer) > BUFFER_SIZE:
        color_buffer.pop(0)

    # Wait for enough samples
    if len(color_buffer) < BUFFER_SIZE:
        return None

    # Get the most common color
    color, count = most_common_color(color_buffer)

    if count / len(color_buffer) >= STABILITY_THRESHOLD:
        return color
    else:
        return None

# Main loop
while True:
    stable_color = get_stable_color()

    if stable_color:
        print("Stable color detected:", stable_color)
    else:
        print("Waiting for valid color...")

    wait(SAMPLE_INTERVAL_MS)