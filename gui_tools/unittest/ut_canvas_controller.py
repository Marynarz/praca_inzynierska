import unittest
from gui_tools.unittest.ut_mocks import CanvasMock
from gui_tools.canvas_controller import CanvasController
import pandas as pd


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.canvases = {'canvas_1': CanvasMock(), 'canvas_2': CanvasMock()}
        self.test_data = pd.DataFrame(((1, 3, 10, -1), (2, 2, -1, 3)))

    def test_data_handling(self):
        # uploading data
        test_controller = CanvasController(canvases=self.canvases)
        test_controller.upload_data(self.test_data)

        for canvas in self.canvases:
            self.assertEqual(self.test_data.columns.tolist(), self.canvases[canvas].data.columns.tolist())

        test_controller.upload_data(clear=True)
        for canvas in self.canvases:
            self.assertTrue(self.canvases[canvas].data.empty)

        print(self.test_data)


if __name__ == '__main__':
    unittest.main()
