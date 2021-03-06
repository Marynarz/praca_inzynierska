from defs import str_defs
from enum import IntEnum
NOERROR = 0
NO_ACTION = 1
UNKNOWN_FILE_TYPE = 10
UNABLE_TO_OPEN_FILE = 11
REBOOT_APP = -123

LOG_DIR_MAX_ATTEMPT = 3

# log defs
INFO_MSG = 0x0000100
WARNING_MSG = 0x0000200
ERROR_MSG = 0x0000300
FUNIN_MSG = 0x0000400
FUNOUT_MSG = 0x0000500

# misc
DEFAULT_PLOT = [(-100, 50), (-50, -50), (0, 0), (50, -50), (100, 50)]
STATUS_TIMEOUT = 10000

# Canvases namespace
MATPLOTLIB = 'MPL'
PYQTGRAPH = 'PQG'
BOKEH = 'BKH'
PLOTLY = 'PLT'

CANVAS_NAME = {MATPLOTLIB: str_defs.MAT_PLOT_LIB, PYQTGRAPH: str_defs.QTGRAPH,
               BOKEH: str_defs.BOKEH, PLOTLY: str_defs.PLOTLY}


class PlotTypes(IntEnum):
    D2_CHART = 1     # 2D - chart
    PIE_CHART = 2    # Pie chart
    BAR_CHART = 3    # Bar chart
