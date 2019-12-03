import numpy as np
import imageio
from ..core.filterable import Filterable


class VideoOutput:
    """ Save as video file """

    def __init__(self, filename, framerate):
        self._video = imageio.get_writer(filename, fps=framerate)

    def __del__(self):
        if self._video is not None:
            self._video.close()

    def add_frame(self, image):
        """
            Add one image to the video
            :param image: [h, w, 3] rgb ndarray
        """
        if not isinstance(image, np.ndarray) or image.ndim != 3 or image.shape[2] != 3:
            raise AssertionError('Image should be a [h, w, 3] rgb ndarray')
        
        self._video.append_data(image)

    def add_all(self, images, verbose=False):
        """
            Add all frames of images to the video
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
            self.add_frame(image)
