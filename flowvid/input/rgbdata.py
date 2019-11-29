import os
import re
import imageio
import numpy as np


class RGBDataIterator:
    def __init__(self, flodata):
        self._iter = iter(flodata.source)

    def __next__(self):
        file_name = next(self._iter)
        return self.__read_image(file_name)

    @classmethod
    def __read_image(self, file_path):
        """
            TODO
        """
        return imageio.imread(file_path)


# TODO hacer que acepte mas que PNG
class RGBData:

    def __init__(self, source, first=None, num_files=None):
        # .flo file source
        if os.path.isfile(source):
            self.source = [source]
        elif os.path.isdir(source):
            self.source = (self.__list_directory(source, first, num_files))
        else:
            raise AssertionError('Source does not exist')

    @classmethod
    def from_file(cls, file_name):
        return cls(file_name)

    @classmethod
    def from_directory(cls, dir_name, first=0, num_files=None):
        return cls(dir_name, first, num_files)

    def __iter__(self):
        return RGBDataIterator(self)

    @classmethod
    def __list_directory(self, directory, first, num_files):
        pattern = re.compile(r'\d+')
        name_list = [f for f in os.listdir(directory) if f.endswith('.png')]
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
