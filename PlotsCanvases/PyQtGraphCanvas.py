import pyqtgraph as pg
from defs.app_defs import PlotTypes
import pandas as pd


class PyQtGraphCanvas(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        self.plot_type = PlotTypes.D2_CHART
        self.x_pos = [0, ]
        self.y_pos = [0, ]
        self.x_idx = 0
        self.y_idx = 0

    def upload_data(self, data):
        columns = data.columns.tolist()

        if self.x_idx == -1:
            self.x_pos = data.index.tolist()
        else:
            self.x_pos = data[columns[self.x_idx]].tolist()

        if self.y_idx == -1:
            self.y_pos = data.index.tolist()
        else:
            self.y_pos = data[columns[self.y_idx]].tolist()

    def show_plot(self):
        self.clear_plot()
        if self.plot_type == PlotTypes.D2_CHART:
            self.plot(self.y_pos, self.x_pos)
        elif self.plot_type == PlotTypes.BAR_CHART:
            bar_chart = pg.BarGraphItem(x=self.y_pos, height=self.x_pos, width=0.6, brush='r')
            self.addItem(bar_chart)
        elif self.plot_type == PlotTypes.PIE_CHART:
            pass

    def set_grid_(self, state):
        self.showGrid(x=state, y=state)

    def set_line(self):
        pass

    def clear_plot(self):
        self.clear()

    def set_plot_type(self, type_no):
        self.plot_type = type_no
        self.show_plot()

    def set_x(self, x_idx):
        self.x_idx = x_idx

    def set_y(self, y_idx):
        self.y_idx = y_idx
