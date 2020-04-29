from bokeh.plotting import figure
from bokeh.io import show, output_notebook


class BokehCanvas(object):
    def __init__(self):
        self.fig = figure()
        self.x = []
        self.y = []

    def load_data(self, x, y):
        self.x = x
        self.y = y
        self.fig.square_cross(self.x, self.y, size= 12, color='red')
        self.show_output()

    def show_output(self):
        output_notebook()
        show(self.fig)