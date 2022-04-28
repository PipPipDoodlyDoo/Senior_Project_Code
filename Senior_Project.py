import math

# Dictionary for the source file.
SP_LIB = {
    "REF_VOLT"  : 3.3,                          # Reference Voltage for ADC
    "BIT_RES"   : 65535,                        # Bit Resolution for ADC
    "DIST"      : 0.076,                        # distance between antennas [meters] (76 cm)
    "BETA"      : 3.466,                        # Beta for 165.5 MHz
    "LAMBDA"    : 1.826,                        # wavelength for 165.5 MHz
    "3 o'clock" : 0,                            # direction headings
    "2 o'clock" : 1,
    "1 o'clock" : 2,
    "12 o'clock": 3,
    "11 o'clock": 4,
    "10 o'clock": 5,
    "9 o'clock" : 6,
    "ERROR"     : 7
}

# THIS FUNCTION WILL CONVERT THE DIGITAL VALUE TO ANALOG
def dig_2_ana(dig_value):
    analog_value = SP_LIB["REF_VOLT"] / SP_LIB["BIT_RES"] * dig_value
    print("\nAnalog Voltage: ", '{:2f}'.format(analog_value))         # print out the analog voltage
    return analog_value

# CONVERT ANALOG VOLTAGE TO PHASE ACCORDING TO AD8302 (really can use either or)
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

# CALCULATE ANGEL OF PLANE'S TRAVELING DIRECTION TO BEACON SIGNAL POSITION
def Phase_array_calc(phase):
    theta = math.asin(math.radians((phase * SP_LIB["LAMBDA"]) / (360 * SP_LIB["DIST"])))
    theta = math.degrees(theta) * 2
    return theta

# USE THE INFORMATION TO SHOW USER WHERE BACON (lol) SIGNAL IS
def dir_to_heading(degree, direction):
    if ((degree <= 15) and (degree >= 0)):
        return SP_LIB["12 o'clock"]                     # Dont need to worry about magnitude

    if (direction >= 0):                                # Test if beacon signal is to the left
        if ((degree > 15) and (degree <= 45)):
            return SP_LIB["11 o'clock"]
        elif ((degree > 45) and (degree <= 75)):
            return SP_LIB["10 o'clock"]
        elif ((degree > 75) and (degree <= 90)):
            return SP_LIB["9 o'clock"]

    if (direction < 0):                                 # Signal to the right
        if ((degree > 15) and (degree <= 45)):
            return SP_LIB["1 o'clock"]
        elif ((degree > 45) and (degree <= 75)):
            return SP_LIB["2 o'clock"]
        elif ((degree > 75) and (degree <= 90)):
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