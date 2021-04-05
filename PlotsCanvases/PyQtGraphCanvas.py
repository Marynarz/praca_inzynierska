import pyqtgraph as pg
from defs.app_defs import PlotTypes
import pandas as pd


class PyQtGraphCanvas(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        self.plot_type = PlotTypes.D2_CHART
        self.title = ''
        self.x_pos = [0, ]
        self.y_pos = [0, ]
        self.x_idx = 0
        self.y_idx = 0
        self.data = pd.DataFrame((0, 0))
        self.clear_plot()
        self.prep_data()
        self.show_plot()

    def upload_data(self, data):
        self.data = data

    def prep_data(self):
        columns = self.data.columns.tolist()
        if self.x_idx == -1:
            self.x_pos = self.data.index.tolist()
        else:
            self.x_pos = self.data[columns[self.x_idx]].tolist()

        if self.y_idx == -1:
            self.y_pos = self.data.index.tolist()
        else:
            self.y_pos = self.data[columns[self.y_idx]].tolist()

    def show_plot(self):
        self.prep_data()
        if self.plot_type == PlotTypes.D2_CHART:
            self.plot(self.x_pos, self.y_pos, title=self.title)
        elif self.plot_type == PlotTypes.BAR_CHART:
            bar_chart = pg.BarGraphItem(x=self.x_pos, height=self.y_pos, width=0.6, brush='r', title=self.title)
            self.addItem(bar_chart)
        elif self.plot_type == PlotTypes.PIE_CHART:
            print('Pie chart not implemented yet')

    def set_grid_(self, state):
        self.showGrid(x=state, y=state)

    def set_line(self):
        pass  # to be implemented in future

    def clear_plot(self):
        self.clear()

    def set_plot_type(self, type_no):
        self.plot_type = type_no

    def set_x(self, x_idx):
        self.x_idx = x_idx

    def set_y(self, y_idx):
        self.y_idx = y_idx

    def set_title(self, text):
        self.title = text
