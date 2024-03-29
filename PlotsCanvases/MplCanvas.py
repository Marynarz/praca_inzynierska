import pandas as pd
from defs.app_defs import PlotTypes
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from PyQt5 import QtWidgets
import matplotlib
matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, grid=False):
        self.data = pd.DataFrame((0, 0))
        self.title = ''
        self.histogram = False
        self.now_x = []
        self.now_y = []
        self.x_idx = 1
        self.y_idx = 1
        self.plot_type = PlotTypes.D2_CHART
        self.dpi = 100
        figure = Figure(figsize=(10, 10), dpi=self.dpi)
        self.axes = figure.add_subplot(111)
        FigureCanvasQTAgg.__init__(self, figure)
        self.setParent(parent)
        self.grid = grid
        self.clear_plot()
        self.show_plot()

        FigureCanvasQTAgg.setSizePolicy(
            self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

    def upload_data(self, data):
        self.data = data

    def show_plot(self):
        self.clear_plot()
        if self.plot_type == PlotTypes.D2_CHART:
            self.data.plot(ax=self.axes, title=self.title)
            if self.histogram:
                self.data.hist()
        elif self.plot_type == PlotTypes.BAR_CHART:
            self.data.plot.bar(
                ax=self.axes, x=self.data.columns[self.now_x].name, y=self.data.columns[self.now_y].name, title=self.title)
        elif self.plot_type == PlotTypes.PIE_CHART:
            self._check_validate_y()
            self.data.plot.pie(
                ax=self.axes, x=self.data.columns[self.now_x].name, y=self.data.columns[self.now_y].name, title=self.title)
        self.axes.grid(self.grid)
        self.draw()

    def clear_plot(self):
        self.axes.cla()

    def set_grid_(self, state):
        self.grid = state

    def set_line(self):
        pass  # to be implemented in future

    def set_plot_type(self, type_no):
        self.plot_type = type_no

    def _check_validate_y(self):
        self.pie_data = [y for y in self.now_y if y > 0]

    def set_x(self, x_idx):
        self.x_idx = x_idx

    def set_y(self, y_idx):
        self.y_idx = y_idx

    def create_toolbar(self, parent):
        return NavigationToolbar2QT(self, parent)

    def set_title(self, text=''):
        self.title = text

    def show_histogram(self):
        self.histogram = not self.histogram
