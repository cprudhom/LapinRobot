import frontend.embedded_graph as graph
import backend.myGlobal as Glob
from frontend import interface
import yaml
from backend import arduino, data_file

import sys
from PyQt5.QtWidgets import (QLabel, QRadioButton, QPushButton, QVBoxLayout, QApplication, QWidget)
from PyQt5.QtWidgets import QWidget, QPushButton, QGroupBox, QVBoxLayout, QHBoxLayout, QFileDialog, QComboBox
from PyQt5 import QtGui
from PyQt5 import QtCore


class basicRadiobuttonExample(QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):

        self.icon_name = "public/img/rabbit-icon.png"

        self.label = QLabel('Dans quel mode de fonctionement voulez-vous être ?')
        self.rbtn1 = QRadioButton('Cardio respiratoire')
        self.rbtn2 = QRadioButton('Cardio rénale')
        self.label2 = QLabel("")

        self.rbtn1.toggled.connect(self.start1)
        self.rbtn2.toggled.connect(self.start2)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.rbtn1)
        layout.addWidget(self.rbtn2)
        layout.addWidget(self.label2)

        self.setGeometry(200, 200, 500, 200)

        self.setLayout(layout)
        self.title = "Lapin Robot"
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.icon_name))

        self.show()

    def onClicked(self):
        radioBtn = self.sender()
        if radioBtn.isChecked():
            self.label2.setText("Vous avez choisi " + radioBtn.text() + "  (developpement en cours)")


    def start1(self):
        # 1. Load configuration
        with open('config.yaml', 'r') as file:
            settings = yaml.safe_load(file)

        # 3. Start app
        Glob.window = interface.Window(settings)

    def start2(self):
        # 1. Load configuration
        with open('config2.yaml', 'r') as file:
            settings = yaml.safe_load(file)

        # 3. Start app
        Glob.window = interface.Window(settings)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = basicRadiobuttonExample()
    sys.exit(app.exec_())

