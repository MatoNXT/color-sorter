from pybricks.hubs import EV3Brick
from pybricks.ev3devices import TouchSensor, ColorSensor, Motor
from pybricks.iodevices import I2CDevice
from pybricks.parameters import Port, Direction, Color
from pybricks.tools import wait
from pybricks.media.ev3dev import SoundFile, ImageFile
import time

class EV3Manager:
    VOLTAGE_REGISTER = 0x41
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

    def __init__(self):
        self.keep_running = True
        try:
            self.ev3 = EV3Brick()
            self.touch = TouchSensor(Port.S4)
            self.color = ColorSensor(Port.S2)
            self.motor_belt = Motor(Port.A, Direction.COUNTERCLOCKWISE)
            self.nxtservo = I2CDevice(Port.S3, 0x58) # I2C device on Port S3 with NXTServo's address
        except Exception as e:
            self.handle_error("Master Initialization error", e)
            self.keep_running = False

    def handle_error(self, msg, error):
        print("[ERROR] {}: {}".format(msg, error))
        self.beep(frequency=200, duration=500)
        # self.keep_running = False

    def beep(self, frequency=3000, duration=200):
        try:
            self.ev3.speaker.beep(frequency=frequency, duration=duration)
        except Exception as e:
            self.handle_error("Beep error", e)

    def read_voltage(self):
        """Read and return the voltage from the nxtservo."""
        return self.nxtservo.read(self.VOLTAGE_REGISTER)

    def wait_for_start(self):
        print("Waiting for touch sensor to start...")
        while not self.touch_check(0):
            wait(10)
        self.beep(frequency=3000, duration=100)
        self.running = True

    def touch_check(self, where = -1):
        try:
            if self.touch.pressed():
                print("Pressed [{}]".format(where))
                return True
            return False
        except Exception as e:
            self.handle_error("Touch sensor error [{}] {}".format(where), e)
            return False

    def touch_check_exit(self, where = -1):
        if self.touch_check(where):
            print("Touch sensor pressed to stop.")
            self.keep_running = False

    def motor_belt_run(self, speed=150):
        try:
            print("Starting belt motor...")
            self.motor_belt.run(speed)
        except Exception as e:
            self.handle_error("Belt Motor run error", e)

    def motor_belt_stop(self):
        try:
            print("Stopping belt motor...")
            self.motor_belt.stop()
        except Exception as e:
            self.handle_error("Belt Motor stop error", e)

    def color_calculate_most_common(self, buffer):
        """Return the most frequently detected color and its count."""
        freq = {}
        for color in buffer:
            if color is not None:
                freq[color] = freq.get(color, 0) + 1
        if not freq:
            return None, 0
        common_color, count = max(freq.items(), key=lambda item: item[1])
        return common_color, count

    def color_get(self):
        try:
            return self.color.color()
        except Exception as e:
            self.handle_error("Color sensor error", e)
            return None

    def color_sensor_read(self):
        """
        Sample the color sensor until a stable reading is obtained or the belt is undetected.
        Returns a color or None if a stable color is not detected.
        """
        color_buffer = []
        belt_detected = 0
        while (
            self.keep_running
            and len(color_buffer) < self.config['color_sensor']['buffer_size']
            ):
            current_color = self.color_get()
            if current_color in self.config['color_sensor']['valid_colors']:
                color_buffer.append(current_color)
                belt_detected = 0  # reset if a valid color is read
            else:
                belt_detected += 1
            wait(self.config['color_sensor']['sample_interval_ms'])
            self.touch_check_exit(1)

        if len(color_buffer) >= self.config['color_sensor']['buffer_size']:
            common_color, count = self.color_calculate_most_common(color_buffer)
            if count / len(color_buffer) < self.config['color_sensor']['stability_threshold']:
                return None
            return common_color
        return None

    def servo_set(self, servo: int, position: int):
        """
        Set the specified servo to a given position.
        The position is adjusted for calibration and clamped between 500 and 2500.
        """
        try:
            position += self.config['servo'][servo]['calibration']
            position = max(500, min(2500, position))
            high_byte = (position >> 8) & 0xFF
            low_byte = position & 0xFF
            print("Set servo [{}] position to [{}]...".format(servo, position))
            self.nxtservo.write(self.config['servo'][servo]['nxt_register'], bytes([low_byte, high_byte]))
        except Exception as e:
            self.handle_error("Servo {} error".format(servo), e)

    def reset(self):
        """Reset all servos to their default positions."""
        print("Reset all servos to their default positions...")
        for servo in self.config['servo']:
            reset_pos = self.config['servo'][servo]['reset_position'] + self.config['servo'][servo]['calibration']
            self.servo_set(servo, reset_pos)
        wait(100)

    def turn_off(self):
        self.motor_belt_stop()
