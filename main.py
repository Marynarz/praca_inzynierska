import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMenuBar, QMainWindow, QAction, qApp, QGridLayout,\
    QFileDialog
from PlotsCanvases import MplCanvas
from FileValidator import FileValidatorTxt


class PlotCompareMain(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui_layout()

    def init_ui_layout(self):
        # menu:
        exit_action = QAction(' &Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(qApp.quit)

        open_file = QAction('&Open', self)
        open_file.setShortcut('Ctrl+O')
        open_file.triggered.connect(self.open_file_window)

        menu = self.menuBar()

        file_opt = menu.addMenu('&File')
        file_opt.addAction(exit_action)
        file_opt.addAction(open_file)


        #plots
        mat_plot_lib_canvas = MplCanvas.MplCanvas(parent=self, x=10, y=10, dpi=100)
        mat_plot_lib_canvas.axes.plot([0,1,2,3,4], [10,1,20,3,40])

        main_layout = QGridLayout()
        main_layout.addWidget(mat_plot_lib_canvas)
        gen_widget = QWidget()
        #main window
        gen_widget.setLayout(main_layout)
        self.setCentralWidget(gen_widget)
        self.setWindowTitle('Praca inzynierska - W. Niedzielski - 2020')
        self.show()

    def open_file_window(self):
        file_to_open, _ = QFileDialog.getOpenFileName(self, 'Open file')
        if '.txt' in file_to_open:
            txt_file_points = FileValidatorTxt.FileValidatorTxt()
            txt_file_points.validate_txt_file(file_to_open)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = PlotCompareMain()
    sys.exit(app.exec())
