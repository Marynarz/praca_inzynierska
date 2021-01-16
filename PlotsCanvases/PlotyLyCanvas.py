import plotly.express as px
import plotly.offline as po
import pandas as pd
from PyQt5.QtWebEngineWidgets import QWebEngineView
from defs.app_defs import PlotTypes


class PlotLyCanvas(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.x_idx = 0
        self.y_idx = 0
        self.grid = False
        self.plot_type = PlotTypes.D2_CHART
        self.data = pd.DataFrame((0, ), index=(0, ))
        self.fig = px.line(self.data, y=self.data.index.name, x=self.data.index.name)

        self.raw_html_head = '<html><head><meta charset="utf-8" />' \
                             '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script></head>' \
                             '<body>'
        self.raw_html_tail = '</body></html>'

    def upload_data(self, data):
        self.data = data

    def prep_plot(self):
        if self.x_idx == -1:
            x = self.data.index.name
        else:
            x = self.data.columns[self.x_idx]

        if self.y_idx == -1:
            y = self.data.index.name
        else:
            y = self.data.columns[self.y_idx]

        try:
            if self.plot_type == PlotTypes.D2_CHART:
                self.fig = px.line(self.data, y=y, x=x)
            elif self.plot_type == PlotTypes.BAR_CHART:
                self.fig = px.bar(self.data, y=y, x=x)
            elif self.plot_type == PlotTypes.PIE_CHART:
                self.fig = px.pie(self.data, values=x)
            self.fig.update_yaxes(showgrid=self.grid)
            self.fig.update_xaxes(showgrid=self.grid)
        except ValueError as e:
            print(e)

    def show_plot(self):
        self.prep_plot()
        raw_html = self.raw_html_head + po.plot(self.fig,
                                                include_plotlyjs=False,
                                                output_type='div') + self.raw_html_tail
        self.setHtml(raw_html)
        self.show()

    def clear_plot(self):
        pass

    def set_grid_(self, state):
        self.grid = state

    def set_plot_type(self, type_no):
        self.plot_type = type_no

    def set_x(self, x_idx):
        self.x_idx = x_idx

    def set_y(self, y_idx):
        self.y_idx = y_idx
