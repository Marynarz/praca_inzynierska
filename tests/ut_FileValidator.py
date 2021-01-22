import sys
import os
import unittest
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from defs import app_defs
from gui_tools import FileValidator


class FileValidatorTest(unittest.TestCase):
    def setUp(self):
        self.returned_data = ([1, 3, 10, -1], [2, 2, 3, -1])
        self.headers = ['x', 'y']

    def test01_init(self):
        test_class = FileValidator.FileValidator('test')

        self.assertEqual(test_class.entry_point, 'test')

    def test02_wrong_file_to_validate(self):
        test_class = FileValidator.FileValidator('test')

        returned = test_class.file_to_validate('testowy.source')

        self.assertEqual(returned, app_defs.UNKNOWN_FILE_TYPE)

    def test03_txt_file_validate(self):
        test_class = FileValidator.FileValidator('test')

        returned = test_class.file_to_validate('tests/ut_data/test_data.txt')
        self.assertEqual(returned, app_defs.NOERROR)

        for i in range(2):
            self.assertListEqual(self.returned_data[i], test_class.get_values()[i].tolist())

    def test04_csv_file_validate(self):
        test_class = FileValidator.FileValidator('test')

        returned = test_class.file_to_validate('tests/ut_data/test_data.csv')
        self.assertEqual(returned, app_defs.NOERROR)

        for i in range(2):
            self.assertListEqual(self.returned_data[i], test_class.get_values()[i].tolist())

    def test05_json_file_validate(self):
        test_class = FileValidator.FileValidator('test')

        returned = test_class.file_to_validate('tests/ut_data/test_data.json')
        self.assertEqual(returned, app_defs.NOERROR)

        for i in range(2):
            self.assertListEqual(self.returned_data[i], test_class.get_values()[i].tolist())

    def test06_txt_file_with_header_validate(self):
        test_class = FileValidator.FileValidator('test')

        returned = test_class.file_to_validate('tests/ut_data/test_data_with_header.txt')
        self.assertEqual(returned, app_defs.NOERROR)
        self.assertListEqual(self.headers, test_class.get_values().columns.tolist())

        for i in range(2):
            self.assertListEqual(self.returned_data[i], test_class.get_values()[self.headers[i]].tolist())

    def test07_csv_file_with_header_validate(self):
        test_class = FileValidator.FileValidator('test')

        returned = test_class.file_to_validate('tests/ut_data/test_data_with_header.csv')
        self.assertEqual(returned, app_defs.NOERROR)
        self.assertListEqual(self.headers, test_class.get_values().columns.tolist())

        for i in range(2):
            self.assertListEqual(self.returned_data[i], test_class.get_values()[self.headers[i]].tolist())

    def test08_json_file_with_header_validate(self):
        test_class = FileValidator.FileValidator('test')

        returned = test_class.file_to_validate('tests/ut_data/test_data_with_header.json')
        self.assertEqual(returned, app_defs.NOERROR)
        self.assertListEqual(self.headers, test_class.get_values().columns.tolist())

        for i in range(2):
            self.assertListEqual(self.returned_data[i], test_class.get_values()[self.headers[i]].tolist())


if __name__ == '__main__':
    unittest.main()
