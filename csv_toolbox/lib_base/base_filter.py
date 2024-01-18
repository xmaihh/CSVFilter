import chardet
import os
from csv_toolbox.lib_utils.file import generate_unique_output_path


class BaseFilter:
    def __init__(self, input_path, output_file_prefix, output_file_extension):
        self.input_path = input_path
        self.output_path = self._get_output_filepath(
            output_prefix=output_file_prefix, extension=output_file_extension
        )

    def _get_output_filepath(self, output_prefix, extension):
        """
        Constructs and returns the output file path based on certain rules.

        Args:
            output_prefix (str): Prefix to be added to the output file name.
            extension (str): Extension for the output file.

        Returns:
            str: Path to the output file.
        """

        input_path = self.input_path
        input_dir, input_filename = os.path.split(input_path)
        input_filename, _ = os.path.splitext(input_filename)
        output_filename = output_prefix + input_filename + extension
        output_path = os.path.join(input_dir, output_filename)
        # Check if the output file already exists
        if os.path.exists(output_path):
            # Generate a new output file path by appending a number to the file name
            output_path = generate_unique_output_path(
                input_dir, output_filename, extension
            )
        return output_path

    def _get_file_encoding(self):
        # Open the input file in read-binary mode.
        # This ensures that the file's contents are read as raw bytes,
        # without any interpretation or conversion.
        with open(self.input_path, "rb") as f:
            # Read the entire file's contents into memory.
            # This step loads the entire file into the program's memory.
            file_content = f.read()

            # Use the chardet library to detect the file's encoding.
            # The chardet library analyzes the file's contents and tries to identify
            # the encoding used to represent the characters in the file.
            result = chardet.detect(file_content)

            # Return the detected encoding.
            # The chardet library returns a dictionary with information about the
            # detected encoding. This code specifically retrieves the value associated
            # with the "encoding" key, which represents the detected encoding of the file.
            return result["encoding"]

    def save_to(self):
        return self.output_path
