from .Project import Project
import os


def run(projects: list[Project], target_directory: str, filename: str):
    file_path = os.path.join(target_directory, filename)
    with open(file_path, "w", newline="\n") as cmake_file:
        for project in projects:
            _write_project(project, cmake_file)


def _write_project(project: Project, cmake_file):
    if project.name == "":
        return

    cmake_file.write('set(' + project.name + '\n')
    for file_path in project.files:
        cmake_file.write('\t' + file_path + '\n')
    cmake_file.write(')\n\n')
