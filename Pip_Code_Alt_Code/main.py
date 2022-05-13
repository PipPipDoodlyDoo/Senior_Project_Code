# Main Code for ALT_CODE. Similar to Version 3
# This will only use one slope. REMEMBER THAT PHASE STEP IS 10 mV per 10 degree

# SOURCE CODES INCLUDED
import Senior_Project                                   # Modulating the Code
import Library                                          # Where all the definitions are located
from machine import Pin                                 # Use for Calibration Human Interaction
from machine import ADC                                 # Read Voltage from AD8302
import utime                                            # Sleep time. Use 'utime.sleepus(1)' as NOP no operation

####################################################################
# Interrupt Functions
####################################################################
# INTERRUPT FOR CALIBRATION DONE BUTTON
def cal_interrupt(cal_in_pin):                          # Need variable that causes interrupt

    # DEBOUNCE PROTOCOL
    while cal_in_pin.value():                           # Wait for user to release Calibration Button
        utime.sleep_us(1)                               # Act as NOP
    utime.sleep(Library.MAIN_LIB["DEBOUNCE_SL"])                 # debounce sleep time

    global cal_prog                                     # Make sure that we can write to the flag and recognise it
    cal_prog = 1                                        # Set flag high for the calibration stage to be done


# INTERRUPT FOR CONFIRMATION BUTTON
def confirm_func(conf_in_pin):

    # DEBOUNCE PROTOCOL
    while conf_in_pin.value():
        utime.sleep_us(1)
    utime.sleep(Library.MAIN_LIB["DEBOUNCE_SL"])

    global confirm
    confirm = 1                                         # Set the flag off to confirm for Magnitude Array Measurement


def debug_interrupt(debug_in_pin):

    # DEBOUNCE PROTOCOL
    while debug_in_pin.value():
        utime.sleep_us(1)
    utime.sleep(Library.MAIN_LIB["DEBOUNCE_SL"])

    global debug_flag
    debug_flag = 1



####################################################################
# Functions
####################################################################
# THIS WILL BE CALCULATING WHETHER THE SIGNAL IS AT THE MAX OR MIN THRESHOLD
def max_min_check(ph_initial):
    # we have to globalize index and switching the ph_mes.
    global index, mag_mes, ph_mes, flag, ph_mes_up, ph_mes_down
    # MOMENTARY VARIABLES THAT WILL BE USED
    flag = 0                                            # Flag used to show where we are
    ph_mes = ph_initial                                 # Reset the initial voltage
    # The center region is the common ground between UPPER AND LOWER REGION so that is why we will force
    # the ph_mes to be the ph usage here


    #USE THE THRESSHOLD VOLTAGE BUFFER LOCATED ON THE LIBRARY INDEX
    # UPPER THRESHOLD
    while ph_mes >= Library.MAIN_LIB["UPPER_VOLT_THRES"]:            # Check if the phase voltage is within UPPER ambiguity region
        # CAPTURE ADC MEASUREMENTS
        mag_mes = mag_adc_pin.read_u16()
        ph_mes = ph_adc_pin.read_u16()

        flag = Library.MAIN_LIB["UPPER_REGION"]                      # Set off the flag that there was an Upper Threshold tirggered

    # LOWER THRESHOLD
    while ph_mes <= Library.MAIN_LIB["LOWER_VOLT_THRES"]:
        # CAPTURE ADC MEASUREMENTS
        mag_mes = mag_adc_pin.read_u16()
        ph_mes = ph_adc_pin.read_u16()

        flag = Library.MAIN_LIB["LOWER_REGION"]                      # Set off flag for Lower Threshold disturbance

    # CHANGE THE INDEX IF THERE WAS A DISTURBANCE
    if flag == Library.MAIN_LIB["UPPER_REGION"]:                     # Indicate which region we are in
        if mag_mes >= (upper_mag + Library.MAIN_LIB["MAG_BUFFER"]):  # Check the magnitude if it is higher than before
            index = Library.MAIN_LIB["UPPER_REGION"]                 # Set the index for operating at

            ph_mes_up = ph_mes                              # This will be the new measurement
            ph_mes = Library.MAIN_LIB["DEFAULT_PH_SH_UP"]            # Reset to max

        else:
            index = Library.MAIN_LIB["CENTER_REGION"]                # Reset to center region


    elif flag == Library.MAIN_LIB["LOWER_REGION"]:                   # Check which region we are working wiht
        if mag_mes <= (lower_mag - Library.MAIN_LIB["MAG_BUFFER"]):  # Check the magnitude to see if pass through into lower region
            index = Library.MAIN_LIB["LOWER_REGION"]                 # Set to lower region for calculation

            ph_mes_down = ph_mes
            ph_mes = Library.MAIN_LIB["DEFAULT_PH_SHIFT"]

        else:
            index = Library.MAIN_LIB["CENTER_REGION"]                # Reset to center region
            # no need to change the ph_mes because that is what the center region uses already

def display_phase():
    phase = ph_adc_pin.read_u16()                           # Read the ADC Pin
    phase = Senior_Project.dig_2_ana(phase)                 # Convert Digital to analog

    phase = Senior_Project.volt_2_ph(phase)                 # Convert the voltage to a phase

    print('Current phase offset = ', phase)

    

# AVERAGE CALCULATION FOR MAGNITUDE
def average_calc():
    # INITIALIZE HOLDER VARIABLE FOR AVERAGE CALCULATION
    average = 0
    # ADD ALL 'mag_array' ELEMENTS TO AVERAGE
    for a in range(len(mag_array)):
        average += mag_array[a]
    # DIVIDE SUM BY TOTAL NUMBER OF ELEMENTS WITHIN 'mag_array' ARRAY
    average /= len(mag_array)
    return average

def debug_routine():
    LED.high()                          # Turn on the LED
    global debug_flag
    debug_flag = 0
    while debug_flag == 0:              # wait for debug button
        utime.sleep_us(1)

    LED.low()                           # Turn it off


#######################################################################################
# VARIABLES USED
#######################################################################################
cal_prog        = 0                                     # use to jump out of calibration process
ph_cal          = 0                                     # Calibrated Phase Recording
ph_mes          = 0                                     # Measured Phase Recording
ph_mes_up       = 0
ph_mes_down     = -180                                  # Mainly using the rising slope
mag_cal         = 0                                     # Calibrated Magnitude Recording
mag_mes         = 0                                     # Measured Magnitude Recording
upper_mag       = 0                                     # Measure the magnitude between 1.6 to 1.7 V
lower_mag       = 0                                     # measure the magnitude between 0.1 to 0.2 V
mag_array       = []                                    # place holder
confirm         = 0                                     # FLAG to confirm magnitude captures at THRESHOLD VOLTAGES
flag            = 0                                     # Use this to check if there is an instance of change
index           = Library.MAIN_LIB["CENTER_REGION"]     # Indicate which region is overlap
current_phase   = 0

debug_flag      = 0                                     # Use this for debugging

#######################################################################################
# INITIALIZATION
#######################################################################################
# ON-BOARD LED
LED = Pin(25, Pin.OUT)                                  # Set the LED to output
LED.low()                                               # Set the LED OFF

# CALIBRATION OUTPUT PIN
cal_out_pin = Pin(Library.MAIN_LIB["cal_out_pin"],
                  Pin.OUT)                              # Set Pin 1 to Output
cal_out_pin.high()                                      # Put the value high

# CALIBRATION INPUT PIN AS INTERRUPT
cal_in_pin = Pin(Library.MAIN_LIB["cal_in_pin"],
                 Pin.IN,
                 Pin.PULL_DOWN)                         # Set the initial value to zero
cal_in_pin.irq(trigger=Pin.IRQ_RISING,                  # Set Interrupt for Rising Edge Trigger
               handler= cal_interrupt)                  # Run "cal_interrupt" defined function

# CONFIRMATION OUTPUT PIN
conf_out_pin = Pin(Library.MAIN_LIB["CONFIRM_OUT_PIN"],
                   Pin.OUT)                             # Initialize confirmation Output Pin
conf_out_pin.high()                                     # Turn Confirm Output Pin ON

# CONFIRMATION INPUT PIN AS INTERRUPT
conf_in_pin = Pin(Library.MAIN_LIB["CONFIRM_IN_PIN"],
                  Pin.IN,
                  Pin.PULL_DOWN)

conf_in_pin.irq(trigger= Pin.IRQ_RISING,                # Set as interrupt for Rising Edge Triggered
                handler= confirm_func)

# DEBUG OUTPUT PIN
debug_out_pin = Pin(Library.MAIN_LIB["DEBUG_OUT_PIN"], Pin.OUT)  # Configure Output Pin
debug_out_pin.high()                                            # Set output High

debug_in_pin = Pin(Library.MAIN_LIB["DEBUG_IN_PIN"],
                   Pin.IN,
                   Pin.PULL_DOWN)

debug_in_pin.irq(trigger= Pin.IRQ_RISING,
                 handler= debug_interrupt)


# ANALOG TO DIGITAL CONVERTER PIN
ph_adc_pin = ADC(Pin(Library.MAIN_LIB["ADC_Ch_1"]))              # Initialize Phase ADC Pin
mag_adc_pin = ADC(Pin(Library.MAIN_LIB["ADC_Ch_0"]))             # Initialize Mag ADC Pin

# INDICATE INIT IS DONE: 'debugging'
print("Initialization is complete!")

#######################################################################################
# CALIBRATION PROCESS
#######################################################################################
# INDICATE TO THE USER TO BEING CALIBRATION
print("Begin Calibration Process.\n Please place the Transmitter in the 12 o'click position.")

##################################################################################
# Calibration Routine
##################################################################################

# CAPTURE ZERO VALUES OF PHASE AND MAGNITUDE OUTPUT OF AD8302
while cal_prog == 0:                                                # Keep capturing the zero value until user stops with button press
    # READ ADC PIN VOLTAGES
    ph_cal  = ph_adc_pin.read_u16()
    mag_cal = mag_adc_pin.read_u16()

    # CONVERT VOLTAGES TO ANALOG
    ph_cal  = Senior_Project.volt_2_ph(Senior_Project.dig_2_ana(ph_cal))     # Convert the Digital voltage to Analog and into Phase offset [Degrees]
    mag_cal = Senior_Project.dig_2_ana(mag_cal)
    # DISPLAY MEASUREMENT TO THE USER
    print('Initial Phase Offset: ', '{:2f}'.format(ph_cal))

# NOTE: THIS MEASUREMENT IS MADE FOR INPUT B PHASE LAGGING. Meaning that as the signal heads right relative to drones flying direction
#         the voltage should increase so the 2 input phase should be aligning
##############################################################################################################
# MAY HAVE TO CHANGE UPPER AND LOWER THRESHOLD
# CONFIRM USER THAT SWEEP RIGHT RAISES VOLTAGE
print('Hold the signal at 15 degree offset')

# CAPTURE THE 10 DEGREE OFFSET IN ARRAY
while confirm == 0:                                     # Wait for the user to confirm
    display_phase()
    utime.sleep_ms(Library.MAIN_LIB["PAUSE_TIME"])

# CALCULATE AVERAGE FOR 10 DEGREE OFFSET
for i in range(Library.MAIN_LIB["MAG_SAMPLES"]):                 # define array size from library definition
    mag_array.append(mag_adc_pin.read_u16())            # create the array

# SET THE MAGNITUDE FOR AVERAGE CALCULATION FOR THE WHOLE UPPER MAGNITUDE
upper_mag = average_calc()
upper_mag = Senior_Project.dig_2_ana(upper_mag)         # Change digital to analog voltage

confirm = 0                                             # Reset the flag

print('Hold the signal at 165 degree offset')
while confirm == 0:
    display_phase()
    utime.sleep_ms(Library.MAIN_LIB["PAUSE_TIME"])

for i in range(len(mag_array)):                         # Array size already set therefore just loop array size
    mag_array[i] = (mag_adc_pin.read_u16())             # Re-write Magnitude Array

# CALCULATE AVERAGE FOR 170 DEGREE OFFSET
lower_mag = average_calc()
lower_mag = Senior_Project.dig_2_ana(lower_mag)         # Change to a voltage

# DELETE VARIABLE TO MAKE SPACE
del mag_array, confirm


# Print the average values
print('The average MAGNITUDE value for upper threshold is: ', '{:2f}'.format(upper_mag))
print('The average MAGNITUDE value for lower threshold is: ', '{:2f}'.format(lower_mag))
utime.sleep(1)                                          # sleep for 1 sec

debug_routine()

# MIGHT CHANGE PHASE CAL VALUE TO DEG OFFSET
####################################################################
# The initial value of the phase measurement should be in Degrees
####################################################################










# LEFT OFF HERE








# FOREVER LOOP TO CALCULATE PHASE ARRAY AND DISPLAY TO USER
while True:
    # CAPTURE ADC MEAS
    ##### MAY NEED TO DO IF STATEMENT TO CHANGE THE RECORDED VALUE DEPENDING ON REGION OF CAPTURE
    # UPPER AND LOWER OVERLAPS
    # NO OVERLAP CASE
    debug_flag()
    if index == Library.MAIN_LIB["CENTER_REGION"]:
        ph_mes = ph_adc_pin.read_u16()                      # Take measurement regularly
        # CONVERT VOLTAGE FROM DIGITAL TO ANALOG VOLTAGE
        ph_mes = Senior_Project.dig_2_ana(ph_mes)

        max_min_check(ph_mes)  # Check if we are on the threshold

        current_phase = Senior_Project.volt_2_ph(ph_mes)

        # Doesnt really matter for these
        ph_mes_up = Library.MAIN_LIB["DEFAULT_PH_SHIFT"]             # Force Upper measurement to be 0 phase contribution
        ph_mes_down = Library.MAIN_LIB["DEFAULT_PH_SHIFT"]           # Force Lower to be 0 phase Contribution when calculating



    # UPPER REGION OF OVERLAP
    elif index == Library.MAIN_LIB["UPPER_REGION"]:
        ph_mes = 180                                        # Preset the Phase Shift to 180 degree offset

        ph_mes_up = ph_adc_pin.read_u16()                   # The upper is reading the phase offset from AD8302
        # CONVERT THIS PHASE OFFSET FROM DIGITAL VOLTAGE
        ph_mes_up = Senior_Project.dig_2_ana(ph_mes_up)

        max_min_check(ph_mes_up)                            # Check if the voltage is at max or min threshold

        current_phase = Senior_Project.volt_2_ph(ph_mes_up)
        ph_mes_down = Library.MAIN_LIB["DEFAULT_PH_SHIFT"]           # No Contribution



    # LOWER REGION OF OVERLAP
    elif index == Library.MAIN_LIB["LOWER_REGION"]:
        ph_mes = 0                                          # Preset to the lower limit
        ph_mes_up = Library.MAIN_LIB["DEFAULT_PH_SHIFT"]             # No Contribution
        ph_mes_down = ph_adc_pin.read_u16()                 # The lower half becomes the ADC Read Pin now

        max_min_check(ph_mes_down)

    # CONVERT PHASE DIGITAL VALUE TO ANALOG
        current_phase = Senior_Project.volt_2_ph(ph_mes_down)

    if flag != 0:                                           # Check if there was a change instance. If so then skip calcualtion
        mag_mes = mag_adc_pin.read_u16()                    # We have the Phase Offset Measurement now for the magnitude measurements
        phase_offset = Senior_Project.phase_offset_calculation(index, current_phase, ph_cal)

        print("OVERALL PHASE OFFSET = ", phase_offset)
        debug_routine()


        # HAVE TO CALCULATE THE OVERALL PHASE OFFSET
        # we can use the index to help indicate what calculations we have to do
        # use a function


    ####################################################################
    # Check the Voltage if it hit the max or min
    ####################################################################



    #
    # # USE CONVERSION FORMULA FOR VOLTAGE -> PHASE
    # ph_mes = Senior_Project.volt_2_ph(ph_mes)           # This should make ph_mes in degrees
    #
    #
    # # CALCULATE PHASE DIFFERENCE FOR PHASE ARRAY CALC
    # ph_dif  = abs(ph_cal - ph_mes)                      # Calculate the phase
    # print('Phase Difference: ', ph_dif)
    # mag_dif = mag_cal - mag_mes
    # print('Magnitude Difference: ',mag_dif)
    #
    # # CALCULATE PHASE ARRAY
    # theta = Senior_Project.Phase_array_calc(ph_dif)
    # print('Theta: ', theta)
    # # Display direction to user
    # heading = Senior_Project.dir_to_heading(theta, mag_dif)
    # Senior_Project.dis_head(heading)
    # utime.sleep(2)