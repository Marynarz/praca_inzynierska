from PyQt5.QtWidgets import QMainWindow, QTableView, QDockWidget, QWidget, QFormLayout, QComboBox,\
    QCheckBox, QTabWidget, QVBoxLayout, QPushButton, QGroupBox
from PyQt5.QtCore import QAbstractTableModel, Qt
from defs import str_defs, app_defs
from gui_tools import data_utils
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


class DataViewer(QTableView):
    FNAME_TEMPLATE = 'DataViewer.{0!s}'

    def __init__(self, parent=None):
        super().__init__(parent)
        print(parent)
        self.par_ = parent
        self.data = pd.DataFrame((0, 0))
        self.col_idx = self.data.columns[0]
        self.col_names = []
        self.language = self.parent().language
        self.show_data()
        self.parent().log.write_log(app_defs.INFO_MSG,
                                    '{0!s} executed successfully'.format(self.FNAME_TEMPLATE.format('init')))

    def create_dock(self):
        main_tools_dock = QDockWidget(str_defs.DOCK_TITLE[self.language], self)
        dock_tabs = QTabWidget()

        dock_tabs.addTab(self._create_tab_overall(), str_defs.OVRALL[self.language])
        dock_tabs.addTab(self._create_tab_x(), 'X')
        dock_tabs.addTab(self._create_tab_y(), 'Y')

        main_tools_dock.setWidget(dock_tabs)

        return main_tools_dock

    def _create_tab_overall(self):
        tab = QWidget()
        layout = QFormLayout()

        self.set_grid_box = QCheckBox(str_defs.GRID[self.language], self)
        self.set_grid_box.setChecked(self.parent().grid)
        self.set_grid_box.stateChanged.connect(self.parent().set_grid)

        self.plot_type_box = QComboBox()
        self.plot_type_box.addItems(str_defs.PLOT_TYPES[self.language])
        self.plot_type_box.currentIndexChanged.connect(self.set_plot_type)

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
        layout.addWidget(self.plot_type_box)
        layout.addWidget(sort_cont)

        tab.setLayout(layout)
        return tab

    def _create_tab_y(self):
        tab_y = QWidget()
        layout = QFormLayout()

        self.y_column_types = QComboBox()
        self.y_column_types.currentIndexChanged.connect(self.set_y)

        layout.addWidget(self.y_column_types)

        tab_y.setLayout(layout)

        return tab_y

    def _create_tab_x(self):
        tab_x = QWidget()
        layout = QFormLayout()

        self.x_column_types = QComboBox()
        self.x_column_types.currentIndexChanged.connect(self.set_x)

        layout.addWidget(self.x_column_types)

        tab_x.setLayout(layout)

        return tab_x

    def set_data(self, data):
        fname = self.FNAME_TEMPLATE.format('set_data')
        self.parent().log.write_log(app_defs.INFO_MSG, '{0!s}: Setting data into DataFrame'.format(fname))
        self.data = pd.DataFrame()
        self.data = data
        self.col_names = ['index'] + list(self.data.columns.values)

        self.col_names = [str(item).strip() for item in self.col_names]

        self.y_column_types.clear()
        self.y_column_types.addItems(self.col_names)
        self.x_column_types.clear()
        self.x_column_types.addItems(self.col_names)
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
                self.data.sort_values(by=self.data.columns[self.sort_items.currentIndex() - 1], inplace=True,
                                      ignore_index=True)
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
        self.parent().canvas_controller.upload_data(self.data)

    def show_data(self):
        model = TableModel(data=self.data)
        self.setModel(model)

    def set_y(self):
        y_pos = self.col_names[self.y_column_types.currentIndex()]
        if y_pos != 'index':
            self.col_idx = self.y_column_types.currentIndex() - 1
        else:
            self.col_idx = -1

        self.parent().canvas_controller.set_values('y', self.col_idx)

    def set_x(self):
        x_pos = self.col_names[self.x_column_types.currentIndex()]
        if x_pos != 'index':
            col_idx = self.x_column_types.currentIndex() - 1
        else:
            col_idx = -1

        self.parent().canvas_controller.set_values('x', col_idx)

    def set_plot_type(self, plot_type):
        # filtering data for pie chart (negative values are not possible)
        if plot_type + 1 == app_defs.PlotTypes.PIE_CHART:
            ret = data_utils.filter_negative_numbers(self.data, self.col_idx)
            ret = data_utils.dataframe_to_radius(ret, self.col_idx)
            self.set_data(ret)
            self.show_data()
        self.parent().canvas_controller.change_plot_type(plot_type + 1)

        self.plot_type_box.blockSignals(True)
        self.plot_type_box.setCurrentIndex(plot_type)
        self.plot_type_box.blockSignals(False)

        self.parent().plot_type_box.blockSignals(True)
        self.parent().plot_type_box.setCurrentIndex(plot_type)
        self.parent().plot_type_box.blockSignals(False)
