import pyqtgraph as pg


class PyQtGraphCanvas(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        self.x_pos = 0
        self.y_pos = 0

    def upload_data(self, x, y):
        self.x_pos = x
        self.y_pos = y
        self.show_plot()

    def show_plot(self):
        self.clear_plot()
        self.plot(self.x_pos, self.y_pos)

    def set_grid(self):
        pass

    def set_line(self):
        pass

    def clear_plot(self):
        self.clear()
