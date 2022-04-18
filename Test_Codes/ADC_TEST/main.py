# This code will test the ADC Pins onboard the Raspberry Pi Pico
# Please refer to the file "Coding Notes" to clear any confusion possibly

from machine import Pin
from machine import ADC
import utime  # allow the board to sleep in between samples

print('hi')
ADC_Test_lib = {
    "CHANNEL_0": 26,
    "CHANNEL_1": 27,
    "CHANNEL_2": 28,
    "BIT_RES": 65535,  # This is the entire denominator result for the DAC formula
    "REF_VOLT": 3.3,  # The Pico supplies the ADC with 3.3V
    "sleep_time": 2
}


# This functionality will convert the 16-bit voltage back to analog
def dig_2_ana(dig_value):
    analog_volt = ADC_Test_lib["REF_VOLT"] / ADC_Test_lib["BIT_RES"] * dig_value
    return analog_volt


def print_values(d_val, a_val, i):
    if i == 0:
        print('\nChannel 0 values:')
    if i == 1:
        print('\n Channel 1 values:')
    if i == 2:
        print('\n Channel 2 values:')

    print('Digital Value: ', d_val)
    print('Analog Value: ', '{:.2f}'.format(a_val))


adc_digi_results = []  # make an empty list
adc_analog_results = []

# Initialize the pins to perform ADC
CH_0_ADC_Pin = ADC(Pin(ADC_Test_lib["CHANNEL_0"]))
CH_1_ADC_Pin = ADC(Pin(ADC_Test_lib["CHANNEL_1"]))
CH_2_ADC_Pin = ADC(Pin(ADC_Test_lib["CHANNEL_2"]))

# we want to constantly perform the ADC and report back the results
while True:
    # Clear the list make sure that we are working with new data
    adc_digi_results.clear()
    adc_analog_results.clear()
    # Read the analog Voltage
    adc_digi_results.append(CH_0_ADC_Pin.read_u16())
    adc_digi_results.append(CH_1_ADC_Pin.read_u16())
    adc_digi_results.append(CH_2_ADC_Pin.read_u16())

    # Convert all the digital values into analog values
    for x in range(len(adc_digi_results)):
        adc_analog_results.append(dig_2_ana(adc_digi_results[x]))

    # Print the values
    for i in range(len(adc_digi_results)):
        print_values(adc_digi_results[i],adc_analog_results[i],i)


    utime.sleep(ADC_Test_lib["sleep_time"])
