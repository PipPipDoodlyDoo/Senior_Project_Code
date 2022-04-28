from machine import Pin
from utime import sleep

PIN_INT = {
    "IN_PIN"    : 18,
    "OUT_PIN"   : 20
}
# make the interrupt function
def Interrupt_function(in_p):           # keep this empty
    print('From Interrupt Func')
    global LED_Pin
    print('penis')                      # By beto
    LED_Pin.high()
    global global_flag
    global_flag = 1



# Initialize the pins
LED_Pin = Pin(25, Pin.OUT)
in_p = Pin(PIN_INT["IN_PIN"], Pin.IN, Pin.PULL_DOWN) # make sure that it stays down when not button press
out_p = Pin(PIN_INT["OUT_PIN"], Pin.OUT)

global_flag = 0

# Set the Output Pin high
LED_Pin.low()
out_p.high()

# Set the input pin as interrupt
in_p.irq(trigger=Pin.IRQ_RISING, handler=Interrupt_function)

# Set up a repeating system
counter = 0
while global_flag == 0:
    print('Counter value = ', counter,'\nGlobal Flag = ',global_flag)
    counter += 1
    sleep(1)

while True:
    print('done')
    utime.sleep(2)