from .easily_filter_csv_file import EasillyFilterCSVFile


def create_easily_filter_csv_file(input_file, output_file_prefix):
    return EasillyFilterCSVFile(input_file, output_file_prefix)


__all__ = ["create_easily_filter_csv_file"]
