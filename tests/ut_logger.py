import unittest
from unittest import mock
import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
from defs import app_defs
import os
from gui_tools import logger
import time


class UtLogger(unittest.TestCase):
    def setUp(self):
        self.log_dir = 'log/unit_test.txt'

    def tearDown(self):
        os.remove(self.log_dir)

    @mock.patch('time.time', mock.MagicMock(return_value=666))
    def test01_logger(self):
        messages = ['Start logging at: 666 from: unit_test\n',
                    '%s: Test info message\n' % app_defs.INFO_MSG,
                    '%s: Test warning message\n' % app_defs.WARNING_MSG,
                    '%s: Test error message\n' % app_defs.ERROR_MSG]
        test_logger = logger.Logger('unit_test')
        test_logger.write_log(app_defs.INFO_MSG, 'Test info message')
        test_logger.write_log(app_defs.WARNING_MSG, 'Test warning message')
        test_logger.write_log(app_defs.ERROR_MSG, 'Test error message')

        with open(self.log_dir) as f:
            idx = 0
            for line in f:
                self.assertEqual(messages[idx], line)
                idx += 1


if __name__ == '__main__':
    unittest.main()
