from defs import app_defs
import operator
from gui_tools import logger
import csv


class FileValidator(object):
    # value = (x, y)
    values = []
    FNAME_PATTERN = 'FileValidator.%s'
    validators_dict = {'txt': 'self.validate_txt_file', 'csv': 'self.validate_csv_file'}

    def __init__(self, entry_point):
        self.entry_point = entry_point
        self.log = logger.Logger('FileValidator')

    def file_to_validate(self, source_file):
        fname = self.FNAME_PATTERN % 'file_to_validate'

        filetype = source_file.split('.')[-1]
        try:
            self.log.write_log(app_defs.INFO_MSG, '%s: file type chosen to validate: {%s}' % (fname, filetype))
            eval(self.validators_dict[filetype])(source_file)
        except KeyError as e:
            self.log.write_log(app_defs.INFO_MSG, '%s: Unknown file type for file: {%s}' % (fname, source_file))
            return app_defs.UNKNOWN_FILE_TYPE
        except Exception as e:
            self.log.write_log(app_defs.ERROR_MSG, '%s: Exception while handling file: %s, exception details {%s}'
                               % (fname, source_file, e))
            return app_defs.UNABLE_TO_OPEN_FILE
        else:
            return app_defs.NOERROR

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

    def validate_csv_file(self, source_file, sort=False):
        fname = self.FNAME_PATTERN % 'validate_csv_file'
        self.log.write_log(app_defs.INFO_MSG, '%s: csv file chosen, validate' % fname)

        with open(source_file, newline='') as file:
            reader = csv.reader(file, dialect='excel')
            for row in reader:
                self.values.append((float(row[0]), float(row[1])))

        if sort:
            self.sort_values()

    def sort_values(self):
        self.values.sort(key=operator.itemgetter(0))

    def get_values(self):
        return self.values
