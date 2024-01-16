class BaseFilter:
    def __init__(self, input_path):
        self.input_path = input_path
        self.output_path = self._get_output_filepath()

    def _get_output_filepath(self):
        raise NotImplementedError

    def _get_file_encoding(self):
        raise NotImplementedError

    def save_to(self):
        return self.output_path
