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
