import os

from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_path: str = os.path.abspath(working_directory)
        target_dir: str = os.path.normpath(os.path.join(abs_path, file_path))
        valid_target_dir: bool = os.path.commonpath([abs_path, target_dir]) == abs_path

        if valid_target_dir is False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_dir, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

        return content
    except Exception as e:
        return f"Error: {e}"
