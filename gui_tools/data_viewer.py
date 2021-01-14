from PyQt5.QtWidgets import QMainWindow, QTableView, QDockWidget, QWidget, QFormLayout, QComboBox, QCheckBox, QTabWidget
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
        self.par_ = parent
        if not data:
            data = pd.DataFrame((0, 0))
        self.data = pd.DataFrame((0, 0))
        self.grid = self.parent().grid
        self.col_names = []
        self.language = self.parent().language
        self.setWindowTitle(str_defs.SHOW_DATA_TITILE[self.language])
        self._prepare_window()
        self._create_dock()
        self.show_data()
        self.data = pd.DataFrame((0, 0))

    def _prepare_window(self):
        self.main_view = QTableView()
        self.setCentralWidget(self.main_view)

    def _create_dock(self):
        self.main_tools_dock = QDockWidget(str_defs.DOCK_TITLE[self.language], self)
        self.dock_tabs = QTabWidget()

        self.dock_tabs.addTab(self._create_tab_overall(), 'Overall')
        self.dock_tabs.addTab(self._create_tab_y(), 'Y')

        self.main_tools_dock.setWidget(self.dock_tabs)

        self.addDockWidget(Qt.RightDockWidgetArea, self.main_tools_dock)

    def _create_tab_overall(self):
        tab = QWidget()
        layout = QFormLayout()

        set_grid_box = QCheckBox(str_defs.GRID[self.language], self)
        set_grid_box.setChecked(self.grid)
        set_grid_box.stateChanged.connect(self.parent().set_grid)

        plot_type_box = QComboBox()
        plot_type_box.addItems(str_defs.PLOT_TYPES[self.language])
        plot_type_box.currentIndexChanged.connect(self.parent().set_plot_type)

        layout.addWidget(set_grid_box)
        layout.addWidget(plot_type_box)

        tab.setLayout(layout)
        return tab

    def _create_tab_y(self):
        tab_y = QWidget()
        layout = QFormLayout()

        self.y_column_types = QComboBox()
        self.y_column_types.addItems(self.col_names)

        layout.addWidget(self.y_column_types)

        tab_y.setLayout(layout)

        return tab_y
        # plot_type_box.currentIndexChanged.connect(self.set_plot_type)

    def set_data(self, data):
        self.data = pd.DataFrame()
        self.data = data
        self.col_names = ['index'] + list(self.data.columns.values)

        self.col_names = [str(item) for item in self.col_names]

        self.y_column_types.clear()
        self.y_column_types.addItems(self.col_names)

        self.show_data()

    def get_data(self):
        return self.data

    def upd_grid(self, grid=False):
        self.grid = grid

    def sort_values(self):
        self.data.sort(key=operator.itemgetter(0))

    def show_data(self):
        model = TableModel(data=self.data)
        self.main_view.setModel(model)
