import numpy as np
import os
from PIL import Image


class ImageOutput:
    def __init__(self, path, name_format, first_id):
        self._path = path
        self._id_template = name_format
        self._next_id = first_id

    def save_image(self, data):
        image = Image.fromarray(data, 'RGB')
        filename = os.path.join(self._path, self._id_template.format(self._next_id))
        image.save(filename)
        self._next_id = self._next_id + 1
