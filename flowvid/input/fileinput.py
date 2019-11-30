import os
import re
import numpy as np

class FileInput:
    def __init__(self, source, input_type, extensions=None, first=None, num_files=None):
        if input_type == 'file' and os.path.isfile(source):
            self.source = [source]
        elif input_type == 'dir' and os.path.isdir(source):
            self.source = (self.__list_directory(source, extensions, first, num_files))
        else:
            raise AssertionError('Source does not exist')

    @classmethod
    def __list_directory(self, directory, extensions, first, num_files):
        pattern = re.compile(r'\d+')
        name_list = [f for f in os.listdir(directory) if (extensions is None or f.endswith(extensions))]
        file_list = []  # (index, name) tuples

        if not name_list:
            raise AssertionError(
                'There are no .png files in directory {d}'.format(d=directory))

        for name in name_list:
            match = pattern.match(name)
            if match is not None:
                file_index = match[0]
                file_path = os.path.join(directory, name)
                file_list.append((file_index, file_path))
        file_list = sorted(file_list, key=lambda tuple: tuple[0])

        if num_files is None:
            num_files = len(file_list) - first
            
        file_names = [file_tuple[1] for file_tuple in file_list]
        return file_names[first:first+num_files]