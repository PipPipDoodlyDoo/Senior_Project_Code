# Overhead Main codes that the Raspberry Pi will run
import Senior_Project
from machine import Pin
from machine import ADC
import utime

# This will be the dictionary for the main script
PA_main = {
    "ADC_Ch_0"      : 26,                               # 1st channel for onboard ADC
    "ADC_Ch_1"      : 27                                # 2nd channel for onboard ADC
}

theta = []                                              # Start a list for the old value and new value

# Initialize ADC Pins
Ph_adc_pin = ADC(Pin(PA_main["ADC_Ch_0"]))              # Init Phase ADC Pin
Mag_adc_pin = ADC(Pin(PA_main["ADC_Ch_1"]))             # Init Mag ADC Pin

# This will be the forever loop
while True:
    # Run the ADC Measurements
    Ph_volt  = Ph_adc_pin.read_u16()
    Mag_volt = Mag_adc_pin.read_u16()

    # Convert both digital value to analog
    Ph_volt  = Senior_Project.dig_2_ana(Ph_volt)
    Mag_volt = Senior_Project.dig_2_ana(Mag_volt)
    print("Phase Voltage is: ", '{:.2f}'.format(Ph_volt))
    print("\n Magnitude Voltage is: ", '{:.2f}'.format(Ph_volt))

    utime.sleep(2)
    # Use the conversion formula for voltage -> Phase & Mag


    # Calculate the Phase Array


    # Display direction to user