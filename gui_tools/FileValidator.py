import app_defs
from gui_tools import logger


class FileValidator(object):
    # value = (x, y)
    values = []

    def __init__(self, entry_point):
        self.entry_point = entry_point
        self.log = logger.Logger('FileValidator_' + str(self))

    def file_to_validate(self, source_file):
        if '.txt' in source_file:
            self.validate_txt_file(source_file)
            return app_defs.NOERROR
        else:
            return app_defs.UNKNOWN_FILE_TYPE

    def validate_txt_file(self, source_file):
        try:
            with open(source_file, 'r') as file:
                for line in file:
                    tmp_str = line.split(' ')
                    self.values.append((int(tmp_str[0]), int(tmp_str[1])))
        except Exception as e:
            print(e)

    def get_values(self):
        return self.values
