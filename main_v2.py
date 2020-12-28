import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar
from defs import str_defs, app_defs
from gui_tools import logger


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        try:
            self.log = logger.Logger('main_gui')
        except Exception as e:
            print(e)
            sys.exit(0)
        self.log.write_log(app_defs.INFO_MSG, 'Hello main gui\t--\tV2.00')
        self.setWindowTitle(str_defs.MAIN_WINDOW_TITLE['pl'])
        self._create_menu()
        self._create_status_bar()

    def _create_menu(self):
        self.menu = self.menuBar().addMenu(str_defs.MENU)
        # new

        self.menu.addAction(str_defs.NEW_APP['pl'], self.reset)

        # exit section
        self.menu.addSeparator()
        self.menu.addAction(str_defs.EXIT_APP['pl'], self.close)

    def _create_status_bar(self):
        status = QStatusBar()
        status.showMessage('OK')
        self.setStatusBar(status)

    def reset(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
