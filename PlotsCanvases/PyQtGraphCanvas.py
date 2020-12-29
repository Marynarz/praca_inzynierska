import pyqtgraph as pg
from abc import register
from BaseCanvas import BaseCanvas


@BaseCanvas.register
class PyQtGraphCanvas(pg.PlotWidget):
    def __init__(self):
        super().__init__()

    def update_canvas(self, x, y):
        self.clear_plot()
        self.plot(x, y)

    def clear_plot(self):
        self.clear()
