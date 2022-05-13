import Library

def clear_screen():
    print("\u001b[2J")                  # Clear the screen
    print("\u001b[H")                   # Move the cursor to the top corner

def calibration_layout():
    print(" Begin Calibration Process.\n\n Please place the Transmitter in the 12 o'click position.")
    print('\n Initial Phase Offset:       degrees')
    print('\n Initial Magnitude Value:      V')