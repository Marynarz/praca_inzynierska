import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMenuBar, QMainWindow, QAction, qApp, QGridLayout,\
    QFileDialog, QMessageBox, QMenu
from PlotsCanvases import MplCanvas
from gui_tools import FileValidator, logger
import app_defs


class PlotCompareMain(QWidget):
    def __init__(self):
        super().__init__()
        try:
            self.log = logger.Logger('main_gui')
        except Exception as e:
            print(e)
            sys.exit(0)

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
        mat_plot_lib_canvas = MplCanvas.MplCanvas(parent=self, x=10, y=10, dpi=100)
        mat_plot_lib_canvas.axes.plot([0,1,2,3,4], [10,1,20,3,40])

        main_layout = QGridLayout()
        main_layout.addWidget(mat_plot_lib_canvas)
        main_layout.addWidget(menu)

        # main window
        self.setLayout(main_layout)
        self.setWindowTitle('Praca inzynierska - W. Niedzielski - 2020')
        self.show()

    def open_file_window(self):
        ret = app_defs.NO_ACTION
        file_to_open, _ = QFileDialog.getOpenFileName(self, 'Open file')
        self.log.write_log(app_defs.INFO_MSG, 'Selected file: ' + str(file_to_open))
        if file_to_open:
            txt_file_points = FileValidator.FileValidator('Main')
            ret = txt_file_points.file_to_validate(file_to_open)

        if ret != app_defs.NOERROR:
            if ret == app_defs.UNKNOWN_FILE_TYPE:
                self.log.write_log(app_defs.WARNING_MSG, 'Unknown file type! File: %s' % file_to_open)
                _ = QMessageBox.information(self, 'Unknown file type',
                                            'File: %s cannot be open. File type unknown.' % file_to_open,
                                            QMessageBox.Ok, QMessageBox.Ok)
            elif ret == app_defs.UNABLE_TO_OPEN_FILE:
                _ = QMessageBox.warning(self, 'Unknown file type',
                                        'File: %s unable to open. Please see log file!' % file_to_open,
                                        QMessageBox.Ok, QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = PlotCompareMain()
    sys.exit(app.exec())
