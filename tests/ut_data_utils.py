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


if __name__ == '__main__':
    unittest.main()
