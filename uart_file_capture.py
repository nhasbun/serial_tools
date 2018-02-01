## Script para capturar archivos o datos entrantes por puerto serial

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
DATASIZE = 26240 # bytes

PORT = 'COM30'

in_buf = bytes('', 'utf-8') # buffer de entrada de datos, el limite en windows
# por driver es 4096 y necesitamos expandir esto

## Thread control
t = "dummy"
run = True

# worker de thread
def worker(dummy, ser):
  global in_buf
  global run

  reporte_tiempo = True
  timer_iniciado = False

  print("worker starting...")
  while(run):
    in_buf += ser.read(ser.inWaiting())
    lenbuf = len(in_buf)
    if (lenbuf > 0 and timer_iniciado == False):
      t_init = time.clock()
      timer_iniciado = True
      print("tic...")
    if (lenbuf == DATASIZE and reporte_tiempo == True):
      t_end = time.clock()
      print("tiempo envio:", t_end - t_init)
      reporte_tiempo = False
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
  timeout_count = 0 # Para llevar la cuenta de segundos sin recibir datos

  while(True):
    time.sleep(1)
    n_datos = len(in_buf)

    if (n_datos != n_datos_old):
      print(n_datos, " en el buffer", end = '\r')

    # rutina que revisa si se terminó la recepción de datos, se genera un
    # se genera un timeout counter para salir del script
    elif (n_datos == n_datos_old) & (n_datos > 0):
      timeout_count += 1

    n_datos_old = n_datos
    if(timeout_count == 3):
      exit_script()

def exit_script():
  global run
  global t

  print("\nInterrupted")
  run = False
  t.join()

  print("****************************")
  print("Data MD5 Hash")
  hash_object = hashlib.md5(in_buf)
  print(hash_object.hexdigest())
  print("****************************")

  file = open("frame_received.jpg", "wb")
  file.write(in_buf)
  file.close()

  try:
    sys.exit(0)
  except SystemExit:
    os._exit(0)

# main()
if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    exit_script()

