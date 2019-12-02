import os
import re
import numpy as np
from flowvid.fvcore.filterable import Filterable


class FileInput(Filterable):
    def __init__(self, source, extensions=None, dir_first=None, dir_total=None):
        Filterable.__init__(self)
        if os.path.isfile(source) and (extensions is None or source.endswith(extensions)):
            self.source = [source]
        elif os.path.isdir(source):
            self.source = (FileInput.__list_directory(
                source, extensions, dir_first, dir_total))
        else:
            raise AssertionError('Source does not exist')

    def __len__(self):
        return len(self.source)

    @staticmethod
    def __list_directory(directory, extensions, dir_first, dir_total):
        pattern = re.compile(r'\d+')
        name_list = [f for f in os.listdir(directory) if (
            extensions is None or f.endswith(extensions))]
        file_list = []  # (index, name) tuples

        if not name_list:
            raise AssertionError(
                'There are no {f} files in directory {d}'.format(f=extensions, d=directory))

        for name in name_list:
            match = pattern.match(name)
            if match is not None:
                file_index = match[0]
                file_path = os.path.join(directory, name)
                file_list.append((file_index, file_path))
        file_list = sorted(file_list, key=lambda tuple: tuple[0])

        if dir_total is None:
            dir_total = len(file_list) - dir_first

        file_names = [file_tuple[1] for file_tuple in file_list]
        return file_names[dir_first:dir_first+dir_total]
