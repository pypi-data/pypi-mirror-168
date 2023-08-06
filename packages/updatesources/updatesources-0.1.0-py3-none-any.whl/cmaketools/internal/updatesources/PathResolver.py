import os
import pathlib


def resolve(target_directory):
    if not os.path.isabs(target_directory):
        working_directory = os.getcwd()
        path = os.path.join(working_directory, target_directory)
    else:
        path = target_directory

    path1 = pathlib.Path(path).resolve()
    return str(path1)


def make_relative(file_path: str, start_path: str):
    relative_path = os.path.relpath(file_path, start_path)
    relative_path = relative_path.replace("\\", "/")

    if relative_path.startswith("../"):
        pass
    elif relative_path.startswith("./"):
        pass
    else:
        relative_path = f"./{relative_path}"

    return relative_path
