import os


def get_dir_files(path):
    files = []
    dirs = []
    for dir_path, dir_names, file_names in os.walk(path):
        for dir_name in dir_names:
            dirs.append(os.path.join(dir_path, dir_name))
        for file_name in file_names:
            files.append(os.path.join(dir_path, file_name))
    return dirs, files
