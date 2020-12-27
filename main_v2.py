import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Praca Inz Niedzielski')
        self._create_menu()
        self._create_status_bar()

    def _create_menu(self):
        self.menu = self.menuBar().addMenu('&Menu')
        self.menu.addAction('&Exit', self.close)

    def _create_status_bar(self):
        status = QStatusBar()
        status.showMessage('OK')
        self.setStatusBar(status)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
