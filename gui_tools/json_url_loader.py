from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QMessageBox
import validators
import pandas as pd


class JsonUrlOpen(QWidget):
    def __init__(self, data_viewer=None):
        super().__init__()
        self.dv = data_viewer
        layout = QFormLayout()
        self.url_set = QLineEdit('Type url here')
        btn_set_url = QPushButton('Set url')
        btn_set_url.clicked.connect(self.download_json)
        layout.addRow('Url:', self.url_set)
        layout.addRow(btn_set_url)
        self.setLayout(layout)

    def download_json(self):
        text = self.url_set.text()
        valid, url = self.validate_url(text)
        if not valid:
            self._err_msg_box('Wrong url', 'Url validation not passed', url + ' is not valid url')
        else:
            try:
                data = pd.read_json(url)
                self.dv.set_data(data)
            except Exception:
                self._err_msg_box('Url not working', 'Your url not working properly', 'Double check it')
            else:
                self.close()

    @staticmethod
    def validate_url(url):
        if not validators.url(url):
            url = 'http://' + url
            return validators.url(url), url
        return True, url

    @staticmethod
    def _err_msg_box(title, text, additional_txt = ''):
        not_valid_msg = QMessageBox()
        not_valid_msg.setIcon(QMessageBox.Warning)
        not_valid_msg.setWindowTitle(title)
        not_valid_msg.setText(text)
        not_valid_msg.setInformativeText(additional_txt)
        not_valid_msg.setStandardButtons(QMessageBox.Ok)
        _ = not_valid_msg.exec()

