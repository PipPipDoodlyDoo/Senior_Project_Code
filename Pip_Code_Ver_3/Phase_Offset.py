# Modular Code for Version 3

#####################################################
# Used to calculate the phase offset
#####################################################

# CONVERT ANALOG VOLTAGE TO PHASE ACCORDING TO AD8302 (really can use either or)
def volt_2_ph(voltage, half):
    if half == 1:
        phase = abs(-94.786 * voltage + 177.15)
        print('Phase Offset = ', phase)
        return phase
    elif half == 0:
        phase = abs(94.476 * voltage - 177.44)
        phase = abs(phase)
        print('Phase Offset = ', phase)
        return phase
    