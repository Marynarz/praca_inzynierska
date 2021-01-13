from PyQt5.QtWidgets import QMainWindow, QTableView, QDockWidget, QWidget, QFormLayout, QLineEdit, QComboBox
from PyQt5.QtCore import QAbstractTableModel, Qt
import operator
from defs import str_defs
import pandas as pd


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return str(self._data.iloc[index.row(), index.column()])
        return None

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, col, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._data.columns[col]
            if orientation == Qt.Vertical:
                return str(self._data.index[col])
        return None


class DataViewer(QMainWindow):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        if not data:
            data = pd.DataFrame((0, 0))
        self.data = data
        self.col_names = []
        self.language = self.parent().language
        self.setWindowTitle(str_defs.SHOW_DATA_TITILE[self.language])
        self._prepare_window()
        self.show_data()

    def _prepare_window(self):
        self.main_view = QTableView()
        self.setCentralWidget(self.main_view)

    def _create_dock(self):
        self.main_tools_dock = QDockWidget(str_defs.DOCK_TITLE[self.language], self)
        self.dock_widget = QWidget()
        dock_layout = QFormLayout()

        self.dock_widget.setLayout(dock_layout)

        self.main_tools_dock.setWidget(self.docket_widget)

        self.addDockWidget(Qt.RightDockWidgetArea, self.main_tools_dock)

    def _create_tab_y(self):
        self.tab_y = QWidget()
        layout = QFormLayout()

        y_column_types = QComboBox()
        y_column_types.addItems(self.col_names)
        # plot_type_box.currentIndexChanged.connect(self.set_plot_type)

    def set_data(self, data):
        self.data = pd.DataFrame()
        self.data = data
        self.col_names = ['index'].join(self.data.columns.toList())
        self.show_data()

    def get_data(self):
        return self.data

    def sort_values(self):
        self.data.sort(key=operator.itemgetter(0))

    def show_data(self):
        model = TableModel(data=self.data)
        self.main_view.setModel(model)
