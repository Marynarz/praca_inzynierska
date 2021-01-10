import pyqtgraph as pg
from defs.app_defs import PlotTypes
import pandas as pd


class PyQtGraphCanvas(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        self.plot_type = PlotTypes.D2_CHART
        self.x_pos = 0
        self.y_pos = 0

    def upload_data(self, data):
        if type(data) != pd.DataFrame:
            print('error')
            print(data)
            data = pd.DataFrame(data)
        columns = data.columns.tolist()

        if len(columns) > 1:
            self.y_pos = data[columns[0]].tolist()
            self.x_pos = data[columns[1]].tolist()
        else:
            self.y_pos = data.index.tolist()
            self.x_pos = data[columns[0]].tolist()

        self.show_plot()

    def show_plot(self):
        self.clear_plot()
        if self.plot_type == PlotTypes.D2_CHART:
            self.plot(self.x_pos, self.y_pos)
        elif self.plot_type == PlotTypes.BAR_CHART:
            bar_chart = pg.BarGraphItem(x=self.x_pos, height=self.y_pos, width=0.6, brush='r')
            self.addItem(bar_chart)
        elif self.plot_type == PlotTypes.PIE_CHART:
            pass

    def set_grid_(self, state):
        self.showGrid(x=state, y=state)
        self.show_plot()

    def set_line(self):
        pass

    def clear_plot(self):
        self.clear()

    def set_plot_type(self, type_no):
        self.plot_type = type_no
        self.show_plot()
