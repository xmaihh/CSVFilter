from .csv_preprocess import DataPreprocessor


def create_csv_preprocess(csv_filepath):
    return DataPreprocessor(csv_filepath)


__all__ = ["create_csv_preprocess"]
