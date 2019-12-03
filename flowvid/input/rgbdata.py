import imageio
import numpy as np
from flowvid.input.fileinput import FileInput


def _read_image(file_path):
    """
        :param file_path: File path of image file
        :returns: [h, w, 3] ndarray where
                    [y, x, :] = [r, g, b] components of pixel x, y
    """
    return imageio.imread(file_path)


class RGBData(FileInput):
    """ Image data (.png, etc.) reader, wrapper for imread """

    def get_type(self):
        return 'rgb'

    def _getitem(self, index):
        if index < 0 or index >= len(self):
            raise IndexError('Index out of range')
        return _read_image(self.source[index])
