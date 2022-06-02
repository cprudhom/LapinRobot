# coding: utf-8

from frontend import interface
from backend import arduino, data_file
import backend.myGlobal as glob
import time

import sys
from PyQt5.QtWidgets import QApplication


def main():
    glob.start, glob.inject, glob.stop, glob.export = start, inject, stop, export
    glob.running = False
    glob.robot = arduino.Arduino()
    glob.app = QApplication(sys.argv)
    glob.window = interface.Window()
    sys.exit(glob.app.exec_())


def start(chart):
    print('Start')
    glob.running = True
    glob.state = glob.State.Rest  # reinit
    data = data_file.DataFile()
    t = 0
    cur_tim = time.time_ns()
    while glob.running:
        csts = data.get_data()
        print(csts)
        real_sleep_duration = (cur_tim + glob.TIME_TO_WAIT - time.time_ns()) / glob.IN_NS
        time.sleep(real_sleep_duration)

        glob.robot.arduino_communication(csts)
        t += csts['TT']
        chart.update_chart(t, csts['FC'])
        cur_tim = time.time_ns()


def inject(molecule):
    print("Inject", molecule)
    glob.state = glob.State[molecule]
    glob.need_change_file = True


def stop():
    print("Stopped")
    glob.running = False


def export(name, xdata, ydata):
    if name != ".txt":
        if name[-8:] == ".txt.txt":
            name = name[:-4]
        file = open(name, "w")
        # file.write("t (ms)\tPression Arterielle\n")
        for i in range(len(glob.tdata)):
            line = str(glob.tdata[i]) + "\t" + str(glob.ydata[i]) + "\n"
            file.write(line)
        file.close()
        print("Exported with success")
    else:
        print("Export aborted")



if __name__ == "__main__":
    main()
