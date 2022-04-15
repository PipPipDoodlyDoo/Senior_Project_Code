# Overhead Main codes that the Raspberry Pi will run
import ADC_Senior_Project
from machine import Pin
from machine import ADC


PA_main = {
    "ADC_Ch_0"      : 26,                               # 1st channel for onboard ADC
    "ADC_Ch_1"      : 27                                # 2nd channel for onboard ADC
}
# initialize the adc measurements as an array in a global level
ADC_mes = [0, 0]    # [0]: Phase, [1]: Magnitude

# Initialize ADC Pins
Ph_adc_pin = ADC(Pin(PA_main["ADC_Ch_0"]))              # Init Phase ADC Pin
Mag_adc_pin = ADC(Pin(PA_main["ADC_Ch_1"]))             # Init Mag ADC Pin

# Might want to work on a calibration stage


# This will be the forever loop
while True:

    # Run the ADC Measurements
    # Calculate the Phase Array
    # Display direction to user