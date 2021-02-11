from PyQt5.QtWidgets import QMainWindow, QStatusBar, QAction, QDockWidget, QWidget, QFormLayout, QCheckBox, QToolButton, \
    QComboBox, QMessageBox, QFileDialog, QToolBar, QVBoxLayout, QGroupBox, QGridLayout, QTabWidget
from PyQt5.QtCore import QSettings, Qt

from PlotsCanvases import MplCanvas, PyQtGraphCanvas, PlotLyCanvas, BokehCanvas
from defs import app_defs, str_defs
from gui_tools import FileValidator, data_viewer, canvas_controller, logger
import pandas as pd


class TabsView(QMainWindow):
    FNAME_LOG_STR = 'TabsView.{0!s}'

    def __init__(self, parent=None):
        super().__init__(parent)
        self.log = logger.Logger('main_gui')
        self.re_write_log = False

        self._setting_up()

        self.log.write_log(app_defs.INFO_MSG, 'Hello main gui\t--\tV2.00')
        self.log.write_log(app_defs.ERROR_MSG, 'lang: %s, type: %s' % (self.language, type(self.language)))
        self.setWindowTitle(str_defs.MAIN_WINDOW_TITLE[self.language])

        # Canvas container
        self._prep_canvases()

        # Setting central widget
        self._central_widget = QTabWidget()
        self.setCentralWidget(self._central_widget)

        for canvas in self.canvases:
            self._central_widget.addTab(self.canvases[canvas], canvas)

        self._create_actions()
        self._create_menu()
        self._create_status_bar()
        self.data_viewer = data_viewer.DataViewer(parent=self)
        self.data_viewer.set_data(pd.DataFrame(app_defs.DEFAULT_PLOT))
        self._create_tool_bar()
        self._create_dock()
        self.load_data()
        self.canvas_controller.set_values('y', 1)

    def _prep_canvases(self):
        self.log.write_log(app_defs.FUNIN_MSG, self.FNAME_LOG_STR.format('_prep_canvases'))
        self.canvases = {app_defs.MATPLOTLIB: MplCanvas(parent=self, grid=False),
                         app_defs.PYQTGRAPH: PyQtGraphCanvas(),
                         app_defs.PLOTLY: PlotLyCanvas(),
                         app_defs.BOKEH: BokehCanvas()}
        self.canvas_controller = canvas_controller.CanvasController(self.canvases)
        self.grid = False
        self.log.write_log(app_defs.FUNOUT_MSG, self.FNAME_LOG_STR.format('_prep_canvases'))

    def _setting_up(self):
        self.settings = QSettings('wnie', 'praca_inzynierska')
        if self.settings.contains('lang'):
            self.language = self.settings.value('lang')
        else:
            # default english
            self.language = str_defs.LANG_ENG

    def _create_menu(self):
        self.log.write_log(app_defs.INFO_MSG, 'Creating menus')
        self.menu = self.menuBar().addMenu(str_defs.MENU)

        # new
        self.menu.addAction(self.reset_action)

        # open file
        self.menu.addAction(self.file_open)

        # exit section
        self.menu.addSeparator()

        self.menu.addAction(self.exit_action)
        self.exit_action.triggered.connect(self.close)

        # settings menu
        self.sets = self.menuBar().addMenu(str_defs.SETTINGS_MENU[self.language])

        # internationalization
        self.langs = self.sets.addMenu(str_defs.LANG_CHANGE[self.language])
        self.langs.addAction(self.lang_pl_action)
        self.langs.addAction(self.lang_eng_action)

    def _create_status_bar(self):
        self.log.write_log(app_defs.INFO_MSG, 'Creating status bar')
        self.status = QStatusBar()
        self.set_status('OK')
        self.setStatusBar(self.status)

    def _create_actions(self):
        self.file_open = QAction(str_defs.FILE_OPEN[self.language], self)
        self.file_open.setShortcut('Ctrl+O')
        self.file_open.triggered.connect(self.open_file_window)

        self.reset_action = QAction(str_defs.NEW_APP[self.language], self)
        self.reset_action.triggered.connect(self.reset)

        self.exit_action = QAction(str_defs.EXIT_APP[self.language], self)
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.triggered.connect(self.close)

        self.lang_pl_action = QAction(str_defs.POLISH[self.language], self)
        self.lang_pl_action.triggered.connect(lambda: self.set_lang(str_defs.LANG_PL))

        self.lang_eng_action = QAction(str_defs.ENGLISH[self.language], self)
        self.lang_eng_action.triggered.connect(lambda: self.set_lang(str_defs.LANG_ENG))

        self.show_data_action = QAction(str_defs.SHOW_DATA[self.language], self)
        self.show_data_action.triggered.connect(self.show_data_app)

    def _create_tool_bar(self):
        tools_toolbar = QToolBar('Tools')
        tools_toolbar.addAction(self.file_open)
        tools_toolbar.addAction(self.show_data_action)
        tools_toolbar.setFloatable(False)
        tools_toolbar.setMovable(False)

        self.addToolBar(tools_toolbar)

    def _create_dock(self):
        self.log.write_log(app_defs.INFO_MSG, 'Creating Dock')
        self.main_tools_dock = QDockWidget(str_defs.DOCK_TITLE[self.language], self)
        self.docket_widget = QWidget()
        dock_layout = QFormLayout()

        self.set_grid_box = QCheckBox(str_defs.GRID[self.language], self)
        self.set_grid_box.setChecked(self.grid)
        self.set_grid_box.stateChanged.connect(self.set_grid)

        show_data_btn = QToolButton()
        show_data_btn.setDefaultAction(self.show_data_action)

        self.plot_type_box = QComboBox()
        self.plot_type_box.addItems(str_defs.PLOT_TYPES[self.language])
        self.plot_type_box.currentIndexChanged.connect(self.data_viewer.set_plot_type)

        self.docket_widget.setLayout(dock_layout)
        dock_layout.addWidget(self.set_grid_box)
        dock_layout.addWidget(show_data_btn)
        dock_layout.addWidget(self.plot_type_box)

        self.main_tools_dock.setWidget(self.docket_widget)

        self.addDockWidget(Qt.RightDockWidgetArea, self.main_tools_dock)

    def show_data_app(self):
        self.data_viewer.show()

    def set_status(self, status):
        self.status.showMessage(status, app_defs.STATUS_TIMEOUT)

    def reset(self):
        # self.exit_app(app_defs.REBOOT_APP)
        pass

    def exit_app(self, rc=0):
        # QApplication.exit(return_code)
        pass

    def set_lang(self, lang):
        self.log.write_log(app_defs.WARNING_MSG, 'Language set to: {0!s}. Manual action needed!'.format(lang))
        self.settings.setValue('lang', lang)
        self.set_status('Lang set to ' + lang)

    def open_file_window(self):
        self.set_status('Open file')
        ret = app_defs.NO_ACTION
        file_to_open, _ = QFileDialog.getOpenFileName(self, 'Open file',
                                                      filter='TextFile (*.txt);;CSV (*.csv);;JSON (*.json)')
        self.log.write_log(app_defs.INFO_MSG, 'Selected file: ' + str(file_to_open))
        if file_to_open:
            file_points = FileValidator.FileValidator('Main', append=self.re_write_log)
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
            self.data_viewer.set_data(file_points.get_values())
            self.load_data()

        if not self.re_write_log:
            self.re_write_log = True

    def load_data(self):
        self.canvas_controller.upload_data(data=self.data_viewer.get_data())

    def set_grid(self):
        grid = self.canvas_controller.grid
        self.log.write_log(app_defs.INFO_MSG, 'grid set to {0}'.format(not grid))

        self.canvas_controller.set_grid()

        self.set_grid_box.blockSignals(True)
        self.set_grid_box.setChecked(not grid)
        self.set_grid_box.blockSignals(False)

        self.set_status(str_defs.GRID_SET[self.language].format(not grid))
        self.data_viewer.upd_grid()