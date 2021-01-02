import pyqtgraph as pg
from defs.app_defs import PlotTypes


class PyQtGraphCanvas(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        self.plot_type = PlotTypes.D2_CHART
        self.x_pos = 0
        self.y_pos = 0

    def upload_data(self, data):
        self.x_pos = (line[0] for line in data)
        self.x_pos = list(self.x_pos)
        self.y_pos = (line[1] for line in data)
        self.y_pos = list(self.y_pos)
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
