# This code will flash the on-board LED to make sure that the board is functioning properly
from machine import Pin as pin      # Import the Pin functionality
import utime                        # Import to sleep

Blink_LED_lib = {
    "sleep_time"    : 2,            # make up the sleep time
    "LED_Pin"       : 25            # define the LED pin
}

# LED pin to turn on and off is Pin 25

LED_pin = Pin(Blink_LED_lib["LED_Pin"], pin.OUT)  # Initialize Pin
i = 1                       # Initialize Counter

while True:
    print('hi')
    if i == 1:
        LED_pin.value(1)    # turn on LED
        print('LED on asd')     # print to REPL Terminal
        i = 0               # reinitialize counter

    elif i == 0:
        LED_pin.value(0)    # Turn LED off
        print('LED off')    # Print to REPL Terminal
        i = i + 1           # increment counter

    utime.sleep(Blink_LED_lib["sleep_time"])    # sleep for the specified time in the Blink_LED_lib
