# Main code for version 3
# Overhead Main codes that the Raspberry Pi will run
import Senior_Project  # Modulating the Code
import Phase_Offset  # Separating the Phase Offset Calculations
from machine import Pin  # Use for Calibration Human Interaction
from machine import ADC  # Read Voltage from AD8302
import utime  # Sleep time

# DICTIONARY "LIBRARY OF VARIABLES THAT WILL BE USED"
PA_main = {
    "ADC_Ch_0"      : 26,               # Phase Channel
    "ADC_Ch_1"      : 27,               # Magnitude Channel
#    "ADC_Ch_2"      : 28,
    "CAL_IN_PIN"    : 18,               # GPIO Pins used to configure for CALIBRATION
    "CAL_OUT_PIN"   : 20,
    "SL_CH_OUT_PIN" : 14,               # SLOPE CHANGE gpio to change PHASE OFFSET CALCULATION
    "SL_CH_IN_PIN"  : 15,
    "DEBOUNCE_SL"   : 1,                # Debounce sleeping time
    "FIRST_INDEX"   : 0,
    "PHASE_DEV"     : 0.05              # This will be used to handle the phase voltage as breathing room
}


# INTERRUPT PROTOCAL TO CHANGE VALUE OF "cal_prog" FLAG TO EXIT CALIBRATION
def inter_pin(cal_in_pin):              # Need variable that causes interrupt
    while cal_in_pin.value() == True:   # Wait for debounce sleep
        utime.sleep_us(1)               # Act as NOP
    utime.sleep(PA_main["DEBOUNCE_SL"]) # debounce sleep time

    print('From Calibration interrupt')
    global cal_prog                     # Make sure that we can write to the flag and recognise it
    cal_prog = 1                        # Set flag high for the calibration stage to be done

# CHANGING THE SLOPE
def slope_change_interrupt(sl_ch_in_pin):
    while sl_ch_in_pin.value() == True: # wait for user to take hand off button
        utime.sleep_us(1)               # NOP
    utime.sleep(PA_main["DEBOUNCE_SL"]) # Debounce sleep time

    global slope_dir
    if slope_dir == 1:
        LED.low()
        slope_dir = 0
    else:
        LED.high()
        slope_dir = 1


# CHECK IF THE MEASURED PHASE IS NEW MAX OR MIN
def phase_max_min_check(phase_mes):
    global ph_out_max
    global ph_out_min

    if ph_out_max < phase_mes:
        ph_out_max = phase_mes

    elif ph_out_min > phase_mes:
        ph_out_min = phase_mes


# INITIALIZING VARIABLES
cal_prog = 0                            # use to jump out of calibration process
ph_cal = 0                              # Calibrated Phase Recording
ph_mes = []                             # Measured Phase Recording
mag_cal = 0                             # Calibrated Magnitude Recording
mag_mes = []                            # Measured Magnitude Recording
slope_dir = 1                           # determining which slope is being used for the calculation
repeat = 0                              # what iteration on repeat
ph_out_max = 1.8                        # Data Sheet Maximum Phase Voltage Output for AD8302
ph_out_min = 0.3                        # Data Sheet Minimum Phase Voltage Output for AD8302


# INITIALIZE ON-BOARD LED FOR DEBUGGING
LED = Pin(25, Pin.OUT)                              # Set the LED to output
LED.low()                                           # Set the LED OFF


# INITIALIZE CALIBRATION PIN
cal_out_pin = Pin(PA_main["CAL_OUT_PIN"],
                  Pin.OUT)                          # Set Calibration Output Pin to Output
cal_out_pin.high()                                  # Set the value high

cal_in_pin = Pin(PA_main["CAL_IN_PIN"],
                 Pin.IN,                            # Set Calibration Input Pin to Input
                 Pin.PULL_DOWN)                     # Enable for logic 1: HIGH

cal_in_pin.irq(trigger= Pin.IRQ_RISING,             # Set Interrupt to only trigger on rising edge
               handler= inter_pin)                  # Set_up input pin as an interrupt and run "inter_pin" function


# INITIALIZE THE SLOPE CHANGING PIN
sl_ch_out_pin = Pin(PA_main["SL_CH_OUT_PIN"],       # Configure the Slope change Pin
                    Pin.OUT)                        # Set the direction of GPIO
sl_ch_out_pin.high()

sl_ch_in_pin = Pin(PA_main["SL_CH_IN_PIN"],         # Call Pin 15
                   Pin.IN,                          # Set GPIO direction as input
                   Pin.PULL_DOWN)                   # enable pull down resistor

sl_ch_in_pin.irq(trigger= Pin.IRQ_RISING,           # Enable this Pin as Interrupt
                 handler= slope_change_interrupt)   # Set the function protocal to "slope_change_interrupt" function

# INITIALIZE ADC PINS
ph_adc_pin = ADC(PA_main["ADC_Ch_1"])               # Init Phase ADC Pin
mag_adc_pin = ADC(PA_main["ADC_Ch_0"])              # Init Mag ADC Pin

# INDICATE INIT IS DONE: 'debugging'
print("Initialization is complete!")

# CALIBRATION PROCESS
print("Begin Calibration Process.\n Please place the Transmitter in the 12 o'clock position.")

# CAPTURE ZERO VALUES OF PHASE AND MAGNITUDE OUTPUT OF AD8302
while cal_prog == 0:                                # Keep capturing the zero value until user stops with button press
    ph_cal = ph_adc_pin.read_u16()
    mag_cal = mag_adc_pin.read_u16()

    ph_cal = Phase_Offset.volt_2_ph(Senior_Project.dig_2_ana(ph_cal),
                                    slope_dir)      # Convert the Digital voltage to Analog and into Phase offset [Degrees]

    # DISPLAY MEASUREMENT TO THE USER
    print('Initial Phase Offset: ', '{:2f}'.format(ph_cal))
    utime.sleep(1)                                  # sleep for 1 sec

# CALIBRATION DONE. INDICATE WITH LED
LED.high()                                          # Set value high
# Note for later: this should indicate that the slope value is 1

####################################################################
# The initial value of the phase measurement should be in Degrees
####################################################################


# CAPTURE 3 ADC MEASUREMENT FOR MAGNITUDE
for i in range(4):
    mag_mes.append(mag_adc_pin.read_u16())          # Do the same for magnitude pin
    # note for later: keep phase offset as voltage and not convert. Make sure the voltage is not the max or min

# CHECK IF THOSE MEASUREMENTS ARE THE MAX OR MIN
for i in range(len(ph_mes)):                                    # This should index through
    phase_max_min_check(ph_mes[i])                  # Test all the measurements if the phase max or min is exceeded


# FOREVER LOOP TO CALCULATE PHASE ARRAY AND DISPLAY TO USER
while True:
    # CAPTURE THE MEASUREMENT
    ph_mes = ph_adc_pin.read_u16()
    mag_mes.append(mag_adc_pin.read_u16())

    #




    # POP THE FIRST INDEX WHICH IS THE OLDEST DATA
    ph_mes.pop(PA_main["FIRST_INDEX"])
    mag_mes.pop(PA_main["FIRST_INDEX"])



    while True:
        print('done')
        utime.sleep(2)


    ################################################################
    # Version 2 code
#    ph_mes = ph_adc_pin.read_u16()  # Measurement in Digital Voltage
#    mag_mes = mag_adc_pin.read_u16()

    # CONVERT PHASE DIGITAL VALUE TO ANALOG
#    ph_mes = Senior_Project.dig_2_ana(ph_mes)  # Measurement in Analog Voltage

    # USE CONVERSION FORMULA FOR VOLTAGE -> PHASE
#    ph_mes = Senior_Project.volt_2_ph(ph_mes, 0)  # This should make ph_mes in degrees

    # CALCULATE PHASE DIFFERENCE FOR PHASE ARRAY CALC
#    ph_dif = abs(ph_cal - ph_mes)  # Calculate the phase
#    print('Phase Difference: ', ph_dif)
#    mag_dif = mag_cal - mag_mes
#    print('Magnitude Difference: ', mag_dif)

    # CALCULATE PHASE ARRAY
#    theta = Senior_Project.Phase_array_calc(ph_dif)
#    print('Theta: ', theta)
    # Display direction to user
#    heading = Senior_Project.dir_to_heading(theta, mag_dif)
#    Senior_Project.dis_head(heading)
#    utime.sleep(2)
