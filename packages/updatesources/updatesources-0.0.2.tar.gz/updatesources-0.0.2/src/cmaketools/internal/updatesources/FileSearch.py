import os


_search_modifier_delimiter = ","


def run(search_path: str, modifiers: list[str]):
    # print(f"FileSearch.run()")

    if _search_modifier_delimiter not in search_path:
        # modifiers = ["**.cpp", "**.h"]
        return _find_files(search_path, modifiers)

    else:
        # modifiers = search_path.split(_search_modifier_delimiter)
        return _find_files(search_path, modifiers)


def _find_files(search_path: str, modifiers: list[str]):
    files = []

    # print(f"modifiers = {modifiers}")

    for modifier in modifiers:
        file_extension = modifier.replace("*", "")
        if modifier.count('*') == 1:
            files += _walk_tree(search_path, file_extension, False)
        elif modifier.count('*') == 2:
            files += _walk_tree(search_path, file_extension, True)

    return files


def _walk_tree(search_path, file_extension, recursive):
    file_list = []
    for root, subdirs, files in os.walk(search_path):
        if files:
            file_list += [os.path.join(search_path, root, file) for file in files if file.endswith(file_extension)]

        if not recursive:
            break

    return file_list
