import math

# Dictionary for the source file.
SP_LIB = {
    "DIST"      : 1,            # distance between antennas [meters]
    "BETA"      : 3.466,        # Beta for 165.5 MHz
    "LAMBDA"    : 1.826,        # wavelength for 165.5 MHz
    "3 o'clock" : 0,            # These are headings
    "2 o'clock" : 1,
    "1 o'clock" : 2,
    "12 o'clock": 3,
    "11 o'clock": 4,
    "10 o'clock": 5,
    "9 o'clock" : 6,
    "ERROR"     : 7             # This would mean that the signal was out of phase
}

# THIS FUNCTION WILL CONVERT THE DIGITAL VALUE TO ANALOG
def dig_2_ana(dig_value):
    analog_value = SP_LIB["REF_VOLT"] / SP_LIB["BIT_RES"] * dig_value
    analog_value = analog_value - SP_LIB["ANA_ADJ"]                     # Calibration: ADC reads 0.02 values higher
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
    theta = math.degrees(theta)
    return theta

# USE THE INFORMATION TO SHOW USER WHERE BACON (lol) SIGNAL IS
def dir_to_heading(degree, direction):
    if ((degree <= 15) and (degree >= 0)):
        return



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