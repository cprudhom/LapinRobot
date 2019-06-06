# coding: utf-8

import frontend.embedded_graph as graph
import backend.myGlobal as glob

from PyQt5.QtWidgets import QWidget, QPushButton, QGroupBox, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt5 import QtGui
from PyQt5 import QtCore


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.title = "Lapin Robot"
        self.top = 100
        self.left = 100
        self.width = 800
        self.height = 500
        self.icon_name = "public/img/rabbit-icon.png"

        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.icon_name))
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.make_menu()
        self.make_chart()

        window_layout = QVBoxLayout()
        window_layout.addWidget(self.menu)
        window_layout.addWidget(self.chart)

        self.setLayout(window_layout)

        self.set_events()

        self.show()


    def make_menu(self):
        self.menu = QGroupBox()
        menu_layout = QHBoxLayout()

        self.start_btn = self.create_button("Start", "public/img/play-icon.png")
        menu_layout.addWidget(self.start_btn)
        self.stop_btn = self.create_button("Stop", "public/img/stop-icon.png")
        menu_layout.addWidget(self.stop_btn)
        self.stop_btn.setDisabled(True)
        self.export_btn = self.create_button("Export", "public/img/export-icon.png")
        menu_layout.addWidget(self.export_btn)
        self.export_btn.setDisabled(True)

        self.menu.setMaximumHeight(65)
        self.menu.setLayout(menu_layout)

    def create_button(self, label, icon_name):
        button = QPushButton(label, self)
        button.setIcon(QtGui.QIcon(icon_name))
        button.setIconSize(QtCore.QSize(30, 30))
        button.setMinimumHeight(40)
        return button

    def make_chart(self):
        graph_width = 30
        graph_min_y = 0
        graph_max_y = 160
        self.chart = graph.DynamicChart(graph_width, graph_min_y, graph_max_y)


    def set_events(self):
        self.start_btn.clicked.connect(self.start)
        self.stop_btn.clicked.connect(self.stop)
        self.export_btn.clicked.connect(self.export)

    def start(self):
        self.start_btn.setDisabled(True)
        self.stop_btn.setEnabled(True)
        self.export_btn.setDisabled(True)

        self.chart.reinit_graph()
        glob.start(self.chart)

    def stop(self):
        self.start_btn.setEnabled(True)
        self.stop_btn.setDisabled(True)
        self.export_btn.setEnabled(True)

        glob.stop()

    def export(self):
        name = str(QFileDialog.getSaveFileName(self, 'Exporter', '', '*.txt')).split(",")[0][2:-1]+'.txt'
        glob.export(name.strip(), self.chart.xdata, self.chart.ydata)

    def closeEvent(self, event):
        self.stop()
        event.accept()