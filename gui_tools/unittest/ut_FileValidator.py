import sys
sys.path.append('../..')

import unittest
import app_defs
from gui_tools import FileValidator


class FileValidatorTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test01_init(self):
        test_class = FileValidator.FileValidator('test')

        self.assertEqual(test_class.entry_point, 'test')

    def test02_wrong_file_to_validate(self):
        test_class = FileValidator.FileValidator('test')

        returned = test_class.file_to_validate('testowy.source')

        self.assertEqual(returned, app_defs.UNKNOWN_FILE_TYPE)

    def test03_txt_file_validate(self):
        returned_list = [(-1, -1), (1, 2), (3, 2), (10, 3)]
        test_class = FileValidator.FileValidator('test')

        returned = test_class.file_to_validate('ut_data/test_data.txt')

        self.assertEqual(returned, app_defs.NOERROR)
        self.assertListEqual(returned_list, test_class.get_values())


if __name__ == '__main__':
    unittest.main()
