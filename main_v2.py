import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QGridLayout, QWidget, QAction, QFileDialog,\
    QMessageBox, QVBoxLayout, QLabel
from PyQt5.QtCore import QSettings
from defs import str_defs, app_defs
from gui_tools import logger, FileValidator
from PlotsCanvases import MplCanvas, PyQtGraphCanvas, BokehCanvas, PlotLyCanvas


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # prepare canveses
        self.mat_plot_lib_canvas = MplCanvas(parent=self, x=10, y=10, dpi=100)
        self.bokeh_canvas = BokehCanvas()
        self.py_qt_graph = PyQtGraphCanvas()
        self.plotly_canvas = PlotLyCanvas()

        try:
            self.log = logger.Logger('main_gui')
        except Exception as e:
            print(e)
            sys.exit(0)
        self.settings = QSettings('wnie', 'praca_inzynierska')
        if self.settings.contains('lang'):
            self.language = self.settings.value('lang')
        else:
            # default english
            self.language = str_defs.LANG_ENG

        self.log.write_log(app_defs.INFO_MSG, 'Hello main gui\t--\tV2.00')
        self.log.write_log(app_defs.ERROR_MSG, 'lang: %s, type: %s' % (self.language, type(self.language)))
        self.setWindowTitle(str_defs.MAIN_WINDOW_TITLE[self.language])
        self.load_and_plot_data(app_defs.DEFAULT_PLOT)

        self._create_canvases_layouts()

        # Setting central widget
        self.general_layout = QGridLayout()
        self.general_layout.setRowMinimumHeight(1, 200)
        self._central_widget = QWidget(self)
        self.setCentralWidget(self._central_widget)
        self._central_widget.setLayout(self.general_layout)
        self.general_layout.addLayout(self.mat_plot_lib_layout, 0, 0)
        self.general_layout.addLayout(self.qt_graph_layout, 0, 1)
        self.general_layout.addLayout(self.bokeh_layout, 1, 0)
        self.general_layout.addLayout(self.plotly_layout, 1, 1)

        self._create_menu()
        self._create_status_bar()

    def _create_menu(self):
        self.menu = self.menuBar().addMenu(str_defs.MENU)
        # new
        self.menu.addAction(str_defs.NEW_APP[self.language], self.reset)

        file_open = QAction(str_defs.FILE_OPEN[self.language], self)
        file_open.setShortcut('Ctrl+O')
        self.menu.addAction(file_open)
        file_open.triggered.connect(self.open_file_window)

        # exit section
        self.menu.addSeparator()
        self.exit_action = QAction(str_defs.EXIT_APP[self.language], self)
        self.exit_action.setShortcut('Ctrl+Q')
        self.menu.addAction(self.exit_action)
        self.exit_action.triggered.connect(self.close)

        # settings menu
        self.sets = self.menuBar().addMenu(str_defs.SETTINGS_MENU[self.language])

        # internationalization
        self.langs = self.sets.addMenu(str_defs.LANG_CHANGE[self.language])

        # pl
        change_lang_action_pl = QAction(str_defs.POLISH[self.language], self)
        self.langs.addAction(change_lang_action_pl)
        change_lang_action_pl.triggered.connect(lambda x: self.set_lang(str_defs.LANG_PL))

        # eng
        change_lang_action_eng = QAction(str_defs.ENGLISH[self.language], self)
        self.langs.addAction(change_lang_action_eng)
        change_lang_action_eng.triggered.connect(lambda x: self.set_lang(str_defs.LANG_ENG))

    def _create_status_bar(self):
        self.status = QStatusBar()
        self.status.showMessage('OK')
        self.setStatusBar(self.status)

    def _create_canvases_layouts(self):
        # setting layouts
        # matplotlib layout
        self.mat_plot_lib_layout = QVBoxLayout()
        mat_plot_lib_label = QLabel(str_defs.MAT_PLOT_LIB)
        self.mat_plot_lib_layout.addWidget(mat_plot_lib_label)
        self.mat_plot_lib_layout.addWidget(self.mat_plot_lib_canvas)

        # qt graph layout
        self.qt_graph_layout = QVBoxLayout()
        qt_graph_label = QLabel(str_defs.QTGRAPH)
        self.qt_graph_layout.addWidget(qt_graph_label)
        self.qt_graph_layout.addWidget(self.py_qt_graph)

        # bokeh layout
        self.bokeh_layout = QVBoxLayout()
        bokeh_label = QLabel(str_defs.BOKEH)
        self.bokeh_layout.addWidget(bokeh_label)
        self.bokeh_layout.addWidget(self.bokeh_canvas)

        # plotly layout
        self.plotly_layout = QVBoxLayout()
        plotly_label = QLabel(str_defs.PLOTLY)
        self.plotly_layout.addWidget(plotly_label)
        self.plotly_layout.addWidget(self.plotly_canvas)

    def set_status(self, status):
        self.status.showMessage(status)

    def reset(self):
        pass

    def set_lang(self, lang):
        self.settings.setValue('lang', lang)
        self.set_status('Lang set to '+lang)

    def open_file_window(self):
        ret = app_defs.NO_ACTION
        file_to_open, _ = QFileDialog.getOpenFileName(self, 'Open file',
                                                      filter='TextFile (*.txt);;CSV (*.csv)')
        self.log.write_log(app_defs.INFO_MSG, 'Selected file: ' + str(file_to_open))
        if file_to_open:
            file_points = FileValidator.FileValidator('Main')
            ret = file_points.file_to_validate(file_to_open)

        if ret != app_defs.NOERROR:
            if ret == app_defs.UNKNOWN_FILE_TYPE:
                self.log.write_log(app_defs.WARNING_MSG, 'Unknown file type! File: %s' % file_to_open)
                _ = QMessageBox.information(self, 'Unknown file type',
                                            'File: %s cannot be open. File type unknown.' % file_to_open,
                                            QMessageBox.Ok, QMessageBox.Ok)
            elif ret == app_defs.UNABLE_TO_OPEN_FILE:
                self.log.write_log(app_defs.ERROR_MSG, 'Unable to open file! File: %s' % file_to_open)
                _ = QMessageBox.warning(self, 'Unknown file type',
                                        'File: %s unable to open. Please see log file!' % file_to_open,
                                        QMessageBox.Ok, QMessageBox.Ok)
        elif ret == app_defs.NOERROR:
            self.log.write_log(app_defs.INFO_MSG, 'File validated successfully, proceed to load and plot data.')
            self.load_and_plot_data(file_points.get_values())

    def load_and_plot_data(self, data):
        self.log.write_log(app_defs.INFO_MSG, 'Load and plot data')
        x = [line[0] for line in data]
        y = [line[1] for line in data]
        self.log.write_log(app_defs.INFO_MSG, 'Data to plot: x:%s | y:%s' % (x, y))
        self.mat_plot_lib_canvas.upload_data(x=x, y=y)
        self.py_qt_graph.upload_data(x=x, y=y)
        self.plotly_canvas.upload_data(x=x, y=y)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
