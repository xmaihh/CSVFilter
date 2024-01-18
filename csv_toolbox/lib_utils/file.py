import os


def generate_unique_output_path(input_dir, output_filename, extension):
    """
    Generates a unique output file path by appending a number to the file name.

    Args:
        input_dir (str): Directory where the output file should be saved.
        output_filename (str): Base output file name without extension.
        extension (str): Extension for the output file.

    Returns:
        str: Unique output file path.
    """

    # Start with the base output file path
    output_path = os.path.join(input_dir, output_filename)
    # Append a number to the file name until we find a unique path
    i = 1
    while os.path.exists(output_path):
        output_path = os.path.join(
            input_dir, f"{os.path.splitext(output_filename)[0]}_{i}{extension}"
        )
        i += 1

    return output_path


def delete_file(file_path):
    """
    Deletes a file at the specified path.

    Args:
        file_path (str): Path to the file to be deleted.
    """

    # Check if the file exists
    if os.path.exists(file_path):
        # Delete the file
        os.remove(file_path)
    else:
        # Raise an error if the file does not exist
        raise FileNotFoundError(f"File not found: {file_path}")


def rename_file(old_path, new_path, extension):
    new_path = generate_unique_output_path(
        os.path.dirname(new_path),
        f"{os.path.splitext(os.path.basename(new_path))[0]}{extension}",
        extension,
    )
    os.rename(old_path, new_path)
    return new_path
