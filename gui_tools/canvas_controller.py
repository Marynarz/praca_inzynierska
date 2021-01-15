import pandas as pd


class CanvasController:
    def __init__(self, canvases):
        self.canvases = canvases
        self.grid = False

    # data handling block
    ##
    # @brief upload_data - data_uploader
    #
    def upload_data(self, data=None, clear=False):
        if clear and data is None:
            data = pd.DataFrame()

        for canvas in self.canvases:
            self.canvases[canvas].upload_data(data)

    ##
    # @brief set_values - set x, y, z axis values
    #
    def set_values(self, val_name='', val_idx=0):
        for canvas in self.canvases:
            if val_name == 'y':
                self.canvases[canvas].set_y(val_idx)
            elif val_name == 'x':
                self.canvases[canvas].set_x(val_idx)

    # canvas view block
    ##
    # @brief set_grid - settin grid on/off
    #
    def set_grid(self):
        pass
