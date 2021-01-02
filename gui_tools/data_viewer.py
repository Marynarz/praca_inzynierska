from PyQt5.QtWidgets import QMainWindow, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt
import operator
from defs import str_defs


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])


class DataViewer(QMainWindow):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        if not data:
            data = [(0, 0), ]
        self.data = data
        self.language = self.parent().language
        self.setWindowTitle(str_defs.SHOW_DATA_TITILE[self.language])
        self._prepare_window()
        self.show_data()

    def _prepare_window(self):
        self.main_view = QTableView()
        self.setCentralWidget(self.main_view)

    def set_data(self, data):
        self.data = data
        self.sort_values()
        self.show_data()

    def get_data(self):
        return self.data

    def sort_values(self):
        self.data.sort(key=operator.itemgetter(0))

    def show_data(self):
        model = TableModel(data=self.data)
        self.main_view.setModel(model)
