# Main code for version 3
# Overhead Main codes that the Raspberry Pi will run
import Senior_Project  # Modulating the Code
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
    "FIRST_INDEX"   : 0,                # Don't know if we need this
    "PHASE_DEV"     : 0.05,             # Phase Voltage Deviation/Buffer
    "HIGH_DEV"      : 0,                #
    "LOW_DEV"       : 1,                 # Indicate that we are in lower deviation
    "RISING_SLOPE"  : 0,
    "FALLING_SLOPE" : 1,
    "ERROR"         : 10                # some random value to distinguish error
}


############################################################################################
# Interrupts
############################################################################################

# INTERRUPT PROTOCOL TO CHANGE VALUE OF "cal_prog" FLAG TO EXIT CALIBRATION
def inter_pin(cal_in_pin):              # Need variable that causes interrupt
    # DEBOUNCE
    while cal_in_pin.value():   # Wait for debounce sleep
        utime.sleep_us(1)               # Act as NOP
    utime.sleep(PA_main["DEBOUNCE_SL"]) # debounce sleep time

    # WRITE TO THE CALIBRATION INTERRUPT FLAG TO BREAK OUT
    global cal_prog                     # Make sure that we can write to the flag and recognise it
    cal_prog = 1                        # Set flag high for the calibration stage to be done


# CHANGING THE SLOPE
def slope_change_interrupt(sl_ch_in_pin):
    # DEBOUNCE
    while sl_ch_in_pin.value():         # wait for user to take hand off button
        utime.sleep_us(1)               # NOP
    utime.sleep(PA_main["DEBOUNCE_SL"]) # Debounce sleep time

    global slope_dir
    if slope_dir == 1:
        LED.low()
        slope_dir = 1
    else:
        LED.high()
        slope_dir = 0

#################################################################################
# Phase Offset Calculation
#################################################################################

# CONVERT ANALOG VOLTAGE TO PHASE ACCORDING TO AD8302 (really can use either or)
def volt_2_ph(voltage, slope):
    # FALLING SLOPE
    if slope == 1:
        phase = -94.786 * voltage + 177.15
        print('Phase Offset = ', phase)
        return phase
    # RISING SLOPE
    elif slope == 0:
        phase = 94.476 * voltage - 177.44
        print('Phase Offset = ', phase)
        return phase


# CHECK IF THE MEASURED PHASE IS NEW MAX OR MIN
def phase_max_min_check():
    global ph_out_max, ph_out_min

    if ph_out_max < ph_mes:
        ph_out_max = ph_mes

    elif ph_out_min > ph_mes:
        ph_out_min = ph_mes

# CHECK IF PHASE VOLTAGE IS MAX OR MIN
def phase_voltage_close_2_max_min():
    global repeat, ph_mes, index
    marker = PA_main["ERROR"]                           # Set the initial variables used to error protocol
    flag = PA_main["ERROR"]
    mag_dev_mes = PA_main["ERROR"]

    # THESE CALCULATION IS FOR SLOPE DIRECTION 1. INPA: LEFT ANTENNA,   INPB: RIGHT ANTENNA
    # ABOVE THE MAX DEVIATION
    while True:
        # CHECK PHASE VOLTAGE IN UPPER DEVIATION
        if ph_mes[index] < (ph_out_max - PA_main["PHASE_DEV"]):
            break                                   # Get out if measurement is not in Upper Deviation
        flag = 1                                    # Signal that voltage is in deviation zone
        marker = PA_main["HIGH_DEV"]                 # Indicate on Max Deviation Region
        ph_mes[index] = ph_adc_pin.read_u16()              # Change the Phase Voltage value
        mag_dev_mes = mag_adc_pin.read_u16()        # Use this variable to check if we moved on

    # BELOW THE MIN DEVIATION
    while True:
        # CHECK IF THE PHASE VOLTAGE IS IN THE LOWER DEVIATION
        if ph_mes[index] > (ph_out_min + PA_main["PHASE_DEV"]):
            break
        flag = 1                                    # Signal that Village is in Deviation Zone
        marker = PA_main["LOW_DEV"]
        ph_mes[index] = ph_adc_pin.read_u16()
        mag_dev_mes = mag_adc_pin.read_u16()        # Use this variable to check if we moved on

    # TEST CASE FOR RISING SLOPE, UPPER DIV AND IN DEVIATION
    if (marker == PA_main["HIGH_DEV"]) and (flag == 1) and (slope_dir == 0):
        if mag_dev_mes > mag_mes:                   # This means that we move onto
            index = 1                               # move the index
            repeat = 1
            ph_mes[0] = 0                           # Set the phase to 0
            return PA_main["FALLING_SLOPE"]         # Configure the slope direction

        if mag_dev_mes <= mag_mes:  # This means that we move onto
            index = 0  # move the index
            ph_mes[1] = 0                           # reset the over index element
            repeat = 0
            return PA_main["RISING_SLOPE"]  # Configure the slope direction

    # TEST CASE FOR RISING SLOPE, LOWER DIV AND IN DEVIATION
    if (marker == PA_main["LOW_DEV"]) and (flag == 1) and (slope_dir == 0):
        if mag_dev_mes < mag_mes:                   # signal moving left
            index = 1                               # move the index
            ph_mes[0] = -180
            repeat = -1                             # set this indicator
            return PA_main["FALLING_SLOPE"]         # Configure the slope direction
        if mag_dev_mes > mag_mes:                   # signal moving left
            index = 0                               # move the index
            ph_mes[1] = 0                           # Contribute no phase
            repeat = 0                              # set this indicator
            return PA_main["RISING_SLOPE"]          # Configure the slope direction


def phase_offset_calculation():
    if repeat == 1:
        phase_off = abs(ph_mes[0] + ph_mes[1] - ph_cal)
    elif repeat == -1:
        phase_off = abs(ph_mes[0] + 180 - ph_mes[1] - ph_cal)
    else:
        phase_off = abs(ph_cal - ph_mes[0])

    return phase_off


#################################################################################
# INITIALIZATION
#################################################################################
# VARIABLES
cal_prog = 0                            # use to jump out of calibration process
ph_cal = 0                              # Calibrated Phase Recording
ph_mes = [0, 0]                         # Measured Phase Recording
mag_cal = 0                             # Calibrated Magnitude Recording
mag_mes = 0                             # Measured Magnitude Recording
slope_dir = 1                           # determining which slope is being used for the calculation
repeat = 0                              # what iteration on repeat
ph_out_max = 1.8                        # Data Sheet Maximum Phase Voltage Output for AD8302
ph_out_min = 0.3                        # Data Sheet Minimum Phase Voltage Output for AD8302
index = 0

# ON-BOARD LED FOR DEBUGGING
LED = Pin(25, Pin.OUT)                              # Set the LED to output
LED.low()                                           # Set the LED OFF


# CALIBRATION PIN
cal_out_pin = Pin(PA_main["CAL_OUT_PIN"],
                  Pin.OUT)                          # Set Calibration Output Pin to Output
cal_out_pin.high()                                  # Set the value high

cal_in_pin = Pin(PA_main["CAL_IN_PIN"],
                 Pin.IN,                            # Set Calibration Input Pin to Input
                 Pin.PULL_DOWN)                     # Enable for logic 1: HIGH

cal_in_pin.irq(trigger= Pin.IRQ_RISING,             # Set Interrupt to only trigger on rising edge
               handler= inter_pin)                  # Set_up input pin as an interrupt and run "inter_pin" function


# SLOPE CHANGING PIN
sl_ch_out_pin = Pin(PA_main["SL_CH_OUT_PIN"],       # Configure the Slope change Pin
                    Pin.OUT)                        # Set the direction of GPIO
sl_ch_out_pin.high()

sl_ch_in_pin = Pin(PA_main["SL_CH_IN_PIN"],         # Call Pin 15
                   Pin.IN,                          # Set GPIO direction as input
                   Pin.PULL_DOWN)                   # enable pull down resistor

sl_ch_in_pin.irq(trigger= Pin.IRQ_RISING,           # Enable this Pin as Interrupt
                 handler= slope_change_interrupt)   # Set the function protocol to "slope_change_interrupt" function

# ANALOG-TO-DIGITAL CONVERTER PINS
ph_adc_pin = ADC(PA_main["ADC_Ch_1"])               # Init Phase ADC Pin
mag_adc_pin = ADC(PA_main["ADC_Ch_0"])              # Init Mag ADC Pin

# INDICATE INIT IS DONE: 'debugging'
print("Initialization is complete!")

# CALIBRATION PROCESS
print("Begin Calibration Process.\n Please place the Transmitter in the 12 o'clock position.")


#################################################################################
# CALIBRATION
#################################################################################
# CAPTURE ZERO VALUES OF PHASE AND MAGNITUDE OUTPUT OF AD8302
while cal_prog == 0:                                # Keep capturing the zero value until user stops with button press
    ph_cal = ph_adc_pin.read_u16()
    mag_cal = mag_adc_pin.read_u16()

    ph_cal = volt_2_ph(Senior_Project.dig_2_ana(ph_cal), 0)      # Convert the Digital voltage to Analog and into Phase offset [Degrees]

    # DISPLAY MEASUREMENT TO THE USER
    print('Initial Phase Offset: ', '{:2f}'.format(ph_cal))
    utime.sleep(1)                                  # sleep for 1 sec

# CALIBRATION DONE. INDICATE WITH LED
LED.high()                                          # Set value high
print('calibration done')
# Note for later: this should indicate that the slope value is 1

####################################################################
# The initial value of the phase measurement should be in Degrees
####################################################################

####################################################################
# FOREVER LOOP TO CALCULATE PHASE ARRAY AND DISPLAY TO USER
####################################################################
while True:
    # CAPTURE THE MEASUREMENT
    ph_mes[index] = ph_adc_pin.read_u16()
    mag_mes = mag_adc_pin.read_u16()                  # append adds the newest measurement which is the 4th index

    # CALCULATE MAGNITUDE DIFFERENCE FROM CALIBRATION
    mag_dif = mag_mes - mag_cal

    # CONVERT PHASE MEASUREMENT TO ANALOG
    ph_mes[index] = Senior_Project.dig_2_ana(ph_mes[index])

    # CHECK IF WE ARE AT THE MAX OR MIN DEVIATION
    phase_voltage_close_2_max_min()

    # CONVERT THE PHASE VOLTAGE MEASUREMENT TO PHASE
    ph_mes[0] = volt_2_ph(ph_mes[0], 0)
    ph_mes[1] = volt_2_ph(ph_mes[1], slope_dir)
    if repeat == 0:
        ph_mes[1] = 0                   # contribute no phase

    # CALCULATE PHASE OFFSET
    phase_offset = phase_offset_calculation()

    # CALCULATE PHASE ARRAY
    theta = Senior_Project.Phase_array_calc(phase_offset)
    print('Theta: ', theta)
    print('Phase Voltage:', ph_mes)

    # Display direction to user
    heading = Senior_Project.dir_to_heading(theta, mag_dif)
    Senior_Project.dis_head(heading)

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
