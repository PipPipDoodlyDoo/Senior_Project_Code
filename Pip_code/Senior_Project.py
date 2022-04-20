import math

# Dictionary for the source file.
ADC_SP = {
    "BIT_RES"   : 65535,  # Denominator for Dig-2-Analog conversion
    "REF_VOLT"  : 3.3,  # Reference Voltage
    "FREQ"      : 165500000,  # Frequency to 165.5 MHz
    "DIST"      : 3,  # distance between antenna in meters
    "BETA"      :
}

# This function will convert the digital value to analog
def dig_2_ana(dig_value):
    analog_value = ADC_SP["REF_VOLT"] / ADC_SP["BIT_RES"] * dig_value
    return analog_value

# Convert the voltage received to phase difference
def volt_2_ph(voltage, half):
    if half == 1:
        phase = -0.0105 * voltage + 1.8685
        return phase
    if half == 0:
        phase =  0.0106 * voltage + 1.878
        return phase

# Calculate angle to the beacon signal
def Phase_array_calc(phase):
    beta = 2 * math.pi * ADC_SP["FREQ"]
    delta_r = phase / beta
    theta = math.acos(delta_r / ADC_SP["DIST"])
    return theta

# This will convert the heading to the user
def dir_to_heading(direction):
    if

# This will display to the user where the heading is
def dis_head(heading):
