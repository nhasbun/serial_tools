## CONFIGURATION SCRIPT FOR HC-05
# AT command mode is needed for this to work

from serial   import Serial
from time     import sleep, time, strftime
from datetime import datetime


t = datetime.fromtimestamp(time())
DEVICE_NAME  = 'TAOTE ' + t.strftime('%d-%m-%Y %H:%M')
SET_BAUDRATE = 115200


def command(uart, command):
  print(command)
  command = command + '\r\n'
  command = command.encode()
  uart.write(command)
  print(uart.readline().decode("utf-8"))


def main():

  ## PARAMETERS ##
  BAUDRATE = 38400 # Factory baudrate for AT mode
  COM_PORT = 'COM31'

  uart = Serial(COM_PORT, BAUDRATE, timeout = 1)

  if (uart.is_open == False):
    uart.open()

  command(uart, 'AT')
  command(uart, 'AT+VERSION?')
  command(uart, 'AT+NAME=' + DEVICE_NAME)
  command(uart, 'AT+UART=' + str(SET_BAUDRATE) + ',0,0')

  print("Configuration routine complete")

  command(uart, 'AT+RESET')

  uart.close()


if __name__ == '__main__':
  main()
