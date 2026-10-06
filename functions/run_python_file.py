import os, subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abs_path: str = os.path.abspath(working_directory)
        target_path: str = os.path.normpath(os.path.join(abs_path, file_path))
        valid_target_dir: bool = os.path.commonpath([abs_path, target_path]) == abs_path

        if valid_target_dir is False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_path]
        if args is not None:
            command.extend(args)

        obj_after_run = subprocess.run(
            command,
            cwd=abs_path,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output = []

        if obj_after_run.returncode != 0:
            output.append(f"Process exited with code {obj_after_run.returncode}")
        if not obj_after_run.stdout and not obj_after_run.stderr:
            output.append("No output produced")
        if obj_after_run.stdout:
            output.append(f"STDOUT:\n{obj_after_run.stdout}")
        if obj_after_run.stderr:
            output.append(f"STDERR:\n{obj_after_run.stderr}")
        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Run a python file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the file we want to run.",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "A list of arguments that we can write in command line when we run the file.",
                },
            },
            "required": ["file_path"],
        },
    },
}
