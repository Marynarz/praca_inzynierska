from bokeh.plotting import figure
from bokeh.io import output_file, save
from bokeh.models import ColumnDataSource
from PyQt5.QtWebEngineWidgets import QWebEngineView
from defs.app_defs import PlotTypes
import pandas as pd


class BokehCanvas(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.fig = figure(plot_width=380, plot_height=320)
        self.title = ''
        self.x_idx = 0
        self.y_idx = 0
        self.fig.xgrid.visible = False
        self.fig.ygrid.visible = False
        self.plot_type = PlotTypes.D2_CHART
        self.data = ColumnDataSource(pd.DataFrame((0, ), columns=('0', )))
        output_file('bokeh_plot.html', mode='inline')

    def upload_data(self, data):
        data = data.rename(columns={col: str(col) for col in data.columns})
        self.data = ColumnDataSource(data)

    def prep_plot(self):
        if self.x_idx == -1:
            x = self.data.column_names[0]
        else:
            x = self.data.column_names[self.x_idx + 1]

        if self.y_idx == -1:
            y = self.data.column_names[0]
        else:
            y = self.data.column_names[self.y_idx + 1]

        try:
            self.fig.title = self.title
            if self.plot_type == PlotTypes.D2_CHART:
                self.fig.line(x=x, y=y, source=self.data)
            elif self.plot_type == PlotTypes.BAR_CHART:
                self.fig.vbar(source=self.data, top=y, x=x)
            elif self.plot_type == PlotTypes.PIE_CHART:
                print('Pie chart not implemented yet')

            save(self.fig)
        except ValueError as e:
            print(e)

    def show_plot(self):
        self.prep_plot()
        html_str = ''
        with open('bokeh_plot.html') as f:
            for line in f.readlines():
                html_str += line
        self.setHtml(html_str)

    def clear_plot(self):
        self.fig.renderers = []

    def set_grid_(self, state):
        self.fig.xgrid.visible = state
        self.fig.ygrid.visible = state

    def set_plot_type(self, type_no):
        self.plot_type = type_no

    def set_x(self, x_idx):
        self.x_idx = x_idx

    def set_y(self, y_idx):
        self.y_idx = y_idx

    def set_title(self, text):
        self.title = text

    def show_histogram(self):
        print('To be implemented')
