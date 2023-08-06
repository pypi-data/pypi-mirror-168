import os
import pathlib


def resolve(target_directory, item):
    if not os.path.isabs(target_directory):
        working_directory = os.getcwd()
        path = os.path.join(working_directory, target_directory, item)
    else:
        path = os.path.join(target_directory, item)

    path1 = pathlib.Path(path).resolve()
    return str(path1)
