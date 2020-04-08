import matplotlib.pyplot as plt
import numpy as np
import imageio
import io
from ..core.filterable import Filterable


class VideoOutput:
    """ Save as video file """

    def __init__(self, filename, framerate):
        self._fig = plt.figure()  # used for Axes to rgb conversion
        self._video = imageio.get_writer(filename, fps=framerate)

    def __del__(self):
        if self._video is not None:
            self._video.close()

    def add_frame(self, image):
        """
            Add one image to the video
            :param image: [h, w, 3] rgb ndarray OR matplotlib axes (figure)
        """
        if isinstance(image, plt.Axes):
            # generate image data from Axes to pass to video
            buffer = io.BytesIO()  # save to temporal buffer
            self._fig.add_axes(image)
            self._fig.savefig(buffer, format='png')
            buffer.seek(0)  # back to the start of the buffer
            self._video.append_data(imageio.imread(buffer))
            self._fig.delaxes(image)
        elif isinstance(image, np.ndarray) and image.ndim == 3 and image.shape[2] == 3:
            self._video.append_data(image)
        else:
            raise AssertionError(
                'Image should be a [h, w, 3] rgb ndarray OR matplotlib axes (figure)')

    def add_all(self, images, verbose=False):
        """
            Add all frames of images to the video
            :param images: List of rgb OR figure data
            :param verbose: Show progress bar
        """
        if not isinstance(images, Filterable):
            raise AssertionError('images should contain a list of rgb data')
        images.assert_type('rgb', 'figure')

        n = len(images)
        for i, image in enumerate(images):
            if verbose:
                print(' Frame', i + 1, 'of', n, end='\r')  # TODO prettify
            self.add_frame(image)
