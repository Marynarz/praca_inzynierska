import pandas as pd


##
# @brief CanvasController - wrapper and controller for all canvases
#
class CanvasController:
    def __init__(self, canvases):
        self.canvases = canvases
        self.grid = False

    # data handling block
    ##
    # @brief upload_data - data_uploader
    #
    def upload_data(self, data=None, clear=False):
        self.clear_plot()
        if clear and data is None:
            data = pd.DataFrame()

        for canvas in self.canvases:
            self.canvases[canvas].upload_data(data)
        self.show_plot()

    ##
    # @brief set_values - set x, y, z axis values
    #
    def set_values(self, val_name='', val_idx=0):
        self.clear_plot()
        for canvas in self.canvases:
            if val_name == 'y':
                self.canvases[canvas].set_y(val_idx)
            elif val_name == 'x':
                self.canvases[canvas].set_x(val_idx)
        self.show_plot()

    # canvas view block
    def clear_plot(self):
        for key in self.canvases:
            self.canvases[key].clear_plot()

    ##
    # @brief show_plot - show updated plot
    #
    def show_plot(self):
        for key in self.canvases:
            self.canvases[key].show_plot()

    ##
    # @brief set_grid - setting grid on/off
    #
    def set_grid(self):
        self.grid = not self.grid
        self.clear_plot()
        for key in self.canvases:
            self.canvases[key].set_grid_(self.grid)
        self.show_plot()

    def change_plot_type(self, type_no):
        self.clear_plot()
        for key in self.canvases:
            self.canvases[key].set_plot_type(type_no)
        self.show_plot()
