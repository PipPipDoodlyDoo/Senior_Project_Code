# DICTIONARY "LIBRARY OF VARIABLES THAT WILL BE USED"
MAIN_LIB = {
    "ADC_Ch_0"          : 26,                           # Phase Channel
    "ADC_Ch_1"          : 27,                           # Magnitude Channel
    "ADC_Ch_2"          : 28,                           # Extra ADC Channel
    "cal_in_pin"        : 18,                           # Calibration Input Pin
    "cal_out_pin"       : 20,                           # Calibration Output Pin
    "CONFIRM_OUT_PIN"   : 14,                           # Confirmation Output Pin for Pre-Measurement Protocol
    "CONFIRM_IN_PIN"    : 15,                           # Confirmation Input Pin for Pre-Measurement Protocol
    "DEBUG_OUT_PIN"     : 10,
    "DEBUG_IN_PIN"      : 11,
    "PAUSE_TIME"        : 100,
    # Reference Pin
    "RISING_SLOPE"      : 1,
    "FALLING SLOPE"     : 0,
    "UPPER_VOLT_THRES"  : 1.65,                         # Threshold Voltages for Phase Output of AD8302
    "LOWER_VOLT_THRES"  : 0.15,
    "DEFAULT_PH_SHIFT"  : 0,                            # Default Phase Shift used for forcing overlapping elements to 0
    "DEFAULT_PH_SH_UP"  : 180,                          #
    "CENTER_REGION"     : 0,                            # No overlap
    "UPPER_REGION"      : 1,                            # Overlap on the phase lead
    "LOWER_REGION"      : -1,                           # Overlap on Phase Lag sides
    "DEBOUNCE_SL"       : 1,                            # Debounce sleeping time
    "MAG_SAMPLES"       : 15,                            # Amount of samples taken'
    "MAG_BUFFER"        : 0.1,                           # Buffer Voltage to check for the overlap. Use with UPPER AND LOWER THRESHOLD VOLTAGES
    "REF_VOLT"          : 3.3,                      # Reference Voltage for ADC
    "BIT_RES"           : 65535,                    # A bit of Resolution for ADC
    "DIST"              : 1.65,                     # distance between antennas [meters] (76 cm)
    "BETA"              : 3.466,                    # Beta for 165.5 MHz
    "LAMBDA"            : 1.812,                    # wavelength for 165.5 MHz
    "NUM_ELEM"          : 2,                        # Number of Elements
    "3 o'clock"         : 0,                        # direction headings
    "2 o'clock"         : 1,
    "1 o'clock"         : 2,
    "12 o'clock"        : 3,
    "11 o'clock"        : 4,
    "10 o'clock"        : 5,
    "9 o'clock"         : 6,
    "ERROR"             : 7
}