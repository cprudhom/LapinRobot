# coding: utf-8

import serial
import serial.tools.list_ports
import time


class Arduino:

    def __init__(self, port, baudrate):
        self.ser = serial.Serial(port=port, baudrate=baudrate)
        time.sleep(1)

    def arduino_communication(self, csts):
        msg = str(csts['FC']) + 'c' + str(csts['FR']) + 'r'
        print(msg)
        self.ser.write(msg.encode())

    def close(self):
        self.ser.close()


if __name__ == "__main__":
    robot = Arduino('COM7', 20000)
    while True:
        robot.arduino_communication({'FC': 180.4, 'FR': 67.2})
