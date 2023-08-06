from .internal.updatesources import Project
from .internal.updatesources import Line
from .internal.updatesources import FileSearch
from .internal.updatesources import FileGenerator
from .internal.updatesources import PathResolver
from .internal.updatesources import HelpFormatter
from typing import List
import argparse
import sys
import os


_version = "0.1.0"

_default_input_file_name = ".sources"
_default_output_file_name = "sources.cmake"


def _setup_parser():
    parser = argparse.ArgumentParser(
        formatter_class=HelpFormatter,
        description=f'''
Reads a {_default_input_file_name} file to generate a {_default_output_file_name} file which populates CMake
variables with a list source files which can be used within a CMakeLists.txt file
''',
        epilog=f'''
Additional Information:
  Sample {_default_input_file_name} file format:

    PROJECT=CMAKE_VARIABLE_NAME
    ./myDirectory/CPPNonRecursiveFileSearch,*.cpp
    ./myDirectory/CPPRecursiveFileSearch,**.cpp
    ./myDirectory/CPPAndHeaderNonRecursiveFileSearch,*.cpp,*.h
    ./myDirectory/CPPAndHeaderRecursiveFileSearch,**.cpp,**.h OR ./myDirectory/CPPAndHeaderRecursiveFileSearch
    ./myDirectory/myCPPFile.cpp
    ./myDirectory/myHFile.h
    -./myDirectory/CPPNonRecursive/CPPIgnoredSubfolder,*.cpp
    -./myDirectory/ignoredHFile.h
    
  Note: Multiple projects can be defined within a single {_default_input_file_name} file 
''')

    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s v{_version}")
    parser.add_argument("path", nargs='?', default=".",
                        help=f"[Optional] Path to the directory that contains the {_default_input_file_name} file")
    parser.add_argument("-i", "--input", default=_default_input_file_name,
                        help=f"Specify the name of the input file")
    parser.add_argument("-o", "--output", default=_default_output_file_name,
                        help=f"Specify the name of the generated output file)")

    return parser


def _read_input_file(input_path, filename):
    input_file_path = os.path.join(input_path, filename)

    if not os.path.isfile(input_file_path):
        raise FileNotFoundError(filename + ' file not found in ' + str(input_path))

    with open(input_file_path, 'rt') as input_file:
        return input_file.readlines()


def _interpret_input_file(file_contents: List[str], search_root):
    projects = []

    project = Project()

    for line_string in file_contents:
        line_string = line_string.strip()
        line = Line(line_string)

        if line.is_project_header:
            if not project.is_empty:
                projects.append(project)
                project = Project()

            project.name = line.get_project_name()

        elif line.is_commented or line.is_empty:
            pass

        else:
            operation, path, modifiers = line.get_path_and_operation(search_root)

            if path.is_file():
                file_path = str(path)
                relative_path = os.path.relpath(file_path, search_root)
                relative_path = relative_path.replace("\\", "/")

                project.add_file(relative_path, operation)

            elif path.is_dir():
                directory_path = str(path)
                file_list = FileSearch.run(directory_path, modifiers)

                relative_paths = [os.path.relpath(file_path, search_root) for file_path in file_list]
                relative_paths = [file_path.replace("\\", "/") for file_path in relative_paths]

                project.add_files(relative_paths, operation)

            else:
                print('Ignoring path "' + str(path) + '"')

    projects.append(project)

    return projects


def update_sources(args):
    try:
        input_path = PathResolver.resolve(args.path)
        file_contents = _read_input_file(input_path, args.input)

        search_root = input_path
        projects = _interpret_input_file(file_contents, search_root)

        output_path = input_path
        FileGenerator.run(projects, output_path, args.output)

    except FileNotFoundError as err:
        print("ERROR: {0}".format(err))


def main(args=None):
    parser = _setup_parser()

    if not args:
        args = sys.argv[1:]

    parsed = parser.parse_args(args)

    print(f"Generating {parsed.output} from {parsed.input}")
    update_sources(parsed)


if __name__ == "__main__":
    main()
