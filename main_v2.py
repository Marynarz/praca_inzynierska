import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QGridLayout, QWidget, QAction
from PyQt5.QtCore import QSettings
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
        self.settings = QSettings('wnie', 'praca_inzynierska')
        if self.settings.contains('lang'):
            self.language = self.settings.value('lang')
        else:
            # default english
            self.language = str_defs.LANG_ENG

        self.log.write_log(app_defs.INFO_MSG, 'Hello main gui\t--\tV2.00')
        self.log.write_log(app_defs.ERROR_MSG, 'lang: %s, type: %s' % (self.language, type(self.language)))
        self.setWindowTitle(str_defs.MAIN_WINDOW_TITLE[self.language])

        # Setting central widget
        self.general_layout = QGridLayout()
        self._central_widget = QWidget(self)
        self.setCentralWidget(self._central_widget)
        self._central_widget.setLayout(self.general_layout)

        self._create_menu()
        self._create_status_bar()

    def _create_menu(self):
        self.menu = self.menuBar().addMenu(str_defs.MENU)
        # new

        self.menu.addAction(str_defs.NEW_APP[self.language], self.reset)

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
        status = QStatusBar()
        status.showMessage('OK')
        self.setStatusBar(status)

    def reset(self):
        pass

    def set_lang(self, lang):
        self.settings.setValue('lang', lang)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
