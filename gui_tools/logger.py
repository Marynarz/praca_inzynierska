from defs import app_defs
import time
import os


class Logger(object):
    def __init__(self, log_point, append=False):
        self.file_name = None
        path = 'log'
        if not os.path.isdir(path):
            os.mkdir(path)

        self.file_name = path + '/' + log_point + '.txt'
        self.append = 'a' if append else 'w+'

        with open(self.file_name, self.append) as f:
            f.write('Start logging at: ' + str(time.time()) + ' from: ' + log_point + '\n')

    def write_log(self, msg_code, msg):
        with open(self.file_name, 'a') as f:
            f.write(str(msg_code) + ': ' + msg + '\n')
