# coding: utf-8

import backend.myGlobal as glob
import serial
import serial.tools.list_ports
import time
import struct


class Arduino:

    def __init__(self):
        self.ser = serial.Serial(path=glob.path, baudrate=glob.baudrate)
        time.sleep(1)

    def arduino_communication(self, csts):
        msg = str(csts['FC']) + 'c' + str(csts['FR']) + 'r'
        print(msg)
        self.ser.write(msg.encode())

    def close(self):
        self.ser.close()


if __name__ == "__main__":
    robot = Arduino()
    while True:
        robot.arduino_communication({'FC': 180.4, 'FR': 67.2})
