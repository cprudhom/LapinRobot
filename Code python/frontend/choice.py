import frontend.embedded_graph as graph
import backend.myGlobal as Glob
from frontend import interface
import yaml
from backend import arduino, data_file

import sys
from PyQt5.QtWidgets import (QLabel, QPushButton, QVBoxLayout, QApplication, QWidget)
from PyQt5.QtWidgets import QWidget, QPushButton, QGroupBox, QVBoxLayout, QHBoxLayout, QFileDialog, QComboBox
from PyQt5 import QtGui
from PyQt5 import QtCore


class Selection(QWidget):

    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.init_ui()

    def init_ui(self):
        self.icon_name = "public/img/rabbit-icon.png"
        layout = QVBoxLayout()
        self.setLayout(layout)

        #self.label = QLabel('Mode de fonctionnement :')
        #layout.addWidget(self.label)

        button = QPushButton('cardiorespi')
        button.clicked.connect(lambda: self.start('cardiorespi'))
        layout.addWidget(button)

        button = QPushButton('cardiorenale')
        button.clicked.connect(lambda: self.start('cardiorenale'))
        layout.addWidget(button)

        self.setGeometry(200, 200, 500, 200)

        self.title = "Lapin Robot"
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.icon_name))

        self.show()

    def start(self, name):
        print('Start', name)
        Glob.data = data_file.DataFile(**self.settings['data'][name])
        Glob.plot_channels = self.settings['data'][name]['plotting']
        Glob.data.init()
        Glob.running = False
        Glob.robot = arduino.Arduino(channels=self.settings['data'][name]['channels'],
                                     port=self.settings['arduino']['port'],
                                     baudrate=self.settings['arduino']['baudrate'],
                                     coeur=self.settings['data'][name]['coeur'],
                                     poumon=self.settings['data'][name]['poumon'],
                                     buzzer=self.settings['data'][name]['buzzer'],
                                     mock=self.settings['arduino']['port']
                                     )

        Glob.window = interface.Window(self.settings['data'][name]['channels'])
        self.close()
