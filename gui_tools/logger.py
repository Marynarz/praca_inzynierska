import app_defs
import time
import os


class Logger(object):
    def __init__(self, log_point):
        self.file_name = None
        path = 'log'
        attempt_cnt = 0
        while not os.path.isdir(path) and attempt_cnt != app_defs.LOG_DIR_MAX_ATTEMPT:
            attempt_cnt += 1
            path = '../' + path

        if attempt_cnt == app_defs.LOG_DIR_MAX_ATTEMPT:
            raise NotADirectoryError('Unable to find log directory')

        self.file_name = path + '/' + log_point + '.txt'
        with open(self.file_name, 'w+') as f:
            f.write('Start logging at: ' + str(time.time()) + ' from: ' + log_point + '\n')

    def write_log(self, msg_code, msg):
        with open(self.file_name, 'a') as f:
            f.write(str(msg_code) + ': ' + msg + '\n')
