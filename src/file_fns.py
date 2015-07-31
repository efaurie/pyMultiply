import os


def is_file_or_directory(file_path):
    if os.path.isfile(file_path):
        return True
    elif os.path.isdir(file_path):
        return True

    return False


def get_file_list_from_source(file_path, max_depth):
    return get_file_list_with_depth(file_path, 0, max_depth)


def get_file_list_with_depth(file_path, current_depth, max_depth):
    if current_depth > max_depth:
        return []

    all_files = []

    if os.path.isfile(file_path):
        all_files.append(file_path)
    else:
        for (directory_path, directory_name, filenames) in os.walk(file_path):
            for filename in filenames:
                full_path = os.path.join(directory_path, filename)
                all_files.append(full_path)
            if current_depth+1 <= max_depth:
                for directory in directory_name:
                    all_files.extend(get_file_list_with_depth(directory, current_depth+1, max_depth))

    return all_files


def get_file_list_from_file(file_path):
    all_files = []

    text_file = open(file_path, 'r')
    for entry in text_file:
        entry = entry.strip()
        all_files.append(entry)

    return all_files
