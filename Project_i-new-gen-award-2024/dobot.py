# dobot.py
#! /usr/bin/python3
from pydobot import Dobot
import serial.tools.list_ports

# Movement limits
X_LIMITS = (0, 250)
Y_LIMITS = (0, 250)
Z_LIMITS = (-10, 150)

# Connect to Dobot
def connect():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        print(port)

    serial_port = '/dev/ttyUSB0'  # Ensure this port is correct
    global dobot
    dobot = Dobot(port=serial_port, verbose=True)
    dobot.suck(False)  # Disable vacuum
    dobot.move_to(200, -20, 30, 0)  # Move to HOME position
    return dobot

def is_within_limits(x, y, z):
    return (X_LIMITS[0] <= x <= X_LIMITS[1] and
            Y_LIMITS[0] <= y <= Y_LIMITS[1] and
            Z_LIMITS[0] <= z <= Z_LIMITS[1])

def GoLeft():
    (x, y, z, r, j1, j2, j3, j4) = dobot.pose()
    y += 20
    if is_within_limits(x, y, z):
        dobot.move_to(x, y, z, r)
        print("Moved Left")
    else:
        dobot.move_to(200, -20, 30, 0)

def GoRight():
    (x, y, z, r, j1, j2, j3, j4) = dobot.pose()
    y -= 20
    if is_within_limits(x, y, z):
        dobot.move_to(x, y, z, r)
        print("Moved Right")
    else:
        dobot.move_to(200, -20, 30, 0)

def GoUp():
    (x, y, z, r, j1, j2, j3, j4) = dobot.pose()
    z += 20
    if is_within_limits(x, y, z):
        dobot.move_to(x, y, z, r)
        print("Moved Up")
    else:
        dobot.move_to(200, -20, 30, 0)

def GoDown():
    (x, y, z, r, j1, j2, j3, j4) = dobot.pose()
    z -= 20
    if is_within_limits(x, y, z):
        dobot.move_to(x, y, z, r)
        print("Moved Down")
    else:
        dobot.move_to(200, -20, 30, 0)

if __name__ == '__main__':
    dobot = connect()
    try:
        while True:
            pass  # Wait for commands from app.py
    except KeyboardInterrupt:
        print("Exiting...")
