from defs import app_defs
import pandas as pd
from gui_tools import logger


class FileValidator(object):
    values_pd = pd.DataFrame()
    FNAME_PATTERN = 'FileValidator.%s'
    validators_dict = {'txt': 'self.validate_txt_file',
                       'csv': 'self.validate_csv_file',
                       'json': 'self.validate_json_file'}

    def __init__(self, entry_point, append=False):
        self.entry_point = entry_point
        self.log = logger.Logger('FileValidator', append=append)

    def file_to_validate(self, source_file):
        fname = self.FNAME_PATTERN % 'file_to_validate'
        self.clear_values()

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

    def validate_txt_file(self, source_file):
        fname = self.FNAME_PATTERN % 'validate_txt_file'

        header = None
        with open(source_file, 'r') as f:
            first_line = f.readline()
            try:
                first_line = first_line.split(' ')
                float(first_line[0])
            except ValueError:
                self.log.write_log(app_defs.INFO_MSG, '%s: file with header. header: %s' % (fname, first_line))
                header = 0

        self.values_pd = pd.read_csv(source_file, sep=" ", header=header)

    def validate_csv_file(self, source_file):
        fname = self.FNAME_PATTERN % 'validate_csv_file'
        self.log.write_log(app_defs.INFO_MSG, '%s: csv file chosen, validate' % fname)

        header = None
        with open(source_file, 'r') as f:
            first_line = f.readline()
            try:
                first_line = first_line.split(',')
                float(first_line[0])
            except ValueError:
                self.log.write_log(app_defs.INFO_MSG, '%s: file with header. header: %s' % (fname, first_line))
                header = 0

        self.values_pd = pd.read_csv(source_file, header=header)

    def validate_json_file(self, source_file):
        fname = self.FNAME_PATTERN % 'validate_json_file'
        self.log.write_log(app_defs.INFO_MSG, '%s: json file chosen, validate' % fname)

        self.values_pd = pd.read_json(source_file)

    def get_values(self):
        fname = self.FNAME_PATTERN % 'get_values'
        self.log.write_log(app_defs.INFO_MSG, '%s: returning pandas data frame' % fname)
        return self.values_pd

    def clear_values(self):
        fname = self.FNAME_PATTERN % 'clear_values'
        self.log.write_log(app_defs.INFO_MSG, '%s: clear values' % fname)
        self.values_pd = self.values_pd[0:0]
        self.log.write_log(app_defs.INFO_MSG, '%s: check if empty: %s' % (fname, self.values_pd.empty))
