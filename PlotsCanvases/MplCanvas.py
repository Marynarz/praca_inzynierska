import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, x=10, y=10, dpi=100):
        figure = Figure(figsize=(x, y), dpi=dpi)
        self.axes = figure.add_subplot(111)
        FigureCanvasQTAgg.__init__(self, figure)
        self.setParent(parent)
        self.now_x = [x]
        self.now_y = [y]
        self.grid = False

        FigureCanvasQTAgg.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

    def update_canvas(self, x, y):
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

