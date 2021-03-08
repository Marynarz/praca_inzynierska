import sys
from gui_view import tabs_view
from defs import app_defs
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    return_code = app_defs.REBOOT_APP

    while return_code == app_defs.REBOOT_APP:
        app = QApplication(sys.argv)
        main = tabs_view.TabsView()
        main.show()
        return_code = app.exec()

    sys.exit(return_code)