from machine import UART

hi_bit = 104
lo_bit = 105

uart = UART(0,115200)

uart.write(hi_bit,lo_bit)
