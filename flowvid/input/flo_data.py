import os
import re
import numpy as np
from ..core.filterable import Filterable
from .file_input import FileInput


TAG_FLOAT = 202021.25


def _read_flow(file_path):
    """
        :param file_path: File path of flo file
        :returns: [h, w, 2] ndarray where
                    [:, :, 0] = u (horizontal flow in pixels)
                    [:, :, 1] = v (vertical flow in pixels)
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
    """ Flow data (.flo) reader """

    def get_type(self):
        return 'flo'

    def _getitem(self, index):
        if index < 0 or index >= len(self):
            raise IndexError('Index out of range')
        return _read_flow(self.source[index])
