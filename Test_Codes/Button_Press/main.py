# This code will test a button press.
from machine import Pin

# Output
out_pin = Pin(1, Pin.OUT)   # Initialize the output Pin
out_pin.value(1)            # Set the output high

# Input
in_pin = Pin(0, Pin.IN, Pin.PULL_DOWN)  # Set the initial value to zero

# Intialize the LED
LED_pin = Pin(25, Pin.OUT)


def Button_press(pin_in, LED):
    while 1:
        if pin_in.value() == 1:
            print('Button is being pressed')
            LED.value(1)

        elif pin_in.value() == 0:
            print('No Press')
            LED.value(0)

Button_press(in_pin, LED_pin)