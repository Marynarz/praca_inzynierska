import app_defs
import operator
from gui_tools import logger


class FileValidator(object):
    # value = (x, y)
    values = []
    FNAME_PATTERN = 'FileValidator.%s'

    def __init__(self, entry_point):
        self.entry_point = entry_point
        self.log = logger.Logger('FileValidator')

    def file_to_validate(self, source_file):
        fname = self.FNAME_PATTERN % 'file_to_validate'
        if '.txt' in source_file:
            self.log.write_log(app_defs.INFO_MSG, '%s: TXT file chosen to validate: {%s}' % (fname, source_file))
            try:
                self.validate_txt_file(source_file)
            except Exception as e:
                self.log.write_log(app_defs.ERROR_MSG, '%s: Exception while handling file: %s, exception details {%s}'
                                   % (fname, source_file, e))
                return app_defs.UNABLE_TO_OPEN_FILE
            return app_defs.NOERROR
        else:
            self.log.write_log(app_defs.INFO_MSG, '%s: Unknown file type for file: {%s}' % (fname, source_file))
            return app_defs.UNKNOWN_FILE_TYPE

    def validate_txt_file(self, source_file, sort=False):
        fname = self.FNAME_PATTERN % 'validate_txt_file'
        self.log.write_log(app_defs.INFO_MSG, '%s: txt file chosen, validate' % fname)
        try:
            with open(source_file, 'r') as file:
                self.values.clear()
                for line in file:
                    tmp_str = line.split(' ')
                    self.values.append((float(tmp_str[0]), float(tmp_str[1])))
        except Exception as e:
            self.log.write_log(app_defs.ERROR_MSG, ' %s: Exception when validating file. {error=%s}' % (fname, e))
            raise e

        if sort:
            self.sort_values()

    def sort_values(self):
        self.values.sort(key=operator.itemgetter(0))

    def get_values(self):
        return self.values
