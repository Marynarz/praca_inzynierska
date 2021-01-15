from bokeh.plotting import figure
from bokeh.io import output_file, save
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


class BokehCanvas(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.fig = figure()
        self.x = []
        self.y = []
        output_file('bokeh_plot.html')
        save(self.fig)
        self.load(QUrl('bokeh_plot.html'))

    def load_data(self, x, y):
        self.x = x
        self.y = y
        self.fig.square_cross(self.x, self.y, size=12, color='red')
        self.show_output()

    def show_output(self):
        # output_notebook()
        output_file('bokeh_plot.html')
