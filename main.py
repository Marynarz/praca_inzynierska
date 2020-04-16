import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMenuBar, QMainWindow, QAction, qApp, QGridLayout
from PlotsCanvases import MplCanvas


class PlotCompareMain(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui_layout()

    def init_ui_layout(self):
        # menu:
        exit_action = QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(qApp.quit)

        menu = self.menuBar()

        file_opt = menu.addMenu('&File')
        file_opt.addAction(exit_action)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = PlotCompareMain()
    sys.exit(app.exec())
