import unittest
import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from gui_tools import data_utils
import pandas as pd


class DataUtilsTest(unittest.TestCase):
    def setUp(self):
        self.test_dataframe = pd.DataFrame({'col1': [-1, 3, -5, 7], 'col2': [4, 3, 0, 2]})
        self.test_data_frame_non_negative = pd.DataFrame({'col1': [25, 50, 20, 30],
                                                          'col2': [3, 4.3, 2, 0.7],
                                                          'Percent': [30, 7, 63, 25]})
        self.wrong_values = [('3', 5), 'test_string', [], 5]

    def test01_filtering(self):
        test_data = self.test_dataframe
        print(test_data)

        filtered1 = data_utils.filter_negative_numbers(test_data, 0)
        print(filtered1)
        self.assertListEqual(filtered1['col1'].tolist(), [3, 7])
        self.assertListEqual(filtered1['col2'].tolist(), [3, 2])

        print(test_data)
        filtered2 = data_utils.filter_negative_numbers(test_data, 1)
        print(filtered2)
        self.assertListEqual(filtered2['col1'].tolist(), [-1, 3, 7])
        self.assertListEqual(filtered2['col2'].tolist(), [4, 3, 2])

    def test02_percent_to_radius(self):
        test_data = self.test_data_frame_non_negative
        test_results = [[90.0, 180.0, 72.0, 108.0],
                        [10.8, 15.48, 7.2, 2.52],
                        [108.0, 25.2, 226.8, 90.0]]

        test_cols = ('col1', 'col2', 'Percent')
        results = []

        for col in test_cols:
            ret = data_utils.percent_to_radius(test_data, col)
            results.append(ret['Radius'].tolist())

        self.assertListEqual(test_results, results)

    def test03_dataframe_to_radius(self):
        test_data = self.test_data_frame_non_negative
        test_results = [[72.0, 144.0, 57.6, 86.4],
                        [108.0, 154.8, 72.0, 25.2],
                        [86.4, 20.16, 181.44, 72.0]]
        results = []
        for i in range(3):
            ret = data_utils.dataframe_to_radius(test_data, i)
            results.append(ret['Radius'].tolist())

        self.assertListEqual(test_results, results)

    def test04_wrong_formats(self):
        test_data = self.wrong_values

        for value in test_data:
            with self.assertRaises(TypeError):
                data_utils.filter_negative_numbers(value)
            # Possible AttributeError and TypeError
            with self.assertRaises(Exception):
                data_utils.percent_to_radius(value, 'S')
            # Possible AttributeError and TypeError
            with self.assertRaises(Exception):
                data_utils.dataframe_to_radius(value, 0)


if __name__ == '__main__':
    unittest.main()
