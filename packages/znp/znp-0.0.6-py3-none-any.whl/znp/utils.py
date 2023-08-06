#!/usr/bin/env python3
import os
import magic
import pathlib


class NoFileOrDirectory(Exception):
    """
    Exception raised when user did not give a complete path
    to the current zathura file
    """

    def __init__(
        self,
        dir_path,
        file_path,
        message="ERROR: No directory or file found",
    ):
        self.file = file_path
        self.dir = dir_path
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}\nFile: "{self.file}"\nDir: "{self.dir}"'


def filter_file(test_file):
    """
    Returns true if file is not a known file type zathura
    """
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(test_file)
    accepted_types = [
        "image/vnd.djvu",
        "application/epub+zip",
        "application/postscript",
        "application/zip",
        "application/pdf",
    ]
    if file_type in accepted_types:
        return False

    return True


def get_next_or_prev_file(current_file_path, next_file=False, prev_file=False):
    """
    Get the next file in a directory when given a file path
    """
    # Split the path into directory and file
    temp = os.path.split(current_file_path)
    directory = temp[0]
    current_file = temp[1]
    # Check that both directory and file are not empty
    if not directory or not current_file:
        # If they are empty raise an error and exit with status 1
        raise NoFileOrDirectory(dir_path=directory, file_path=current_file)

    # Get a (sorted) list of files from the given directory
    file_list = os.listdir(directory)
    file_list.sort()

    # Populate vars
    new_index = 0
    incrementor = 0
    range_limit = 0
    reset_val = 0

    # Set vars depending on next or prev
    if next_file:
        incrementor = 1
        range_limit = len(file_list)
        reset_val = 0
    elif prev_file:
        incrementor = -1
        range_limit = -1
        reset_val = len(file_list) - 1

    # Add one to the given files index to get the next file
    if current_file in file_list:
        new_index = file_list.index(current_file) + incrementor

    # Check if we are out of bounds
    if next_file and new_index >= len(file_list):
        new_index = reset_val
    elif prev_file and new_index < 0:
        new_index = reset_val

    next_or_prev_file = os.path.join(directory, file_list[new_index])

    # Test if next_or_prev_file is valid file
    for i in range(new_index, range_limit, incrementor):
        next_or_prev_file = os.path.join(directory, file_list[i])
        if os.path.isfile(next_or_prev_file) and not filter_file(next_or_prev_file):
            return next_or_prev_file

    # File was not found so we start from the beginning / end
    new_index = reset_val
    for i in range(new_index, range_limit, incrementor):
        next_or_prev_file = os.path.join(directory, file_list[i])
        if os.path.isfile(next_or_prev_file) and not filter_file(next_or_prev_file):
            return next_or_prev_file

    # If the current file is the only compatible file then return None
    return None


def write_pid_file(pid_file, current_file):
    with open(pid_file, "w") as pf:
        pf.write(current_file)
    return 0
