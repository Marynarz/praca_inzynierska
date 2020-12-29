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

        # Canvas container
        self.canvases = {app_defs.MATPLOTLIB: MplCanvas(parent=self), app_defs.PYQTGRAPH: PyQtGraphCanvas(),
                         app_defs.PLOTLY: PlotLyCanvas()}

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

        x, y = 0, 0
        for layout in self.layouts:
            self.general_layout.addLayout(layout, x, y)
            if y == 1:
                y = 0
                x += 1
            else:
                y += 1

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
        self.layouts = []
        for key in self.canvases:
            layout = QVBoxLayout()
            layout.addWidget(QLabel(app_defs.CANVAS_NAME[key]))
            layout.addWidget(self.canvases[key])
            self.layouts.append(layout)

    def set_status(self, status):
        self.status.showMessage(status)

    def reset(self):
        pass

    def set_lang(self, lang):
        self.settings.setValue('lang', lang)
        self.set_status('Lang set to '+lang)

    def open_file_window(self):
        self.set_status('Open file')
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
        for key in self.canvases:
            self.canvases[key].upload_data(x=x, y=y)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
