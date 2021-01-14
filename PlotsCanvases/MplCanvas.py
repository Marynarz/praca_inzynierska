import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from defs.app_defs import PlotTypes


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, grid=False):
        self.now_x = []
        self.now_y = []
        self.x_idx = 0
        self.y_idx = 0
        self.plot_type = PlotTypes.D2_CHART
        self.dpi = 100
        figure = Figure(figsize=(10, 10), dpi=self.dpi)
        self.axes = figure.add_subplot(111)
        FigureCanvasQTAgg.__init__(self, figure)
        self.setParent(parent)
        self.grid = grid

        FigureCanvasQTAgg.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvasQTAgg.updateGeometry(self)

    def upload_data(self, data=None):
        columns = data.columns.tolist()

        if self.x_idx == -1:
            self.now_x = data.index.tolist()
        else:
            self.now_x = data[columns[self.x_idx]].tolist()

        if self.y_idx == -1:
            self.now_y = data.index.tolist()
        else:
            self.now_y = data[columns[self.y_idx]].tolist()

        self.show()

    def show(self):
        self.axes.cla()
        if self.plot_type == PlotTypes.D2_CHART:
            self.axes.plot(self.now_y, self.now_x)
        elif self.plot_type == PlotTypes.BAR_CHART:
            self.axes.bar(self.now_y, self.now_x)
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

    def set_x(self, x_idx):
        self.x_idx = x_idx

    def set_y(self, y_idx):
        self.y_idx= y_idx
