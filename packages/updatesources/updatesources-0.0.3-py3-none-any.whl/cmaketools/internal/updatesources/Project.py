from typing import List


class Project:
    def __init__(self):
        self.name = ""
        self._files = []
        self._ignored_files = []

    @property
    def files(self):
        files = []
        for path in self._files:
            if path not in self._ignored_files:
                files.append(path)

        files.sort()
        return list(files)

    @property
    def is_empty(self):
        return len(self._files) == 0

    def add_file(self, file_path: str, operation: str):
        if operation == "add":
            self._files.append(file_path)
        elif operation == "ignore":
            self._ignored_files.append(file_path)
        else:
            raise NotImplementedError(operation + ' operation is not supported')

    def add_files(self, file_paths: List[str], operation: str):
        if operation == "add":
            self._files += file_paths
        elif operation == "ignore":
            self._ignored_files += file_paths
        else:
            raise NotImplementedError(operation + ' operation is not supported')
