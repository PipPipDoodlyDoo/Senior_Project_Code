# Overhead Main codes that the Raspberry Pi will run
import Senior_Project
import Calibration
from machine import Pin
from machine import ADC
import utime

# This will be the dictionary for the main script
PA_main = {
    "ADC_Ch_0"      : 26,                               # 1st channel for onboard ADC
    "ADC_Ch_1"      : 27                                # 2nd channel for onboard ADC
}

# Initialize the LCaED pin for debugging
LED = Pin(25, Pin.OUT)                                  # Set the LED to output
LED.value(0)                                            # Set the LED OFF

# Initialize ADC Pins
Ph_adc_pin = ADC(Pin(PA_main["ADC_Ch_0"]))              # Init Phase ADC Pin
Mag_adc_pin = ADC(Pin(PA_main["ADC_Ch_1"]))             # Init Mag ADC Pin

# Set up the variables that will be used
ph_mes = []                                             # This will be useful for the calibration process
mag_mes = []                                            # Don't know if we'll need this later
cal_prog = 0                                            # use to jump out of calibration process

# Indicate to the user that the Initialization is done
print("Intialization is complete!")

# Calibrartion




# This will be the forever loop
while True:
    # Run the ADC Measurements
    Ph_volt  = Ph_adc_pin.read_u16()
    Mag_volt = Mag_adc_pin.read_u16()
    print("Phase Voltage is: ", '{:.2f}'.format(Ph_volt))
    print("\n Magnitude Voltage is: ", '{:.2f}'.format(Ph_volt))

    # Convert both digital value to analog
    #Ph_volt  = Senior_Project.dig_2_ana(Ph_volt)
    #Mag_volt = Senior_Project.dig_2_ana(Mag_volt)

    # Use the conversion formula for voltage -> Phase & Mag


    # Calculate the Phase Array


    # Display direction to user

    utime.sleep(2)