# Overhead Main codes that the Raspberry Pi will run
import Senior_Project                                                       # Modulating the Code
from machine import Pin                                                     # Use for Calibration Human Interaction
from machine import ADC                                                     # Read Voltage from AD8302
import utime                                                                # Sleep time

# DICTIONARY "LIBRARY OF VARIABLES THAT WILL BE USED"
PA_main = {
    "ADC_Ch_0"      : 26,                                                   # Phase Channel
    "ADC_Ch_1"      : 27,                                                   # Magnitude Channel
    "ADC_Ch_2"      : 28,
    "IN_PIN"        : 18,
    "OUT_PIN"       : 20
    # Reference Pin
}

# INTERRUPT FUNCTION TRIGGERED BY THE 'in_pin'
def inter_pin(in_pin):                                                      # Need variable that causes interrupt
    print('from interrupt')
    global cal_prog                                                         # Make sure that we can write to the flag and recognise it
    cal_prog = 1                                                            # Set flag high for the calibration stage to be done

# INIT VARIABLES
cal_prog = 0                                                                # use to jump out of calibration process
ph_cal   = 0                                                                # Calibrated Phase Recording
ph_mes   = 0                                                                # Measured Phase Recording
mag_cal  = 0                                                                # Calibrated Magnitude Recording
mag_mes  = 0                                                                # Measured Magnitude Recording

# INIT ON-BOARD LED FOR DEBUGGING
LED = Pin(25, Pin.OUT)                                                      # Set the LED to output
LED.low()                                                                   # Set the LED OFF

# INIT OUTPUT GPIO PIN
out_pin = Pin(PA_main["OUT_PIN"], Pin.OUT)                                                   # Set Pin 1 to Output
out_pin.high()                                                              # Put the value high

# INIT INPUT GPIO PIN
in_pin = Pin(PA_main["IN_PIN"], Pin.IN, Pin.PULL_DOWN)                                      # Set the initial value to zero
in_pin.irq(trigger=Pin.IRQ_RISING, handler= inter_pin)                      # Set_up input pin as an interupt and run "inter_pin" function

# INIT ADC PINS
Ph_adc_pin = ADC(Pin(PA_main["ADC_Ch_1"]))                                  # Init Phase ADC Pin
Mag_adc_pin = ADC(Pin(PA_main["ADC_Ch_0"]))                                 # Init Mag ADC Pin

# INDICATE INIT IS DONE: 'debugging
print("Initialization is complete!")

# CALIBRATION PROCESS
print("Begin Calibration Process.\n Please place the Transmitter in the 12 o'click position.")

# CAPTURE ZERO VALUES OF PHASE AND MAGNITUDE OUTPUT OF AD8302
while (cal_prog == 0):                                                        # Keep capturing the zero value until user stops with button press
    ph_cal  = Ph_adc_pin.read_u16()
    mag_cal = Mag_adc_pin.read_u16()

    ph_cal  = Senior_Project.volt_2_ph(Senior_Project.dig_2_ana(ph_cal), 1) # Convert the Digital voltage to Analog and into Phase offset [Degrees]

    # DISPLAY MEASUREMENT TO THE USER
    print('Initial Phase Offset: ', '{:2f}'.format(ph_cal))
    print('Calibration flag: ', cal_prog)
    utime.sleep(1)                                                          # sleep for 1 sec

# MIGHT CHANGE PHASE CAL VALUE TO DEG OFFSET
####################################################################
# The initial value of the phase measurement should be in Degrees
####################################################################



# FOREVER LOOP TO CALCULATE PHASE ARRAY AND DISPLAY TO USER
while True:
    # CAPTURE ADC MEAS
    ph_mes  = Ph_adc_pin.read_u16()                                         # Measurement in Digital Voltage
    mag_mes = Mag_adc_pin.read_u16()

    # CONVERT PHASE DIGITAL VALUE TO ANALOG
    ph_mes = Senior_Project.dig_2_ana(ph_mes)                               # Measurement in Analog Voltage

    # USE CONVERSION FORMULA FOR VOLTAGE -> PHASE
    ph_mes = Senior_Project.volt_2_ph(ph_mes, 0)                            # This should make ph_mes in degrees

    # CALCULATE PHASE DIFFERENCE FOR PHASE ARRAY CALC
    ph_dif  = abs(ph_cal - ph_mes)                                           # Calculate the phase
    print('Phase Difference: ', ph_dif)
    mag_dif = mag_cal - mag_mes
    print('Magnitude Difference: ',mag_dif)

    # CALCULATE PHASE ARRAY
    theta = Senior_Project.Phase_array_calc(ph_dif)
    print('Theta: ', theta)
    # Display direction to user
    heading = Senior_Project.dir_to_heading(theta, mag_dif)
    Senior_Project.dis_head(heading)
    utime.sleep(2)