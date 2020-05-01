import sys

from PyQt5.QtWidgets import QApplication, QWidget, QMenuBar, QAction, qApp, QGridLayout, \
    QFileDialog, QMessageBox
import app_defs
from PlotsCanvases import BokehCanvas
from PlotsCanvases import MplCanvas
from gui_tools import FileValidator, logger


class PlotCompareMain(QWidget):
    def __init__(self):
        super().__init__()
        try:
            self.log = logger.Logger('main_gui')
        except Exception as e:
            print(e)
            sys.exit(0)

        self.mat_plot_lib_canvas = MplCanvas.MplCanvas(parent=self, x=10, y=10, dpi=100)
        self.bokeh_canvas = BokehCanvas.BokehCanvas()
        self.setStyleSheet(open('gui_tools/main_style.css').read())
        self.init_ui_layout()

    def init_ui_layout(self):
        self.log.write_log(app_defs.INFO_MSG, 'Begin main ui routine')
        # menu:
        exit_action = QAction(' &Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(qApp.quit)

        open_file = QAction('&Open', self)
        open_file.setShortcut('Ctrl+O')
        open_file.triggered.connect(self.open_file_window)

        menu = QMenuBar()

        file_opt = menu.addMenu('&File')
        file_opt.addAction(open_file)
        file_opt.addAction(exit_action)

        # plots
        self.load_and_plot_data(app_defs.DEFAULT_PLOT)



        main_layout = QGridLayout()
        main_layout.addWidget(menu)
        main_layout.addWidget(self.mat_plot_lib_canvas, 1, 0)

        # main window
        self.setLayout(main_layout)
        self.setWindowTitle('Praca inzynierska - W. Niedzielski - 2020')
        self.show()

    def open_file_window(self):
        ret = app_defs.NO_ACTION
        file_to_open, _ = QFileDialog.getOpenFileName(self, 'Open file',
                                                      filter='TextFile (*.txt);;XML (*.xml);;JSON (*.json)')
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
            self.log.write_log(app_defs.INFO_MSG, 'File validated succefully, proceed to load and plot data.')
            self.load_and_plot_data(file_points.get_values())

    def load_and_plot_data(self, data):
        self.log.write_log(app_defs.INFO_MSG, 'Load and plot data')
        x = []
        y = []
        for line in data:
            x.append(line[0])
            y.append(line[1])
        self.log.write_log(app_defs.INFO_MSG, 'Data to plot: x:%s | y:%s' % (x, y))
        self.mat_plot_lib_canvas.update_canvas(x=x, y=y)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = PlotCompareMain()
    sys.exit(app.exec())
