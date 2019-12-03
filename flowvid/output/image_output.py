import numpy as np
import os
from PIL import Image
from ..core.filterable import Filterable


class ImageOutput:
    """ Save as image sequence """

    def __init__(self, path, name_format, first_id):
        if not os.path.isdir(path):
            raise AssertionError('{p} is not a directory.'.format(p=path))
        self._path = path
        self._id_template = name_format
        self._next_id = first_id

    def save_image(self, image):
        """
            Save one image with the next ID filename
            :param image: [h, w, 3] rgb ndarray
        """
        if not isinstance(image, np.ndarray) or image.ndim != 3 or image.shape[2] != 3:
            raise AssertionError('Image should be a [h, w, 3] rgb ndarray')

        image = Image.fromarray(image, 'RGB')
        filename = os.path.join(
            self._path, self._id_template.format(self._next_id))
        image.save(filename)
        self._next_id = self._next_id + 1

    def save_all(self, images, verbose=False):
        """
            Save all frames of images
            :param images: List of rgb data
            :param verbose: Show progress bar
        """
        if not isinstance(images, Filterable):
            raise AssertionError('images should contain a list of rgb data')
        images.assert_type('rgb')

        n = len(images)
        for i, image in enumerate(images):
            if verbose:
                print(' Frame', i + 1, 'of', n, end='\r')  # TODO prettify
            self.save_image(image)
