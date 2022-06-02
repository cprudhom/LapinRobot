# coding: utf-8

import backend.myGlobal as glob

import os
import random as rd
import pandas as pd
import time
import numpy as np


class DataFile:

    def __init__(self, filename=None):
        glob.initFile = None
        if (filename is None):
            self.get_random_file()
        else:
            self.filename = filename
        self.open_file()
        glob.rest_file_name = self.filename

    def get_random_file(self):
        directory = self.get_directory()
        files = os.listdir(directory)
        if glob.debug:
            self.filename = directory + "test.csv"
        else:
            self.filename = directory + rd.choice(files)
        while not self.filename.endswith(".csv"):
            self.filename = directory + rd.choice(files)

    def get_directory(self):
        if glob.state == glob.State.Adrenaline and glob.need_change_file:
            directory = "./public/data/adrenaline/"
        elif glob.state == glob.State.Acetylcholine and glob.need_change_file:
            directory = "./public/data/acetylcholine/"
        else:
            directory = "./public/data/rest/"
        glob.need_change_file = False
        return directory

    def open_file(self):
        self.data = pd.read_csv(self.filename, sep=";")
        print(self.data)
        print(self.data.index)
        print(self.data.columns)
        print(self.data.shape)
        self.line_number = 1
        self.nb_of_lines = len(self.data)

    def change_file(self):
        if glob.state == glob.State.Rest:
            self.filename = glob.rest_file_name
        else:
            self.get_random_file()

        self.open_file()

    def get_data(self):
        self.check_event()
        cstes = {o.name: 0 for o in glob.Observation}
        for _ in range(glob.NUMBER_OF_LINES):
            for o in glob.Observation:
                cstes[o.name] += self.data.loc[self.line_number, o.name]
            self.line_number += 1
        for o in glob.Observation:
            cstes[o.name] /= glob.NUMBER_OF_LINES
        cstes['TT'] = glob.NUMBER_OF_LINES * glob.FREQUENCY  # time in ms
        return cstes

    def check_event(self):
        if (self.line_number + glob.NUMBER_OF_LINES > len(self.data)):
            glob.state = glob.State.Rest
            glob.window.rest_back()
            glob.need_change_file = True

        if glob.need_change_file:
            self.change_file()
            glob.need_change_file = False


if __name__ == "__main__":
    print("-------------------------")
    for i in range(5):
        data = DataFile(filename="../public/data/rest/test.csv")
        print("FICHIER: ", data.filename[15:])
        t0 = time.time()
        dict = data.get_data()
        print(dict)
