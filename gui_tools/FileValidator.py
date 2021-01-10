from defs import app_defs
import pandas as pd
import operator
from gui_tools import logger
import csv


class FileValidator(object):
    values_pd = pd.DataFrame()
    FNAME_PATTERN = 'FileValidator.%s'
    validators_dict = {'txt': 'self.validate_txt_file', 'csv': 'self.validate_csv_file'}

    def __init__(self, entry_point):
        self.entry_point = entry_point
        self.log = logger.Logger('FileValidator')

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

    def validate_txt_file(self, source_file, sort=True):
        fname = self.FNAME_PATTERN % 'validate_txt_file'

        header = None
        with open(source_file, 'r') as f:
            first_line = f.readline()
            try:
                first_line = first_line.split(' ')
                float(first_line[0])
            except ValueError as e:
                self.log.write_log(app_defs.INFO_MSG, '%s: file with header. header: %s' % (fname, first_line))
                header = 0

        self.values_pd = pd.read_csv(source_file, sep=" ", header=header)

        if sort:
            self.sort_values()

    def validate_csv_file(self, source_file, sort=True):
        fname = self.FNAME_PATTERN % 'validate_csv_file'
        self.log.write_log(app_defs.INFO_MSG, '%s: csv file chosen, validate' % fname)

        header = None
        with open(source_file, 'r') as f:
            first_line = f.readline()
            try:
                first_line = first_line.split(',')
                float(first_line[0])
            except ValueError as e:
                self.log.write_log(app_defs.INFO_MSG, '%s: file with header. header: %s' % (fname, first_line))
                header = 0

        self.values_pd = pd.read_csv(source_file, header=header)

        if sort:
            self.sort_values()

    def validate_json_file(self, source_file, sort=True):
        fname = self.FNAME_PATTERN % 'validate_json_file'
        self.log.write_log(app_defs.INFO_MSG, '%s: json file chosen, validate' % fname)

        self.values_pd = pd.read_json(source_file)

        if sort:
            self.sort_values()

    def sort_values(self):
        fname = self.FNAME_PATTERN % 'sort_values'
        try:
            self.values_pd.sort_values(by=self.values_pd.columns[0], inplace=True)
        except Exception as e:
            self.log.write_log(app_defs.WARNING_MSG, '%s: unable to sort values, excpetion = {%s}' % (fname, e))

    def get_values(self):
        print(type(self.values_pd))
        print(self.values_pd)
        return self.values_pd

    def clear_values(self):
        fname = self.FNAME_PATTERN % 'clear_values'
        self.log.write_log(app_defs.INFO_MSG, '%s: clear values' % fname)
        self.values_pd = []
