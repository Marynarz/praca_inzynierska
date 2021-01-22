import unittest
import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from ut_mocks import CanvasMock
from gui_tools.canvas_controller import CanvasController
from defs.app_defs import PlotTypes
import pandas as pd


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.canvases = {'canvas_1': CanvasMock(), 'canvas_2': CanvasMock()}
        self.test_data = pd.DataFrame(((1, 3, 10, -1), (2, 2, -1, 3)))
        self.plot_type_scenario = [PlotTypes.PIE_CHART, PlotTypes.BAR_CHART,
                                   PlotTypes.D2_CHART, PlotTypes.BAR_CHART]

    def test01_data_handling(self):
        # uploading data
        test_controller = CanvasController(canvases=self.canvases)
        test_controller.upload_data(self.test_data)

        for canvas in self.canvases:
            self.assertEqual(self.test_data.columns.tolist(), self.canvases[canvas].data.columns.tolist())

        test_controller.upload_data(clear=True)
        for canvas in self.canvases:
            self.assertTrue(self.canvases[canvas].data.empty)

        print(self.test_data)

    def test02_set_values(self):
        test_controller = CanvasController(canvases=self.canvases)

        # setting x
        test_controller.set_values('x', 666)

        for canvas in self.canvases:
            self.assertEqual(666, self.canvases[canvas].x_idx)

        # setting y
        test_controller.set_values('y', 999)

        for canvas in self.canvases:
            self.assertEqual(999, self.canvases[canvas].y_idx)
            self.assertEqual(666, self.canvases[canvas].x_idx)

        with self.assertRaises(ValueError):
            test_controller.set_values('wong_value', 999)

        # test of clearing up canvases
        test_controller.clear_plot(all=True)
        for canvas in self.canvases:
            self.assertEqual(0, self.canvases[canvas].y_idx)
            self.assertEqual(0, self.canvases[canvas].x_idx)
            self.assertEqual(4, self.canvases[canvas].clear_counter)
            self.assertEqual(2, self.canvases[canvas].show_plot_counter)

    def test03_set_grid(self):
        test_controller = CanvasController(canvases=self.canvases)

        print('Check initial state of grid')
        for canvas in self.canvases:
            self.assertFalse(self.canvases[canvas].grid)

        print('Setting grid to true')
        test_controller.set_grid()
        for canvas in self.canvases:
            self.assertTrue(self.canvases[canvas].grid)
            self.assertEqual(1, self.canvases[canvas].clear_counter)
            self.assertEqual(1, self.canvases[canvas].show_plot_counter)

        print('Setting grid to False')
        test_controller.set_grid()
        for canvas in self.canvases:
            self.assertFalse(self.canvases[canvas].grid)
            self.assertEqual(2, self.canvases[canvas].clear_counter)
            self.assertEqual(2, self.canvases[canvas].show_plot_counter)

    def test04_set_plot_type(self):
        test_controller = CanvasController(canvases=self.canvases)

        for type in self.plot_type_scenario:
            test_controller.change_plot_type(type)

        for canvas in self.canvases:
            self.assertListEqual(self.plot_type_scenario, self.canvases[canvas].set_plot_type_types)


if __name__ == '__main__':
    unittest.main()
