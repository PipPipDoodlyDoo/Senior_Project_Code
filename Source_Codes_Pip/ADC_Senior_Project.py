from machine import ADC

ADC_SP = {
    "BIT_RES"   : 65535,                # Denominator for Dig-2-Analog conversion
    "REF_VOLT"  : 3.3                   # Reference Voltage
}

# This function will convert the digital value to analog
def dig_2_ana(dig_value):
    analog_value = ADC_SP["REF_VOLT"] / ADC_SP["BIT_RES"] * dig_value
    return analog_value

def volt_2_ph(voltage):
    # Convert the voltage received to phase difference

def volt_2_mag(voltage):
    # Convert the voltage to magnitude difference.