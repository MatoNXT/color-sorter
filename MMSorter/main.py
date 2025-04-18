#!/usr/bin/env pybricks-micropython
from ev3_manager import EV3Manager
from pybricks.tools import wait

# Initialize color sorter
color_sorter = EV3Manager()

def perform_sort_action(color):
    """Perform the sort action based on the detected color."""
    action = color_sorter.config['sort_action'][color]
    servo_num = action['servo']
    # Beep with the color-specific frequency
    color_sorter.beep(frequency=action['beep'], duration=100)
    color_sorter.reset()
    # Open the servo to let the object pass to the designated bin
    color_sorter.servo_set(servo_num, action['open'])
    wait(action['wait_ms'])
    color_sorter.beep(frequency=300, duration=100)
    # Close the servo after sorting
    color_sorter.servo_set(servo_num, action['close'])

def main():
    if color_sorter.keep_running: # check if initialization was ok
        print("Ready...")
        color_sorter.wait_for_start()
        color_sorter.beep()
        color_sorter.reset()
        color_sorter.motor_belt_run()

        print("Press touch sensor to finish...")
        while color_sorter.keep_running:
            detected_color = color_sorter.color_sensor_read()
            if detected_color is not None:
                perform_sort_action(detected_color)
            wait(10) # to lower CPU load

        # Stop the belt and reset servos at the end
        color_sorter.turn_off()
        print("...End")

if __name__ == '__main__':
    main()