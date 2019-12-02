import imageio
import numpy as np
from flowvid.input.fileinput import FileInput


def _read_image(file_path):
    """
        TODO
    """
    return imageio.imread(file_path)


class RGBDataIterator:
    def __init__(self, flodata):
        self._iter = iter(flodata.source)

    def __next__(self):
        file_name = next(self._iter)
        return _read_image(file_name)


class RGBData(FileInput):

    @classmethod
    def from_file(cls, file_name):
        return cls(file_name, 'file')

    @classmethod
    def from_directory(cls, dir_name, first=0, num_files=None):
        return cls(dir_name, 'dir', ('.png', '.jpg', '.bmp'), first, num_files)

    def __iter__(self):
        return RGBDataIterator(self)

    def __getitem__(self, index):
        # TODO el index esta dentro de source
        return _read_image(self.source[index])
