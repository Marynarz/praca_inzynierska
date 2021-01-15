from PyQt5.QtWidgets import QMainWindow, QTableView, QDockWidget, QWidget, QFormLayout, QComboBox,\
    QCheckBox, QTabWidget, QVBoxLayout, QPushButton, QGroupBox
from PyQt5.QtCore import QAbstractTableModel, Qt
from defs import str_defs, app_defs
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
    FNAME_TEMPLATE = 'DataViewer.{0!s}'

    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.par_ = parent
        if not data:
            data = pd.DataFrame((0, 0))
        self.data = pd.DataFrame((0, 0))
        self.col_names = []
        self.language = self.parent().language
        self.setWindowTitle(str_defs.SHOW_DATA_TITILE[self.language])
        self._prepare_window()
        self._create_dock()
        self.show_data()
        self.data = pd.DataFrame((0, 0))
        self.parent().log.write_log(app_defs.INFO_MSG,
                                    '{0!s} executed successfully'.format(self.FNAME_TEMPLATE.format('init')))

    def _prepare_window(self):
        self.main_view = QTableView()
        self.setCentralWidget(self.main_view)

    def _create_dock(self):
        self.main_tools_dock = QDockWidget(str_defs.DOCK_TITLE[self.language], self)
        self.dock_tabs = QTabWidget()

        self.dock_tabs.addTab(self._create_tab_overall(), str_defs.OVRALL[self.language])
        self.dock_tabs.addTab(self._create_tab_y(), 'Y')

        self.main_tools_dock.setWidget(self.dock_tabs)

        self.addDockWidget(Qt.RightDockWidgetArea, self.main_tools_dock)

    def _create_tab_overall(self):
        tab = QWidget()
        layout = QFormLayout()

        self.set_grid_box = QCheckBox(str_defs.GRID[self.language], self)
        self.set_grid_box.setChecked(self.parent().grid)
        self.set_grid_box.stateChanged.connect(self.parent().set_grid)

        plot_type_box = QComboBox()
        plot_type_box.addItems(str_defs.PLOT_TYPES[self.language])
        plot_type_box.currentIndexChanged.connect(self.parent().set_plot_type)

        sort_layout = QVBoxLayout()
        self.sort_items = QComboBox()
        self.sort_items.addItems(self.col_names)

        sort_cont = QGroupBox(str_defs.SORT_TOOL[self.language])
        sort_btn = QPushButton()
        sort_btn.setText(str_defs.SORT[self.language])
        sort_btn.clicked.connect(self.sort_values)

        sort_layout.addWidget(self.sort_items)
        sort_layout.addWidget(sort_btn)
        sort_cont.setLayout(sort_layout)

        layout.addWidget(self.set_grid_box)
        layout.addWidget(plot_type_box)
        layout.addWidget(sort_cont)

        tab.setLayout(layout)
        return tab

    def _create_tab_y(self):
        tab_y = QWidget()
        layout = QFormLayout()

        self.y_column_types = QComboBox()
        self.y_column_types.addItems(self.col_names)
        self.y_column_types.currentIndexChanged.connect(self.set_y)

        layout.addWidget(self.y_column_types)

        tab_y.setLayout(layout)

        return tab_y
        # plot_type_box.currentIndexChanged.connect(self.set_plot_type)

    def set_data(self, data):
        fname = self.FNAME_TEMPLATE.format('set_data')
        self.parent().log.write_log(app_defs.INFO_MSG, '{0!s}: Setting data into DataFrame'.format(fname))
        self.data = pd.DataFrame()
        self.data = data
        self.col_names = ['index'] + list(self.data.columns.values)

        self.col_names = [str(item).strip() for item in self.col_names]

        self.y_column_types.clear()
        self.y_column_types.addItems(self.col_names)
        self.sort_items.clear()
        self.sort_items.addItems(self.col_names)

        self.show_data()

    def get_data(self):
        return self.data

    def upd_grid(self):
        self.set_grid_box.blockSignals(True)
        self.set_grid_box.setCheckState(self.parent().grid)
        self.set_grid_box.blockSignals(False)

    def sort_values(self):
        fname = self.FNAME_TEMPLATE.format('sort_values')
        sort_by = self.col_names[self.sort_items.currentIndex()]

        try:
            if sort_by != 'index':
                self.data.sort_values(by=self.data.columns[self.sort_items.currentIndex() - 1], inplace=True)
                self.parent().log.write_log(app_defs.INFO_MSG,
                                            '%s: all values in dataframe are sorted by {%s}' %
                                            (fname, self.data.columns[self.sort_items.currentIndex() - 1]))
            else:
                self.data.sort_index(inplace=True)
                self.parent().log.write_log(app_defs.INFO_MSG, '%s: Data sorted by index' % fname)
        except Exception as e:
            self.parent().log.write_log(app_defs.WARNING_MSG, '%s: unable to sort values, exception = {%s}' % (fname,
                                                                                                               e))

        self.show_data()
        self.parent().load_data()
        self.parent().update_canvas_view()

    def show_data(self):
        model = TableModel(data=self.data)
        self.main_view.setModel(model)

    def set_y(self):
        y_pos = self.col_names[self.y_column_types.currentIndex()]
        if y_pos != 'index':
            col_idx = self.y_column_types.currentIndex() - 1
        else:
            col_idx = -1

        for canvas in self.parent().canvases:
            self.parent().canvases[canvas].set_y(col_idx)
            self.parent().update_canvas_view()

    def set_x(self):
        y_pos = self.col_names[self.y_column_types.currentIndex()]
        if y_pos != 'index':
            col_idx = self.y_column_types.currentIndex() - 1
        else:
            col_idx = -1

        for canvas in self.parent().canvases:
            self.parent().canvases[canvas].set_y(col_idx)
            self.parent().load_and_plot_data()
