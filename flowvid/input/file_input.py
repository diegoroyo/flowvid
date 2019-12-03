import os
import re
import numpy as np
from ..core.filterable import Filterable


class FileInput(Filterable):
    """
        Utility to read files and directories with required extensions
        Only returns filenames, file processing should be done in a subclass
    """

    def __init__(self, source, extensions=None, dir_first=None, dir_total=None):
        Filterable.__init__(self)
        if os.path.isfile(source) and (extensions is None or source.endswith(extensions)):
            self.source = [source]
        elif os.path.isdir(source):
            self.source = (FileInput.__list_directory(
                source, extensions, dir_first, dir_total))
        else:
            raise AssertionError('Source ({s}) does not exist{extra}'.format(
                s=source, extra='' if extensions is None else ' or doesn\'t contain files with extension {e}'.format(e=extensions)))

    def __len__(self):
        return len(self.source)

    @staticmethod
    def __list_directory(directory, extensions, dir_first, dir_total):
        """
            List all files in directory
            :param directory: Directory to be checked
            :param extensions: Filter file extensions from that type
                               If None, don't filter extensions
            :param dir_first: Get elements from that index
                              (dir[dir_first:])
            :param dir_total: Number of elements to retrieve (from dir_first)
                              (dir[dir_first:dir_first+dir_total])
                              If None, get all elements from the first one
            :returns: List of filenames (strings)
        """
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
