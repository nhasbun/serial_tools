## CONFIGURATION SCRIPT FOR HC-05
# AT command mode is needed for this to work

from serial   import Serial
from time     import sleep, time, strftime
from datetime import datetime
from os       import urandom # fn que genera un numero aleatorio de n bytes
from binascii import b2a_hex # fn que convierte de bytes a hexadecimal

## PARAMETERS ##
BAUDRATE     = 38400 # Factory baudrate for AT mode
COM_PORT     = 'COM31'
DEVICE_NAME  = 'TAOTE '
DEVICE_ID    = b2a_hex(urandom(4)).decode('utf-8')
SET_BAUDRATE = 115200


# ****************************************************************************
# *    Función general para escribir comandos AT y esperar una respuesta.    *
# ****************************************************************************

def command(uart, command):
  print(command)
  command = command + '\r\n'
  command = command.encode()
  uart.write(command)
  print(uart.readline().decode('utf-8'))


# ****************************************************************************
# *                                   MAIN                                   *
# ****************************************************************************

def main():

  uart = Serial(COM_PORT, BAUDRATE, timeout = 1)

  if (uart.is_open == False):
    uart.open()

  command(uart, 'AT')
  command(uart, 'AT+VERSION?')
  command(uart, 'AT+NAME=' + DEVICE_NAME + DEVICE_ID)
  command(uart, 'AT+UART=' + str(SET_BAUDRATE) + ',0,0')

  print("Configuration routine complete")

  command(uart, 'AT+RESET')

  uart.close()


if __name__ == '__main__':
  main()
