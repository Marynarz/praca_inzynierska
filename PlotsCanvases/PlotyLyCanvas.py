import plotly.express as px
import plotly.offline as po
import pandas as pd
from PyQt5.QtWebEngineWidgets import QWebEngineView


class PlotLyCanvas(QWebEngineView):
    def __init__(self):
        super().__init__()
        test_pd = pd.DataFrame({'First': (1, 2, 3, 10, -1)})
        self.fig = px.line(test_pd)

        raw_html = '<html><head><meta charset="utf-8" />'
        raw_html += '<script src="https://cdn.plot.ly/plotly-latest.min.js"></script></head>'
        raw_html += '<body>'
        raw_html += po.plot(self.fig, include_plotlyjs=False, output_type='div')
        raw_html += '</body></html>'
        # setHtml has a 2MB size limit, need to switch to setUrl on tmp file
        # for large figures.
        self.setHtml(raw_html)
        self.show()
