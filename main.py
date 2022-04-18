# This code will test the ADC Pins onboard the Raspberry Pi Pico
# Please refer to the file "Coding Notes" to clear any confusion possibly

from machine import Pin
from machine import ADC
import utime                # allow the board to sleep in between samples

ADC_Test_lib = {
    "CHANNEL_0"     : 26,
    "CHANNEL_1"     : 27,
    "CHANNEL_2"     : 28,
    "BIT_RES"       : 65535,        # This is the entire denominator result for the DAC formula
    "REF_VOLT"      : 3.3,          # The Pico supplies the ADC with 3.3V
    "sleep_time"    : 2
}

# This functionailty will convert the 16-bit voltage back to analog
def dig_2_ana(dig_value):
    analog_volt = ADC_Test_lib["REF_VOLT"] / ADC_Test_lib["BIT_RES"] * dig_value
    return analog_volt

def print_values(d_val, a_val, i):
    match i:                    # using a switch statement but for python
        case 0:
            print('For Channel 0 (Pin 26)')
        case 1:
            print('For Channel 1 (Pin 27)')
        case 2:
            print('For Channel 2 (Pin 28)')

    print('Digital Value: ', d_val)
    print('\n Analog Value: ', '{:.2f}'.format(a_val))


adc_digi_results = []            # make an empty list
adc_analog_results = []

# Initialize the pins to perform ADC
CH_0_ADC_Pin = ADC(Pin(ADC_Test_lib["CHANNEL_0"]))
CH_1_ADC_Pin = ADC(Pin(ADC_Test_lib["CHANNEL_1"]))
CH_2_ADC_Pin = ADC(Pin(ADC_Test_lib["CHANNEL_2"]))

# we want to constantly perform the ADC and report back the results
while True:
    # Read the analog Voltage
    adc_digi_results[0] = CH_0_ADC_Pin.read_u16()
    adc_digi_results[1] = CH_1_ADC_Pin.read_u16()
    adc_digi_results[2] = CH_2_ADC_Pin.read_u16()

    # Convert all the digitial values into analog values
    for x in adc_digi_results:
        adc_analog_results[x] = dig_2_ana(adc_digi_results[x])

    # display the values to the REPL
    for x in adc_digi_results:
        print_values(adc_digi_results[x], adc_analog_results[x], x)

    utime.sleep(ADC_Test_lib["sleep_time"])