import imageio
import numpy as np
from flowvid.input.fileinput import FileInput


def _read_image(file_path):
    """
        TODO
    """
    return imageio.imread(file_path)


class RGBData(FileInput):

    def _getitem(self, index):
        # TODO el index esta dentro de source
        return _read_image(self.source[index])
