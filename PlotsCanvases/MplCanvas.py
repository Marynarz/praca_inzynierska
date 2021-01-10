import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from defs.app_defs import PlotTypes
import pandas as pd

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, grid=False):
        self.now_x = []
        self.now_y = []
        self.plot_type = PlotTypes.D2_CHART
        self.dpi = 100
        figure = Figure(figsize=(10, 10), dpi=self.dpi)
        self.axes = figure.add_subplot(111)
        FigureCanvasQTAgg.__init__(self, figure)
        self.setParent(parent)
        self.grid = grid

        FigureCanvasQTAgg.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

    def upload_data(self, data):
        if type(data) != pd.DataFrame:
            print('error')
            print(data)
            data = pd.DataFrame(data)
        columns = data.columns.tolist()

        if len(columns) > 1:
            self.now_y = columns[0]
            self.now_x = columns[1]
        else:
            self.now_y = data.index.tolist()
            self.now_x = data[columns[0]].tolist()
        self.show()

    def show(self):
        self.axes.cla()
        if self.plot_type == PlotTypes.D2_CHART:
            self.axes.plot(self.now_x, self.now_y)
        elif self.plot_type == PlotTypes.BAR_CHART:
            self.axes.bar(self.now_x, self.now_y)
        elif self.plot_type == PlotTypes.PIE_CHART:
            self._check_validate_y()
            self.axes.pie(x=self.pie_data, labels=range(len(self.pie_data)))
        self.axes.grid(self.grid)
        self.draw()

    def set_grid_(self, state):
        self.grid = state
        self.show()

    def set_line(self):
        pass

    def set_plot_type(self, type_no):
        self.plot_type = type_no
        self.show()

    def _check_validate_y(self):
        self.pie_data = [y for y in self.now_y if y > 0]
