#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile



# Sensor and Motor Setup
sensor = ColorSensor(Port.S2)
belt_motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)

# Parameters
BUFFER_SIZE = 10
STABILITY_THRESHOLD = 0.7
SAMPLE_INTERVAL_MS = 50
REFLECTION_THRESHOLD = 15
VALID_COLORS = {Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW, Color.BROWN, Color.WHITE}

# Start the belt
belt_motor.run(100)

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
    # if sensor.reflection() < REFLECTION_THRESHOLD:
    #     color_buffer.clear()
    #     return None

    color_buffer.clear()
    while (len(color_buffer) < BUFFER_SIZE):
        current_color = sensor.color()
        if (current_color in VALID_COLORS):
            color_buffer.append(current_color)

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
        wait(1000)
    else:
        print("Waiting for valid color...")

    wait(SAMPLE_INTERVAL_MS)

    #!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.iodevices import I2CDevice
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from time import sleep

#Initialize the EV3
nxtservo = I2CDevice(Port.S3, 0x58)                    # Create an  I2C device on Port 3 with NXTServo's 7-bit address (0x58)
ev3_brick = EV3Brick()
ev3_touch = TouchSensor(Port.S1)
ev3_color = ColorSensor(Port.S4)
ev3_motor_belt = Motor(Port.A, Direction.COUNTERCLOCKWISE)
VOLTAGE = 0x41
col = None  
col1 = None
beltspeed = 150
s1_cal = 50

def servo_reset():
    nxtservo_set_servo(1, 1500)
    nxtservo_set_servo(2, 1500)
    nxtservo_set_servo(3, 1500)

def nxtservo_set_servo(servo: int, position: int):
    if position < 500:
        position = 500 
    if position > 2500:
        position = 2500

    high_byte = (position >> 8) & 0xFF
    low_byte = position & 0xFF

    # Register for Servo 1 starts at 0x42
    register = 0x40 + servo*2
    nxtservo.write(register,bytes([low_byte, high_byte]))

def read_voltage():
    volts = nxtservo.read(VOLTAGE)
    return volts

print("Ready...")



# ev3.light.off()
# nxtservo_set_servo(1, 500)
# nxtservo_set_servo(2, 500)
#sleep(2)/

while (True):
    if ev3_touch.pressed(): break 
ev3_brick.speaker.beep(frequency=3000, duration=100)
servo_reset()
ev3_brick.speaker.set_speech_options(language= 'de', voice='f2', pitch=1)
ev3_brick.speaker.say("Acthung starting belt")
ev3_motor_belt.run(beltspeed)


while (True):
    col = ev3_color.color()
    if (col == Color.RED):
        ev3_brick.speaker.beep(frequency=500, duration=100)
        servo_reset()
        nxtservo_set_servo(3, 2000)
        sleep(4.2)
        ev3_brick.speaker.beep(frequency=300, duration=100)  
        nxtservo_set_servo(3, 1500)

    elif (col == Color.BLUE):
        ev3_brick.speaker.beep(frequency=600, duration=100)
        servo_reset()
        nxtservo_set_servo(1, 2000)
        sleep(2.5)
        ev3_brick.speaker.beep(frequency=300, duration=100)  
        nxtservo_set_servo(1, 1500)

    elif (col == Color.GREEN):
        ev3_brick.speaker.beep(frequency=700, duration=100)
        servo_reset()
        nxtservo_set_servo(2, 2000)
        sleep(3)
        ev3_brick.speaker.beep(frequency=350, duration=100)  
        nxtservo_set_servo(2, 1500)

    elif (col == Color.YELLOW):
        ev3_brick.speaker.beep(frequency=800, duration=100)       
        servo_reset()
        nxtservo_set_servo(1, 1000)
        sleep(2.5)
        ev3_brick.speaker.beep(frequency=400, duration=100)  
        servo_reset()

    elif (col == Color.WHITE):
        ev3_brick.speaker.beep(frequency=900, duration=100)
        servo_reset()
        nxtservo_set_servo(2, 500)

    elif (col == Color.BROWN):
        ev3_brick.speaker.beep(frequency=1000, duration=100)  
        servo_reset()
        nxtservo_set_servo(3, 1000)
        sleep(4.2)
        ev3_brick.speaker.beep(frequency=500, duration=100)  
        nxtservo_set_servo(3, 1500)


    # if (col != col1):
    #     print(col)
    #     col1 = col
    #     (r,g,b) = ev3_color.rgb()
    #     print(r)
    #     print(g)
    #     print(b)

    if ev3_touch.pressed(): break
#end of while
     
servo_reset()
    