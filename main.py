from machine import Pin
from utime import sleep

# make the interrupt function
def Interrupt_function(pin):           # keep this empty
    print('From Interrupt Func')
    global global_flag
    global_flag = 1



# Initialize the pins
LED_Pin = Pin(25, Pin.OUT)
in_p = Pin(0, Pin.IN, Pin.PULL_DOWN) # make sure that it stays down when not button press
out_p = Pin(1, Pin.OUT)

global_flag = 0

# Set the Output Pin high
LED_Pin.low()
out_p.high()

# Set the input pin as interrupt
in_p.irq(trigger=Pin.IRQ_HIGH_LEVEL, handler=Interrupt_function)

# Set up a repeating system
counter = 0
while True:
    print('Counter value = ', counter,'\nGlobal Flag = ',global_flag)
    counter += 1
    sleep(1)