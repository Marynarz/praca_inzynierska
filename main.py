import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMenuBar, QMainWindow, QAction, qApp, QGridLayout


class PlotCompareMain(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui_layout()

    def init_ui_layout(self):
        window = QWidget()
        # menu:
        exit_action = QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(qApp.quit)

        menu = self.menuBar()

        file_opt = menu.addMenu('&File')
        file_opt.addAction(exit_action)

        main_layout = QGridLayout()
        #main window
        self.setWindowTitle('Praca inzynierska - W. Niedzielski - 2020')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = PlotCompareMain()
    sys.exit(app.exec())
    