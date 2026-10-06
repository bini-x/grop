import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_path: str = os.path.abspath(working_directory)
        target_dir: str = os.path.normpath(os.path.join(abs_path, directory))
        valid_target_dir: bool = os.path.commonpath([abs_path, target_dir]) == abs_path

        if valid_target_dir is False:
            return f'    Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'    Error: "{directory}" is not a directory'

        string_to_return = ""

        dir_contents = os.listdir(target_dir)
        for i in dir_contents:
            full_path = os.path.join(target_dir, i)
            is_dir = os.path.isdir(full_path)
            contents_size = os.path.getsize(full_path)
            string_to_return += (
                f" - {i}: file_size={contents_size} bytes, is_dir={is_dir}\n"
            )
        return string_to_return

    except Exception as e:
        return f"    Error: {e}"


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
