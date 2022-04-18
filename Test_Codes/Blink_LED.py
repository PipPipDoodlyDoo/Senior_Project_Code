# This will flash the on-board LED to make sure that the board is functioning properly
from machine import Pin
import utime

# LED pin to turn on and off is Pin 25

LED_pin = Pin(25, Pin.OUT)  # Initialize Pin
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

    utime.sleep(2)          # sleep for 2 seconds
