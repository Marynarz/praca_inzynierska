import plotly.express as px
import plotly.offline as po
import plotly.graph_objs as pgo
import pandas as pd
from PyQt5.QtWebEngineWidgets import QWebEngineView
from defs.app_defs import PlotTypes


class PlotLyCanvas(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.plot_type = PlotTypes.D2_CHART
        self.data = pd.DataFrame((0, ), index=(0, ))
        self.fig = px.line(self.data)

        self.raw_html_head = '<html><head><meta charset="utf-8" />' \
                             '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script></head>' \
                             '<body>'
        self.raw_html_tail = '</body></html>'

    def upload_data(self, data):
        self.data = pd.DataFrame(data)
        if self.plot_type == PlotTypes.D2_CHART:
            self.fig = px.line(self.data, x=0, y=1)
        elif self.plot_type == PlotTypes.BAR_CHART:
            self.fig = px.bar(self.data, x=0, y=1)
        elif self.plot_type == PlotTypes.PIE_CHART:
            self.fig = px.pie(self.data, values=0)
        self.show_plot()

    def show_plot(self):
        raw_html = self.raw_html_head + po.plot(self.fig,
                                                include_plotlyjs=False,
                                                output_type='div') + self.raw_html_tail
        self.setHtml(raw_html)
        self.show()

    def set_grid_(self, state):
        pass

    def set_plot_type(self, type_no):
        self.plot_type = type_no
        self.upload_data(self.data)
