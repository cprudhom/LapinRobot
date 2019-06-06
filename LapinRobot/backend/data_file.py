# coding: utf-8

import backend.myGlobal as glob


import os
import random as rd
import scipy.signal as sgn
import time
import numpy as np

class DataFile:
    PEAK_BUFFER_TIME = 5000  # ms - duration of the buffer to calculate peaks


    def __init__(self):
        self.get_random_file()
        self.previous_lines = 0
        self.compt=0
        self.delta_files = 0

        # for find_peaks (operational but need to set parameters) :
        # self.t_peak_buffer, self.y_peak_buffer = self.init_peak_buffer()
        # self.peaks = self.get_peaks()

    def get_random_file(self):
        directory = self.get_directory()
        files = os.listdir(directory)
        self.filename = directory + rd.choice(files)
        while not self.filename.endswith(".txt"):
            self.filename = directory + rd.choice(files)
        self.file = open(self.filename, "r")
        self.line_number = 0
        self.file_peaks = open(self.filename, "r")
        self.line_number_peaks = 0
        print("Data File :   ", self.filename)

    def get_directory(self):
        if glob.state == 1 and glob.need_change_file:
            directory = "./public/data/adrenaline/"
        elif glob.state == 2 and glob.need_change_file:
            directory = "./public/data/acetylcholine/"
        else:
            directory = "./public/data/repos/"
        glob.need_change_file = False
        return directory

    def change_file(self):
        self.close()
        self.get_random_file()
        self.set_delta_files()

    def close(self):
        self.previous_lines += self.line_number
        self.file.close()
        self.file_peaks.close()

    def get_data(self, t):
        self.check_event()
        line = self.file.readline()
        while self.line_number < t-self.previous_lines and line:
            self.line_memory = line
            line = self.file.readline()
            self.line_number += 1

        if not line:
            self.change_file()
            glob.state = 0
            line = self.line_memory  # we return the last line of the file

        return self.format_line(line)

    def set_delta_files(self):
        #function to be optimized, and surely use the find_peaks buffer when operationnal
        if len(glob.tdata) > 0:
            t = glob.tdata[-1]
            i = -2
            while t-glob.tdata[-1]<3000 and -i<len(glob.tdata):
                i -= 1
            last_average_value = np.average(glob.ydata[i:])
        first_values = []
        with open(self.filename) as fp:
            first_values.append(self.format_line(fp.readline())[1])
        first_average_value = np.average(first_values)
        self.delta_files = first_average_value - last_average_value

    def format_line(self, line):
        line = line.replace(',', '.')
        line = line.split()
        line = [float(line[i]) for i in range(glob.NB_PARAMETERS)]
        return line

    def check_event(self):
        if glob.need_change_file:
            self.change_file()
            glob.need_change_file = False

    # For find_peaks()
    def init_peak_buffer(self):
        t = []
        y = []
        for i in range(self.PEAK_BUFFER_TIME):
            line = self.file_peaks.readline()
            line = self.format_line(line)
            t.append(line[0])
            y.append(line[1])
            self.line_number_peaks += 1
        return t, y

    def get_peaks(self):
        while self.line_number_peaks <= self.line_number + self.PEAK_BUFFER_TIME:
            self.t_peak_buffer = self.t_peak_buffer[1:]
            self.y_peak_buffer = self.y_peak_buffer[1:]
            line = self.file_peaks.readline()
            line = self.format_line(line)
            self.t_peak_buffer.append(line[0])
            self.y_peak_buffer.append(line[1])
            self.line_number_peaks += 1

        return sgn.find_peaks(self.y_peak_buffer, distance=280)[0]

    def get_heart_frenquency(self):
        self.get_peaks()
        gaps = [(self.peaks[i+1]-self.peaks[i])/1000 for i in range(len(self.peaks)-1)]
        return 1/np.mean(gaps)





if __name__ == "__main__":
    print("-------------------------")
    for i in range(5):
        data = DataFile("../public/data/adrenaline/")
        print("FICHIER: ", data.filename[15:])
        t0 = time.time()
        peaks = data.get_peaks()
        t1 = time.time()

        print("DURATION GET_PEAKS: ", (t1-t0)*1000, " ms")
        print("FREQUENCY = ", int(data.get_heart_frenquency()*60), "BPM")
        print("-------------------------")
