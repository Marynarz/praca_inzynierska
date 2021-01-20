import sys
sys.path.append('..')

from defs import app_defs
import os
from gui_tools import logger, unittest


class UtLogger(unittest.TestCase):
    def setUp(self):
        self.log_dir = '../../log/unit_test.txt'

    def tearDown(self):
        os.remove(self.log_dir)

    def test01_logger(self):
        messages = ['%s: Test info message\n' % app_defs.INFO_MSG,
                    '%s: Test warning message\n' % app_defs.WARNING_MSG,
                    '%s: Test error message\n' % app_defs.ERROR_MSG]
        lines_readed = []
        test_logger = logger.Logger('unit_test')
        test_logger.write_log(app_defs.INFO_MSG, 'Test info message')
        test_logger.write_log(app_defs.WARNING_MSG, 'Test warning message')
        test_logger.write_log(app_defs.ERROR_MSG, 'Test error message')

        with open(self.log_dir) as f:
            for line in f:
                lines_readed.append(line)

        self.assertEqual(messages[0], lines_readed[1])
        self.assertEqual(messages[1], lines_readed[2])
        self.assertEqual(messages[2], lines_readed[3])


if __name__ == '__main__':
    unittest.main()
