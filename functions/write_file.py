import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_path: str = os.path.abspath(working_directory)
        target_dir: str = os.path.normpath(os.path.join(abs_path, file_path))
        valid_target_dir: bool = os.path.commonpath([abs_path, target_dir]) == abs_path

        if valid_target_dir is False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent_dir = os.path.dirname(target_dir)
        os.makedirs(parent_dir, exist_ok=True)

        with open(target_dir, "w") as f:
            content_chars = f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
