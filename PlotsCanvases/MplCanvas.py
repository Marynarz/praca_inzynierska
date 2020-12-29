import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None):
        self.now_x = 10
        self.now_y = 10
        self.dpi = 100
        figure = Figure(figsize=(self.now_x, self.now_y), dpi=self.dpi)
        self.axes = figure.add_subplot(111)
        FigureCanvasQTAgg.__init__(self, figure)
        self.setParent(parent)
        self.grid = False

        FigureCanvasQTAgg.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

    def upload_data(self, x, y):
        self.axes.cla()
        self.axes.plot(x, y)
        self.draw()
        self.now_x = x
        self.now_y = y

    def show(self):
        self.grid = not self.grid
        self.axes.cla()
        self.axes.plot(self.now_x, self.now_y)
        self.axes.grid(self.grid)
        self.draw()

    def set_grid(self):
        pass

    def set_line(self):
        pass
