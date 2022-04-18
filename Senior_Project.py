import math

# Dictionary for the source file.
ADC_SP = {
    "BIT_RES"   : 65535,                # Denominator for Dig-2-Analog conversion
    "REF_VOLT"  : 3.3,                  # Reference Voltage
    "FREQ"      : 165500000,            # Frequency to 165.5 MHz
    "DIST"      : 3,                    # distance between antenna in meters

}

# This function will convert the digital value to analog
def dig_2_ana(dig_value):
    analog_value = ADC_SP["REF_VOLT"] / ADC_SP["BIT_RES"] * dig_value
    return analog_value

def volt_2_ph(voltage):
    # Convert the voltage received to phase difference
    phase = voltage
    return phase

def volt_2_mag(voltage):
    # Convert the voltage to magnitude difference.
    magnitude = voltage
    return magnitude

def Phase_array_calc(phase):
    beta = 2 * math.pi * ADC_SP["FREQ"]
    delta_r = phase / beta
    theta = math.acos(delta_r / ADC_SP["DIST"])
    return theta