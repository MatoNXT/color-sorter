#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.iodevices import I2CDevice
from pybricks.parameters import Port, Direction, Color
from pybricks.tools import wait
from pybricks.media.ev3dev import SoundFile, ImageFile

# Parameters
VOLTAGE_REGISTER = 0x41
BELT_SPEED = 150
config = {
    'color_sensor': {
        'buffer_size': 8,            # Number of measurements for color
        'belt_threshold': 15,         # Maximum allowed non-valid readings before giving up
        'stability_threshold': 0.7,   # Fraction of identical readings required for stability
        'sample_interval_ms': 20,     # Interval between color measurements in ms
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
            'calibration': 20
        },
        2: {
            'nxt_register': 0x44,
            'reset_position': 1500,
            'calibration': 20
        },
        3: {
            'nxt_register': 0x46,
            'reset_position': 1500,
            'calibration': -15
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
        Color.WHITE: {
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

# Initialize devices
nxtservo = I2CDevice(Port.S3, 0x58)  # I2C device on Port S3 with NXTServo's address
ev3_brick = EV3Brick()
ev3_touch = TouchSensor(Port.S1)
ev3_color = ColorSensor(Port.S2)
ev3_motor_belt = Motor(Port.A, Direction.COUNTERCLOCKWISE)

def get_most_common_color(buffer):
    """Return the most frequently detected color and its count."""
    freq = {}
    for color in buffer:
        if color is not None:
            freq[color] = freq.get(color, 0) + 1
    if not freq:
        return None, 0
    common_color, count = max(freq.items(), key=lambda item: item[1])
    return common_color, count

def get_sensor_color():
    """
    Sample the color sensor until a stable reading is obtained or the belt is undetected.
    Returns a color or None if a stable color is not detected.
    """
    color_buffer = []
    belt_detected = 0
    while (len(color_buffer) < config['color_sensor']['buffer_size']
           #and belt_detected < config['color_sensor']['belt_threshold']
          ):
        current_color = ev3_color.color()
        if current_color in config['color_sensor']['valid_colors']:
            color_buffer.append(current_color)
            belt_detected = 0  # reset if a valid color is read
        else:
            belt_detected += 1
        wait(config['color_sensor']['sample_interval_ms'])
    if len(color_buffer) >= config['color_sensor']['buffer_size']:
        common_color, count = get_most_common_color(color_buffer)
        if count / len(color_buffer) < config['color_sensor']['stability_threshold']:
            return None
        return common_color
    return None

def servo_reset():
    """Reset all servos to their default positions."""
    for servo in config['servo']:
        reset_pos = config['servo'][servo]['reset_position'] + config['servo'][servo]['calibration']
        nxtservo_set_servo(servo, reset_pos)
    wait(100)

def nxtservo_set_servo(servo: int, position: int):
    """
    Set the specified servo to a given position.
    The position is adjusted for calibration and clamped between 500 and 2500.
    """
    position += config['servo'][servo]['calibration']
    position = max(500, min(2500, position))
    high_byte = (position >> 8) & 0xFF
    low_byte = position & 0xFF
    nxtservo.write(config['servo'][servo]['nxt_register'], bytes([low_byte, high_byte]))

def read_voltage():
    """Read and return the voltage from the nxtservo."""
    return nxtservo.read(VOLTAGE_REGISTER)

def perform_sort_action(color):
    """Perform the sort action based on the detected color."""
    action = config['sort_action'][color]
    servo_num = action['servo']
    # Beep with the color-specific frequency
    ev3_brick.speaker.beep(frequency=action['beep'], duration=100)
    servo_reset()
    # Open the servo to let the object pass to the designated bin
    nxtservo_set_servo(servo_num, action['open'])
    wait(action['wait_ms'])
    ev3_brick.speaker.beep(frequency=300, duration=100)
    # Close the servo after sorting
    nxtservo_set_servo(servo_num, action['close'])

def main():
    print("Ready...")
    # Wait for the touch sensor to be pressed to start
    while not ev3_touch.pressed():
        wait(10)
    ev3_brick.speaker.beep(frequency=3000, duration=100)
    servo_reset()
    # Start the belt motor
    ev3_motor_belt.run(BELT_SPEED)

    while True:
        detected_color = get_sensor_color()
        if detected_color is not None:
            perform_sort_action(detected_color)
        if ev3_touch.pressed():
            break

    # Stop the belt and reset servos at the end
    ev3_motor_belt.stop()
    servo_reset()

if __name__ == '__main__':
    main()