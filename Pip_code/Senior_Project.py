import math

# Dictionary for the source file.
ADC_SP = {
    "BIT_RES"   : 65535,        # Denominator for Dig-2-Analog conversion
    "REF_VOLT"  : 3.3,          # Reference Voltage
    "FREQ"      : 165500000,    # Frequency to 165.5 MHz
    "DIST"      : 1,            # distance between antenna in meters
    "BETA"      : 3.466,        # Beta for 165.5 MHz for Phase Array Calculation
    "3 o'clock" : 0,            # These are headings
    "2 o'clock" : 1,
    "1 o'clock" : 2,
    "12 o'clock": 3,
    "11 o'clock": 4,
    "10 o'clock": 5,
    "9 o'clock" : 6,
    "ERROR"     : 7             # This would mean that the signal was out of phase
}

# This function will convert the digital value to analog
def dig_2_ana(dig_value):
    analog_value = ADC_SP["REF_VOLT"] / ADC_SP["BIT_RES"] * dig_value
    print("Analog Voltage: ", '{:2f}'.format(analog_value))         # print out the analog voltage
    return analog_value

# Convert the analog voltage received to phase difference
def volt_2_ph(voltage, half):
    if half == 1:
        phase = abs(-94.786 * voltage + 177.15)
        print('Phase Offset = ', phase)
        return phase
    elif half == 0:
        phase =  abs(94.476 * voltage - 177.44)
        phase = abs(phase)
        print('Phase Offset = ', phase)
        return phase

# Calculate angle to the beacon signal
def Phase_array_calc(phase):
    delta_r = math.radians(phase) / ADC_SP["BETA"]
    theta = math.degrees(math.acos(delta_r / ADC_SP["DIST"]))
    print("Theta value: ", theta)
    return theta

# This will convert the heading to the user
def dir_to_heading(degree):
    # 3 o'clock heading
    if ((degree >= 0) and (degree <= 15)):
        return ADC_SP["3 o'clock"]
    # 2 o'clock heading
    elif ((degree >= 15) and (degree <= 45)):
        return ADC_SP["2 o'clock"]
    # 1 o'clock heading
    elif ((degree >= 45) and (degree <= 75)):
        return ADC_SP["1 o'clock"]
    # 12 o'clock heading
    elif ((degree >= 75) and (degree <= 105)):
        return ADC_SP["12 o'clock"]
    # 11 o'clock heading
    elif ((degree >= 105) and (degree <= 135)):
        return ADC_SP["11 o'clock"]
    # 10 o'clock heading
    elif ((degree >= 135) and (degree <= 165)):
        return ADC_SP["10 o'clock"]
    # 9 o'clock heading
    elif ((degree >= 165) and (degree <= 180)):
        return ADC_SP["9 o'clock"]
    else:
        return ADC_SP["ERROR"]


# This will display to the user where the heading is
def dis_head(heading):
    if heading == 0:
        print("Signal Located at 3 o'Clock")
    elif heading == 1:
        print("Signal Located at 2 o'Clock")
    elif heading == 2:
        print("Signal Located at 1 o'Clock")
    elif heading == 3:
        print("Signal Located at 12 o'Clock")
    elif heading == 4:
        print("Signal Located at 11 o'Clock")
    elif heading == 5:
        print("Signal Located at 10 o'Clock")
    elif heading == 6:
        print("Signal Located at 9 o'Clock")
    else:
        print("Error")