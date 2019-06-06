# coding: utf-8

from frontend import interface
from backend import arduino, data_file
import backend.myGlobal as glob
import time

import sys
from PyQt5.QtWidgets import QApplication




def main():
    glob.start, glob.stop, glob.export = start, stop, export
    glob.running = False
    glob.robot = arduino.Arduino()
    glob.app = QApplication(sys.argv)
    glob.window = interface.Window()
    sys.exit(glob.app.exec_())
    reset_t0()


def start(chart):
    print("Started")
    glob.running = True
    glob.state = 0 #  reinit
    glob.adrenaline_running, glob.acetylcholine_running, glob.need_change_file = False, False, False
    data = data_file.DataFile()
    reset_t0()

    while glob.running:
        t = get_time()
        data_line = data.get_data(t)
        f_heart, f_breath, f_urea = int(data_line[4]), int(6000/data_line[5]), 10
        glob.robot.arduino_communication(f_heart, f_breath, f_urea)
        chart.update_chart(t/1000, data_line[1]-data.delta_files)
        time.sleep(0.01)


def stop():
    print("Stopped")
    glob.running = False


def export(name, xdata, ydata):
    if name != ".txt":
        if name[-8:] == ".txt.txt":
            name = name[:-4]
        file = open(name, "w")
        #file.write("t (ms)\tPression Arterielle\n")
        for i in range(len(glob.tdata)):
            line = str(glob.tdata[i]) + "\t" + str(glob.ydata[i]) + "\n"
            file.write(line)
        file.close()
        print("Exported with success")
    else:
        print("Export aborted")


def get_time():
    return int(round(time.time() * 1000) - glob.t0)


def reset_t0():
    glob.t0 = int(round(time.time() * 1000))


if __name__ == "__main__":
    main()
