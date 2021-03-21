from PyQt5.QtWidgets import QWidget, QFormLayout, QLabel, QLineEdit
import validators
import pandas as pd


class JsonUrlOpen(QWidget):
    def __init__(self, data_viewer=None):
        super().__init__()
        self.dv = data_viewer
        layout = QFormLayout()
        self.url_set = QLineEdit('Type url here')
        self.url_set.textChanged.connect(self.download_json)
        layout.addRow('Url:', self.url_set)
        self.setLayout(layout)

    @staticmethod
    def validate_url(url):
        return validators.url(url)

    def download_json(self, text):
        if not self.validate_url(text):
            print("Wrong JSON url!")
        else:
            data = pd.read_json(text)
            data = pd.json_normalize(data)
            print(data)
            self.dv.set_data(data)

