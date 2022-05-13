# Source Code for ALT_CODE
import math
import Library
# DICTIONARY FOR SOURCE FILE

# DIGITAL TO ANALOG CONVERTOR
def dig_2_ana(dig_value):
    analog_value = Library.MAIN_LIB["REF_VOLT"] / Library.MAIN_LIB["BIT_RES"] * dig_value
    return analog_value

# ANALOG TO PHASE OFFSET CONVERTOR
def volt_2_ph(voltage):
    # if half == Library.MAIN_LIB["FALLING_SLOPE"]:
    #     phase = abs(-94.786 * voltage + 177.15)
    #     print('Phase Offset = ', phase)
    #     return phase
    # elif half == Library.MAIN_LIB["RISING_SLOPE"]:
    #     #        phase = abs(94.476 * voltage - 177.44)                         # Original
    #     phase = abs(phase)

    # NEW VERSION. AS VOLTAGE INCREASES SO DOES PHASE OFFSET
    phase = abs(94.476 * voltage)

    # SET SOME LIMITS
    if phase > 180:
        phase = 180

    elif phase < 0:
        phase = 0

    return phase

def phase_offset_calculation(index, current_phase, calibrated_phase):
    if index == Library.MAIN_LIB["CENTER_REGION"]:
        phase_offset = abs(calibrated_phase - current_phase)
        return phase_offset

    elif index == Library.MAIN_LIB["UPPER_REGION"]:
        # SINCE THIS IS A PEAK, THE CONTRIBUTION IS OFF BY 180 DEGREES THAT IS WHY WE HAVE A 180 - CURRENT PHASE MEASUREMENTS
        phase_offset = (Library.MAIN_LIB["DEFAULT_PH_SH_UP"] - calibrated_phase) + (180 - current_phase)
        return phase_offset

    elif index == Library.MAIN_LIB["LOWER_REGION"]:
        # THIS IS THE TROPH OUTPUT OF AD83O2 THEREFORE THE CONTRIBUTION OF PHASE OFFSET IS
        # A SIMPLE ADDITION
        phase_offset = (calibrated_phase + current_phase)
        return phase_offset


# PHASE ARRAY CALCULATION: (Relative to drone's flying direction)
def Phase_array_calc(phase):
    phase = math.radians(phase)
    theta = (phase * Library.MAIN_LIB["NUM_ELEM"] * Library.MAIN_LIB["LAMBDA"]) / (2 * math.pi * Library.MAIN_LIB["DIST"])  # General Equation for Phase Array
    theta = math.asin(theta)                                                                # Inverse Sine in radians
    theta = theta * 180 / math.pi                                                           # Convert to Degrees
    return theta

# USE THE INFORMATION TO SHOW USER WHERE BACON (lol) SIGNAL IS
def dir_to_heading(degree, direction):
    if (degree <= 15) and (degree >= 0):
        return Library.MAIN_LIB["12 o'clock"]                     # Don't need to worry about magnitude

    if direction >= 0:                                  # Test if beacon signal is to the left
        if (degree > 15) and (degree <= 45):
            return Library.MAIN_LIB["11 o'clock"]
        elif (degree > 45) and (degree <= 75):
            return Library.MAIN_LIB["10 o'clock"]
        elif (degree > 75) and (degree <= 90):
            return Library.MAIN_LIB["9 o'clock"]

    if direction < 0:                                   # Signal to the right
        if (degree > 15) and (degree <= 45):
            return Library.MAIN_LIB["1 o'clock"]
        elif (degree > 45) and (degree <= 75):
            return Library.MAIN_LIB["2 o'clock"]
        elif (degree > 75) and (degree <= 90):
            return Library.MAIN_LIB["3 o'clock"]

# This will display to the user where the heading is
def dis_head(heading):
    if heading == Library.MAIN_LIB["3 o'clock"]:
        print("Signal Located at 3 o'Clock")
    elif heading == Library.MAIN_LIB["2 o'clock"]:
        print("Signal Located at 2 o'Clock")
    elif heading == Library.MAIN_LIB["1 o'clock"]:
        print("Signal Located at 1 o'Clock")
    elif heading == Library.MAIN_LIB["12 o'clock"]:
        print("Signal Located at 12 o'Clock")
    elif heading == Library.MAIN_LIB["11 o'clock"]:
        print("Signal Located at 11 o'Clock")
    elif heading == Library.MAIN_LIB["10 o'clock"]:
        print("Signal Located at 10 o'Clock")
    elif heading == Library.MAIN_LIB["9 o'clock"]:
        print("Signal Located at 9 o'Clock")
    else:
        print("Error")