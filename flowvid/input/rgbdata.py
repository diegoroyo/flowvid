import imageio
import numpy as np
from flowvid.input.fileinput import FileInput


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


class RGBData(FileInput):

    @classmethod
    def from_file(cls, file_name):
        return cls(file_name, 'file')

    @classmethod
    def from_directory(cls, dir_name, first=0, num_files=None):
        return cls(dir_name, 'dir', ('.png', '.jpg', '.bmp'), first, num_files)

    def __iter__(self):
        return RGBDataIterator(self)
