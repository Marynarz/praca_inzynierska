from bokeh.plotting import figure
from bokeh.io import output_file, save
from bokeh.models import ColumnDataSource
from PyQt5.QtWebEngineWidgets import QWebEngineView
from defs.app_defs import PlotTypes
import pandas as pd


class BokehCanvas(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.fig = figure(plot_width=400, plot_height=400)
        self.x_idx = 0
        self.y_idx = 0
        self.plot_type = PlotTypes.D2_CHART
        self.data = ColumnDataSource(pd.DataFrame((0, ), columns=('0', )))

    def show_output(self):
        output_file('bokeh_plot.html', mode='inline')
        html_str = ''
        with open('bokeh_plot.html') as f:
            for line in f.readlines():
                html_str += line
        self.setHtml(html_str)

    def upload_data(self, data):
        data = data.rename(columns={col: str(col) for col in data.columns})
        self.data = ColumnDataSource(data)
        print(self.data)

    def prep_plot(self):
        print(self.data)

        try:
            self.fig.line(x='0', y='0', source=self.data)
            save(self.fig)
            self.show_output()
        except ValueError as e:
            print(e)

    def show_plot(self):
        self.prep_plot()
        output_file('bokeh_plot.html', mode='inline')
        html_str = ''
        with open('bokeh_plot.html') as f:
            for line in f.readlines():
                html_str += line
        self.setHtml(html_str)

    def clear_plot(self):
        pass

    def set_grid_(self, state):
        pass

    def set_plot_type(self, type_no):
        self.plot_type = type_no

    def set_x(self, x_idx):
        self.x_idx = x_idx

    def set_y(self, y_idx):
        self.y_idx = y_idx
