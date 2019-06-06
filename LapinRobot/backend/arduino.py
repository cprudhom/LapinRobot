# coding: utf-8

import backend.myGlobal as glob
import serial
import serial.tools.list_ports
import time
import struct


class Arduino:

    def __init__(self):
        path = self.get_serial_ports()
        self.ser = serial.Serial(path, baudrate=19200)
        time.sleep(1)

    def get_serial_ports(self):
        """ produce a list of all serial ports. The list contains a tuple with the port number,
        description and hardware address """
        ports = list(serial.tools.list_ports.comports())
        for i in range(len(ports)):
            port = ports.__getitem__(i)
            print(port.description)
            if port.description.__contains__("Mega 2560"):
                return port.device

    def communication_test(self):
        ready = False
        while not ready:
            self.ser.write(struct.pack('b', 0))
            recu = struct.unpack('b', self.ser.read())[0]
            if recu == 1:
                self.ser.write(struct.pack('b', 0))
            else:
                if recu == 0:
                    ready = True

    def send_data(self, values):
        for i in range(4):
            self.ser.write(struct.pack('B', values[i]))

    def arduino_communication(self, f_heart, f_breath, f_urea):
        values = [glob.state, f_urea, f_breath, f_heart]
        self.communication_test()
        self.send_data(values)

        substance = struct.unpack('b', self.ser.read())[0]
        if substance == 1:
            glob.state = 1
            glob.need_change_file = True
            print("Adrenaline")

    def close(self):
        self.ser.close()


if __name__ == "__main__":
    robot = Arduino()
    robot.get_serial_ports()
    while True:
        robot.arduino_communication(137, 122, 89)

