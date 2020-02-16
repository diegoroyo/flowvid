import os
import re
import numpy as np
from ..core.filterable import Filterable
from .file_input import FileInput


class FloData(FileInput):
    """ Flow data (.flo) reader """

    def _items(self):
        return (FloData._read_flow(filename) for filename in self.source)

    def get_type(self):
        return 'flo'

    def __getitem__(self, index):
        if index < 0 or index >= len(self):
            raise IndexError('Index out of range')
        return FloData._read_flow(self.source[index])

    TAG_FLOAT = 202021.25

    @staticmethod
    def _read_flow(file_path):
        """
            :param file_path: File path of flo file
            :returns: [h, w, 2] ndarray where
                        [:, :, 0] = u (horizontal flow in pixels)
                        [:, :, 1] = v (vertical flow in pixels)
        """
        with open(file_path, 'rb') as file:
            tag = np.frombuffer(file.read(4), dtype=np.float32, count=1)[0]
            if not tag == FloData.TAG_FLOAT:
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
