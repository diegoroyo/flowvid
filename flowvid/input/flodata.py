import os
import re
import numpy as np
from flowvid.input.fileinput import FileInput


TAG_FLOAT = 202021.25


def _read_flow(file_path):
    """
        TODO
    """
    with open(file_path, 'rb') as file:
        tag = np.frombuffer(file.read(4), dtype=np.float32, count=1)[0]
        if not tag == TAG_FLOAT:
            raise AssertionError(
                'File {f} has wrong tag ({t})'.format(f=file_path, t=tag))

        [width, height] = np.frombuffer(
            file.read(8), dtype=np.int32, count=2)

        dimensions = 2  # u (horizontal) and v (vertical)
        items = width * height * dimensions

        # read flow values from file
        flow = np.frombuffer(file.read(4 * items),
                             dtype=np.float32, count=items)
        flow = np.resize(flow, (height, width, dimensions))

    return flow


class FloDataIterator:
    def __init__(self, flodata):
        self._iter = iter(flodata.source)

    def __next__(self):
        file_name = next(self._iter)
        return _read_flow(file_name)


class FloData(FileInput):

    @classmethod
    def from_file(cls, file_name):
        return cls(file_name, 'file')

    @classmethod
    def from_directory(cls, dir_name, first=0, num_files=None):
        return cls(dir_name, 'dir', '.flo', first, num_files)

    def __iter__(self):
        return FloDataIterator(self)

    def __getitem__(self, index):
        # TODO el index esta dentro de source
        return _read_flow(self.source[index])
