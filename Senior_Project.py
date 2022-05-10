# Source Code for ALT_CODE
import math

# DICTIONARY FOR SOURCE FILE
SP_LIB = {
    "REF_VOLT"      : 3.3,                          # Reference Voltage for ADC
    "BIT_RES"       : 65535,                        # Bit Resolution for ADC
    "DIST"          : 1.65,                         # distance between antennas [meters] (76 cm)
    "BETA"          : 3.466,                        # Beta for 165.5 MHz
    "LAMBDA"        : 1.812,                        # wavelength for 165.5 MHz
    "NUM_ELEM"      : 2,                            # Number of Elements
    "3 o'clock"     : 0,                            # direction headings
    "2 o'clock"     : 1,
    "1 o'clock"     : 2,
    "12 o'clock"    : 3,
    "11 o'clock"    : 4,
    "10 o'clock"    : 5,
    "9 o'clock"     : 6,
    "ERROR"         : 7,
    "RISING_SLOPE"  : 1,
    "FALLING_SLOPE" : 0
}

# DIGITAL TO ANALOG CONVERTOR
def dig_2_ana(dig_value):
    analog_value = SP_LIB["REF_VOLT"] / SP_LIB["BIT_RES"] * dig_value
    print("\nAnalog Voltage: ", '{:2f}'.format(analog_value))         # print out the analog voltage
    return analog_value

# ANALOG TO PHASE OFFSET CONVERTOR
def volt_2_ph(voltage):
    # if half == SP_LIB["FALLING_SLOPE"]:
    #     phase = abs(-94.786 * voltage + 177.15)
    #     print('Phase Offset = ', phase)
    #     return phase
    # elif half == SP_LIB["RISING_SLOPE"]:
    #     #        phase = abs(94.476 * voltage - 177.44)                         # Original
    #     phase = abs(phase)

    # NEW VERSION. AS VOLTAGE INCREASES SO DOES PHASE OFFSET
    phase = abs(94.476 * voltage)
    print('Phase Offset = ', phase)
    return phase

# PHASE ARRAY CALCULATION: (Relative to drone's flying direction)
def Phase_array_calc(phase):
    phase = math.radians(phase)
    theta = (phase * SP_LIB["NUM_ELEM"] * SP_LIB["LAMBDA"])/(2 * math.pi * SP_LIB["DIST"])  # General Equation for Phase Array
    theta = math.asin(theta)                                                                # Inverse Sine in radians
    theta = theta * 180 / math.pi                                                           # Convert to Degrees
    return theta

# USE THE INFORMATION TO SHOW USER WHERE BACON (lol) SIGNAL IS
def dir_to_heading(degree, direction):
    if (degree <= 15) and (degree >= 0):
        return SP_LIB["12 o'clock"]                     # Don't need to worry about magnitude

    if direction >= 0:                                  # Test if beacon signal is to the left
        if (degree > 15) and (degree <= 45):
            return SP_LIB["11 o'clock"]
        elif (degree > 45) and (degree <= 75):
            return SP_LIB["10 o'clock"]
        elif (degree > 75) and (degree <= 90):
            return SP_LIB["9 o'clock"]

    if direction < 0:                                   # Signal to the right
        if (degree > 15) and (degree <= 45):
            return SP_LIB["1 o'clock"]
        elif (degree > 45) and (degree <= 75):
            return SP_LIB["2 o'clock"]
        elif (degree > 75) and (degree <= 90):
            return SP_LIB["3 o'clock"]

# This will display to the user where the heading is
def dis_head(heading):
    if heading == SP_LIB["3 o'clock"]:
        print("Signal Located at 3 o'Clock")
    elif heading == SP_LIB["2 o'clock"]:
        print("Signal Located at 2 o'Clock")
    elif heading == SP_LIB["1 o'clock"]:
        print("Signal Located at 1 o'Clock")
    elif heading == SP_LIB["12 o'clock"]:
        print("Signal Located at 12 o'Clock")
    elif heading == SP_LIB["11 o'clock"]:
        print("Signal Located at 11 o'Clock")
    elif heading == SP_LIB["10 o'clock"]:
        print("Signal Located at 10 o'Clock")
    elif heading == SP_LIB["9 o'clock"]:
        print("Signal Located at 9 o'Clock")
    else:
        print("Error")