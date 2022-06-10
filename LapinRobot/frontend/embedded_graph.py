from collections import defaultdict

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FingureCanvas
from matplotlib.figure import Figure

import backend.myGlobal as glob

plt.ion()


class DynamicChart(FingureCanvas):
    def __init__(self, settings, width, parent=None):
        self.min_t = 0
        self.max_t = width
        self.graph_width = width
        self.margin_t = 0.1 * width

        glob.plot_channels = settings['plotting']['channels']
        channels = settings['data']['channels']
        self.fig, self.axes = plt.subplots(nrows=len(glob.plot_channels), ncols=1, squeeze=False) # squeeze=False to deal with 1 channel selected
        self.lines = defaultdict(list)
        glob.tdata = defaultdict(list)
        glob.ydata = defaultdict(list)
        for i in range(len(glob.plot_channels)):
            ch = next(filter(lambda c: c['name'] == glob.plot_channels[i], channels), None)
            ax = self.axes[i][0] # due to squeeze = False
            ax.set_ylabel(ch['description'])
            ax.set_xlabel("Temps (s)")
            ax.grid()
            ax.set_xlim(self.min_t, self.max_t + self.margin_t)
            bounds = ch['bounds']
            margin = 0.1 * (bounds[1] - bounds[0])
            ax.set_ylim(bounds[0] - margin, bounds[1] + margin)
            id = ch['id']
            glob.tdata[id] = [0]
            glob.ydata[id] = [0]
            self.lines[id], = self.axes[i][0].plot([], [], '-')

        FingureCanvas.__init__(self, self.fig)
        self.setParent(parent)



    def update_chart(self):
        for k in glob.tdata.keys():
            t = glob.tdata[k][-1]
            y = glob.ydata[k][-1]
            self.max_t = max(self.max_t, t)
            self.set_scale(t, y)

            glob.tdata[k].append(t)
            glob.ydata[k].append(y)
            self.lines[k].set_xdata(glob.tdata[k])
            self.lines[k].set_ydata(glob.ydata[k])

        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    def set_scale(self, t, y):
        self.max_t = max(t, self.max_t)
        self.min_t = self.max_t - self.graph_width
        for i in range(len(glob.tdata.keys())):
            self.axes[i][0].set_xlim(self.min_t, self.max_t + +self.margin_t)

        # if y > self.max_y:
        #    self.max_y = y
        #    self.axes.set_ylim(self.min_y, self.max_y + self.margin_y)

    def reinit_graph(self):
        for k in glob.tdata.keys():
            glob.tdata[k] = [0]
            glob.ydata[k] = [0]
        self.min_t = 0
        self.max_t = self.graph_width
        self.set_scale(0, 0)
