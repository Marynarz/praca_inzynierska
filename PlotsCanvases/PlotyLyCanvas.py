import plotly.express as px
import plotly.offline as po
import plotly.graph_objs as pgo
import pandas as pd
from PyQt5.QtWebEngineWidgets import QWebEngineView


class PlotLyCanvas(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.data = pd.DataFrame((0, ), index=(0, ))
        self.fig = px.line(self.data)

        self.raw_html_head = '<html><head><meta charset="utf-8" />' \
                             '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script></head>' \
                             '<body>'
        self.raw_html_tail = '</body></html>'

    def upload_data(self, data):
        self.data = pd.DataFrame(data[1], index=data[0])
        self.fig = px.line(self.data)
        self.show_plot()

    def show_plot(self):
        raw_html = self.raw_html_head + po.plot(self.fig,
                                                include_plotlyjs=False,
                                                output_type='div') + self.raw_html_tail
        self.setHtml(raw_html)
        self.show()

    def set_grid_(self, state):
        pass
