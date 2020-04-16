import matplotlib
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, x=10, y=10, dpi=100):
        figure = Figure(figsize=(x, y), dpi=dpi)
        self.axes = figure.add_subplot(111)
        super(MplCanvas, self).__init__(figure)

