# coding: utf-8

import serial
import serial.tools.list_ports
import time


class Arduino:

    def __init__(self, channels, port, baudrate, coeur, poumon, buzzer, mock):
        self.mock = mock
        if not self.mock:
            self.ser = serial.Serial(port=port, baudrate=baudrate)
        self.fs = {}
        ch = next(filter(lambda c: c['name'] == coeur, channels), None)
        if ch is not None:
            self.fs['fc'] = ch['id']
        ch = next(filter(lambda c: c['name'] == poumon, channels), None)
        if ch is not None:
            self.fs['fr'] = ch['id']
        ch = next(filter(lambda c: c['name'] == buzzer, channels), None)
        if ch is not None:
            self.fs['fd'] = ch['id']
        time.sleep(1)

    def arduino_communication(self, csts):
        fc, fr, fd = 90, 20, 75
        if 'fc' in self.fs:
            fc = csts[self.fs['fc']]
        if 'fr' in self.fs:
            fr = csts[self.fs['fr']]
        if 'fd' in self.fs:
            fd = csts[self.fs['fd']]

        msg = str(fc) + 'c' + \
              str(fr) + 'r' + \
              str(fd) + 'd'  # + str(75) +'f'

        if not self.mock:
            self.ser.write(msg.encode())
        else:
            print(msg)


def close(self):
    if not self.mock:
        self.ser.close()


if __name__ == "__main__":
    robot = Arduino('COM7', 20000)
    while True:
        robot.arduino_communication({'FC': 180.4, 'FR': 67.2})
