## Herramienta sencilla para detectar cantidad de bytes entrantes
# por puerto serial

from functions.serial_ports import *
import serial
import threading
import time
import sys
import os
import hashlib

## Parameters
# BAUDRATE = 1041666
BAUDRATE = 115200

PORT = 'COM5'

in_buf = bytes('', 'utf-8') # buffer de entrada de datos, el limite en windows
# por driver es 4096 y necesitamos expandir esto

## Thread control
t = "dummy"
run = True

# worker de thread
def worker(dummy, ser):
  global in_buf
  global run

  print("worker starting...")
  while(run):
    in_buf += ser.read(ser.inWaiting())
  print("worker stop...")

# funcion principal
def main():
  global in_buf
  global t

  ser = serial.Serial(PORT, BAUDRATE, timeout = 1)
  ser.reset_input_buffer() # se limpia buffer por seguridad
  print("** Buffer Cleaned **")

  # Thread para ir sacando elementos del buffer
  t = threading.Thread(target=worker, args = (0, ser))
  t.start()

  # Loop para revisar cantidad de elementos en buffer de userspace
  n_datos_old = 0
  while(True):
    time.sleep(1)
    n_datos = len(in_buf)

    if(n_datos != n_datos_old):
      print(n_datos, " en el buffer", end = '\r')

    n_datos_old = n_datos

# main()
if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print("\nInterrupted")
    run = False
    t.join()

    print("****************************")
    print("Data MD5 Hash")
    hash_object = hashlib.md5(in_buf)
    print(hash_object.hexdigest())
    print("****************************")
    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)

