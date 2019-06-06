import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FingureCanvas
from matplotlib.figure import Figure

import backend.myGlobal as glob

plt.ion()


class DynamicChart(FingureCanvas):
    def __init__(self, width, min_y, max_y, parent=None):
        self.min_t = 0
        self.max_t = width
        self.min_y = min_y
        self.max_y = max_y
        self.graph_width = width
        self.margin_t = 0.1 * width
        self.margin_y = 0.1 * (max_y - min_y)

        figure = Figure()
        self.axes = figure.add_subplot(111)
        self.axes.set_title("Pression Artérielle")
        self.axes.set_xlabel("Temps (s)")
        self.axes.set_ylabel("PA (mmHg)")

        self.axes.grid()
        self.axes.set_xlim(self.min_t, self.max_t + self.margin_t)
        self.axes.set_ylim(self.min_y - self.margin_y, self.max_y + self.margin_y)

        FingureCanvas.__init__(self, figure)
        self.setParent(parent)

        self.lines, = self.axes.plot([], [], '-')

    def update_chart(self, t, y):
        self.max_t = max(self.max_t, t)
        self.set_scale(t, y)

        glob.tdata.append(t)
        glob.ydata.append(y)
        self.lines.set_xdata(glob.tdata)
        self.lines.set_ydata(glob.ydata)

        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    def set_scale(self, t, y):
        self.max_t = max(t, self.max_t)
        self.min_t = self.max_t - self.graph_width
        self.axes.set_xlim(self.min_t, self.max_t + +self.margin_t)

        if y > self.max_y:
            self.max_y = y
            self.axes.set_ylim(self.min_y, self.max_y + self.margin_y)

    def reinit_graph(self):
        glob.tdata = []
        glob.ydata = []
        self.min_t = 0
        self.max_t = self.graph_width
        self.set_scale(0, 0)
