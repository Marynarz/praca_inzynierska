class CanvasMock:
    def __init__(self):
        self.data = 0
        self.y_idx = 0
        self.x_idx = 0
        self.show_plot_counter = 0
        self.grid = False
        self.clear_counter = 0
        self.set_plot_type_counter = 0
        self.set_plot_type_types = []

    def upload_data(self, data):
        self.data = data

    def show_plot(self):
        self.show_plot_counter += 1

    def set_grid_(self, state):
        self.grid = state

    def set_line(self):
        pass

    def clear_plot(self):
        self.clear_counter += 1

    def set_plot_type(self, type_no):
        self.set_plot_type_counter += 1
        self.set_plot_type_types.append(type_no)

    def set_x(self, x_idx):
        self.x_idx = x_idx

    def set_y(self, y_idx):
        self.y_idx = y_idx
