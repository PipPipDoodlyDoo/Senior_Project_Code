# Main Code for ALT_CODE. Similar to Version 3
# This will only use one slope. REMEMBER THAT PHASE STEP IS 10 mV per 10 degree

# SOURCE CODES INCLUDED
import Senior_Project                                   # Modulating the Code
from machine import Pin                                 # Use for Calibration Human Interaction
from machine import ADC                                 # Read Voltage from AD8302
import utime                                            # Sleep time

# DICTIONARY "LIBRARY OF VARIABLES THAT WILL BE USED"
PA_main = {
    "ADC_Ch_0"          : 26,                           # Phase Channel
    "ADC_Ch_1"          : 27,                           # Magnitude Channel
    "ADC_Ch_2"          : 28,
    "cal_in_pin"        : 18,                           # Calibration Pin
    "cal_out_pin"       : 20,
    "CONFIRM_OUT_PIN"   : 14,
    "CONFIRM_IN_PIN"    : 15,                           # Confirm Pin used for calibration
    # Reference Pin
    "RISING_SLOPE"      : 1,
    "FALLING SLOPE"     : 0,
    "LOWER_DEF"         : 180,                          # Lower Overlap Default value
    "UPPER_DEF"         : 0,                            # Upper Overlap Default value
    "CENTER"            : 0,                            # No overlap
    "UPPER"             : 1,                            # Overlap on the phase lead
    "LOWER"             : -1,                           # Overlap on Phase Lag sides
    "DEBOUNCE_SL"       : 1,                           # Debounce sleeping time
    "MAG_SAMPLES"       :15
}

# INTERRUPT FOR CALIBRATION DONE BUTTON
def cal_interrupt(cal_in_pin):                              # Need variable that causes interrupt
    cal_out_pin.low()                                   # Turn off the Pin

    # DEBOUNCE
    while cal_in_pin.value():                           # Wait for debounce sleep
        utime.sleep_us(1)                               # Act as NOP
    utime.sleep(PA_main["DEBOUNCE_SL"])                 # debounce sleep time

    global cal_prog                                     # Make sure that we can write to the flag and recognise it
    cal_prog = 1                                        # Set flag high for the calibration stage to be done

    cal_in_pin.high()                                   # Turn the Calibration Output Pin ON

# INTERRUPT FOR CONFIRMATION BUTTON
def confirm_func(conf_in_pin):
    conf_out_pin.low()

    # DEBOUNCE
    while conf_in_pin.value():
        utime.sleep_us(1)
    utime.sleep(PA_main["DEBOUNCE_SL"])

    global confirm
    confirm = 1

    conf_in_pin.high()

# AVERAGE CALCULATION FOR MAGNITUDE
def average_calc():
    average = 0
    if index == PA_main["UPPER"]:                       # Looking for the upper mag
        for a in range(len(mag_array)):
            average += mag_array[a]
        average /= len(mag_array)                       # divide the array by size
        return average

    if index == PA_main["LOWER"]:
        for a in range(len(mag_array)):
            average += mag_array[a]
        average /= len(mag_array)                       # divide the array by size
        return average


#######################################################################################
# VARIABLES USED
#######################################################################################
cal_prog    = 0                                         # use to jump out of calibration process
ph_cal      = 0                                         # Calibrated Phase Recording
ph_mes      = 0                                         # Measured Phase Recording
ph_mes_up   = 0
ph_mes_down = 180
mag_cal     = 0                                         # Calibrated Magnitude Recording
mag_mes     = 0                                         # Measured Magnitude Recording
upper_mag   = 0                                         # Measure the magnitude between 1.6 to 1.7 V
lower_mag   = 0                                         # measure the magnitude between 0.1 to 0.2 V
mag_array   = []                                        # place holder
confirm     = 0                                         # FLAG to confirm magnitude captures at THRESHOLD VOLTAGES
index       = PA_main["CENTER"]                         # Indicate which region is overlap


#######################################################################################
# INITIALIZATION
#######################################################################################
# ON-BOARD LED
LED = Pin(25, Pin.OUT)                                                      # Set the LED to output
LED.low()                                                                   # Set the LED OFF

# CALIBRATION OUTPUT PIN
cal_out_pin = Pin(PA_main["cal_out_pin"],
                  Pin.OUT)                                                  # Set Pin 1 to Output
cal_out_pin.high()                                                          # Put the value high

# CALIBRATION INPUT PIN AS INTERRUPT
cal_in_pin = Pin(PA_main["cal_in_pin"],
                 Pin.IN,
                 Pin.PULL_DOWN)                                             # Set the initial value to zero
cal_in_pin.irq(trigger=Pin.IRQ_RISING,
               handler= cal_interrupt)                                          # Set_up input pin as an interupt and run "cal_interrupt" function

# CONFIRMATION OUTPUT PIN
conf_out_pin = Pin(PA_main["CONFIRM_OUT_PIN"],
                   Pin.OUT)                                                 # Initialize confirmation Output Pin
conf_out_pin.high()                                                         # Turn Confirm Output Pin ON

# CONFIRMATION INPUT PIN AS INTERRUPT
conf_in_pin = Pin(PA_main["CONFIRM_IN_PIN"], Pin.IN)                        # Configure Confirmation Pin
conf_in_pin.irq(trigger= Pin.IRQ_RISING,                                    # Set as interrupt for Rising Edge Triggered
                handler= confirm_func)

# ANALOG TO DIGITAL CONVERTER PIN
ph_adc_pin = ADC(Pin(PA_main["ADC_Ch_1"]))                                  # Init Phase ADC Pin
mag_adc_pin = ADC(Pin(PA_main["ADC_Ch_0"]))                                 # Init Mag ADC Pin

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
while cal_prog == 0:                                                        # Keep capturing the zero value until user stops with button press
    ph_cal  = ph_adc_pin.read_u16()
    mag_cal = mag_adc_pin.read_u16()

    ph_cal  = Senior_Project.volt_2_ph(Senior_Project.dig_2_ana(ph_cal), 1) # Convert the Digital voltage to Analog and into Phase offset [Degrees]

    # DISPLAY MEASUREMENT TO THE USER
    print('Initial Phase Offset: ', '{:2f}'.format(ph_cal))

# CONFIRM USER THAT SWEEP RIGHT RAISES VOLTAGE
print('Hold the signal at 15 degree offset')

# CAPTURE THE 10 DEGREE OFFSET IN ARRAY
while confirm == 0:                                                         # Wait for the user to confirm
    utime.sleep_us(1)

# CALCULATE AVERAGE FOR 10 DEGREE OFFSET
for i in range(PA_main["MAG_SAMPLES"]):
    mag_array.append(mag_adc_pin.read_u16())                                # create the array

index = PA_main["UPPER"]                                                    # Set this for the magnitude
upper_mag = average_calc()

print('Hold the signal at 165 degree offset')
for i in range(len(mag_array)):
    mag_array[i] = (mag_adc_pin.read_u16())                             # create the array

# CALCULATE AVERAGE FOR 170 DEGREE OFFSET
index = PA_main["LOWER"]                                                # Set this for the magnitude
lower_mag = average_calc()
del mag_array                                                           # delete variable for space
utime.sleep(1)                                                          # sleep for 1 sec

# MIGHT CHANGE PHASE CAL VALUE TO DEG OFFSET
####################################################################
# The initial value of the phase measurement should be in Degrees
####################################################################



# FOREVER LOOP TO CALCULATE PHASE ARRAY AND DISPLAY TO USER
while True:
    # CAPTURE ADC MEAS
    ph_mes  = ph_adc_pin.read_u16()                                         # Measurement in Digital Voltage
    mag_mes = mag_adc_pin.read_u16()

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