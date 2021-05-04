from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QMessageBox
import validators
import pandas as pd
from defs import str_defs


class JsonUrlOpen(QWidget):
    def __init__(self, data_viewer=None, language=str_defs.LANG_ENG):
        super().__init__()
        if not data_viewer:
            raise RuntimeError
        self.dv = data_viewer
        self.language = language
        self.setMinimumWidth(350)
        self.setWindowTitle(str_defs.URL_TITLE[self.language])
        layout = QFormLayout()
        self.url_set = QLineEdit(str_defs.URL_LINE_EDIT[self.language])
        btn_set_url = QPushButton(str_defs.URL_BTN_LABEL[self.language])
        btn_set_url.clicked.connect(self.download_json)
        layout.addRow(str_defs.URL_LINE_LABEL, self.url_set)
        layout.addRow(btn_set_url)
        self.setLayout(layout)

    def download_json(self):
        text = self.url_set.text()
        valid, url = self.validate_url(text)
        if not valid:
            self._err_msg_box(str_defs.WRONG_URL_TITLE[self.language],
                              str_defs.WRONG_URL_MAIN[self.language],
                              str_defs.WRONG_URL_ADDITIONAL[self.language].format(url))
        else:
            try:
                data = pd.read_json(url)
                self.dv.set_data(data)
            except Exception:
                self._err_msg_box(str_defs.URL_NOT_WORK_TITLE[self.language],
                                  str_defs.URL_NOT_WORK_MAIN[self.language],
                                  str_defs.URL_NOT_WORK_ADDITIONAL[self.language])
            else:
                self.close()

    # Url validation by validators.url, if not true first check if maybe only we need to add 'http://'
    @staticmethod
    def validate_url(url):
        if not validators.url(url):
            url = 'https://' + url
            return validators.url(url), url
        return True, url

    # Error massage box for class JsonUrlOpen
    # A lot of things can go wrong, in every bad scenario we should inform user
    @staticmethod
    def _err_msg_box(title, text, additional_txt= ''):
        not_valid_msg = QMessageBox()
        not_valid_msg.setIcon(QMessageBox.Warning)
        not_valid_msg.setWindowTitle(title)
        not_valid_msg.setText(text)
        not_valid_msg.setInformativeText(additional_txt)
        not_valid_msg.setStandardButtons(QMessageBox.Ok)
        _ = not_valid_msg.exec()

