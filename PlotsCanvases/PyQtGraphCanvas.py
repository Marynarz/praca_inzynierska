import pyqtgraph as pg


class PyQtGraphCanvas(pg.PlotWidget):
    def __init__(self):
        super().__init__()
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
        self.plot(self.x_pos, self.y_pos)

    def set_grid_(self, state):
        self.showGrid(x=state, y=state)
        self.show_plot()

    def set_line(self):
        pass

    def clear_plot(self):
        self.clear()
