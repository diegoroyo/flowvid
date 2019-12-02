import os
import re
import numpy as np
from flowvid.fvinput.fileinput import FileInput


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


class FloData(FileInput):

    def _getitem(self, index):
        # TODO el index esta dentro de source
        return _read_flow(self.source[index])
