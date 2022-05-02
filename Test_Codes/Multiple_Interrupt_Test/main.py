# This code is to test multiple pins acting as interrupts
from machine import Pin
import utime

lib = {
    "OUT_PIN1": 18,
    "IN_PIN1": 20,
    "OUT_PIN2": 14,
    "IN_PIN2": 15,
    "OUT_PIN3": 10,
    "IN_PIN3": 11
}


def int_1(in_1):
    print('In Interrupt 1')
    while in_1.value() == True:
        utime.sleep_us(1)
    global counter_1
    counter_1 += 1


def int_2(in_2):
    print('In Interrupt 2')
    global counter_2
    while in_2.value() == True:
        utime.sleep_us(1)
    counter_2 += 1



def int_3(in_3):
    print('In Interrupt 3')
    while in_3.value() == True:
        utime.sleep_us(1)
    global counter_3
    counter_3 += 1


# INITIALIZE VARIABLES
counter_1 = 0
counter_2 = 0
counter_3 = 0
i = 0

# CONFIGURE OUTPUT PINS
out_1 = Pin(lib["OUT_PIN1"], Pin.OUT)
out_1.high()
out_2 = Pin(lib["OUT_PIN2"], Pin.OUT)
out_2.high()
out_3 = Pin(lib["OUT_PIN3"], Pin.OUT)
out_3.high()

# CONFIGURE INPUT PINS
in_1 = Pin(lib["IN_PIN1"], Pin.IN, Pin.PULL_DOWN)
in_1.irq(trigger=Pin.IRQ_RISING, handler=int_1)

in_2 = Pin(lib["IN_PIN2"], Pin.IN, Pin.PULL_DOWN)
in_2.irq(trigger=Pin.IRQ_RISING, handler=int_2)

in_3 = Pin(lib["IN_PIN3"], Pin.IN, Pin.PULL_DOWN)
in_3.irq(trigger=Pin.IRQ_RISING, handler=int_3)

while True:
    print('\nCounter 1: ', counter_1)
    print('Counter 2: ', counter_2)
    print('Counter 3: ', counter_3)
    print('done, ', i)
    i += 1
    utime.sleep(2)
