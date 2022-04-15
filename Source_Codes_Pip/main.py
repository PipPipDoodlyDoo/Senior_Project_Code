# Overhead Main codes that the Raspberry Pi will run
import ADC_Senior_Project
from machine import Pin
from machine import ADC


PA_main = {
    "ADC_Ch_0"      : 26,                               # 1st channel for onboard ADC
    "ADC_Ch_1"      : 27                                # 2nd channel for onboard ADC
}

# Initialize ADC Pins
Ph_adc_pin = ADC(Pin(PA_main["ADC_Ch_0"]))              # Init Phase ADC Pin
Mag_adc_pin = ADC(Pin(PA_main["ADC_Ch_1"]))             # Init Mag ADC Pin


# This will be the forever loop
while True:
    # Run the ADC Measurements
    Ph_volt  = Ph_adc_pin.read_u16()
    Mag_volt = Mag_adc_pin.read_u16()

    # Convert both digital value to analog
    Ph_volt  = ADC_Senior_Project.dig_2_ana(Ph_volt)
    Mag_volt = ADC_Senior_Project.dig_2_ana(Mag_volt)

    # Use the conversion formula for voltage -> Phase & Mag

    # Calculate the Phase Array


    # Display direction to user