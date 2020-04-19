class FileValidatorTxt(object):
    # value = (x, y)
    values = []

    def __init__(self):
        pass

    def validate_txt_file(self, source_file):
        try:
            with open(source_file, 'r') as file:
                for line in file:
                    tmp_str = line.split(' ')
                    self.values.append((tmp_str[0], tmp_str[2]))
        except Exception as e:
            print(e)

    def get_values(self):
        return self.get_values()
