import numpy as np
import imageio


class VideoOutput:
    def __init__(self, filename, framerate):
        self._video = imageio.get_writer(filename, fps=framerate)

    def __del__(self):
        if self._video is not None:
            self._video.close()

    def add_frame(self, image):
        self._video.append_data(image)

    def add_all(self, images, verbose=False):
        n = len(images)
        for i, image in enumerate(images):
            print(' Frame', i + 1, 'of', n, end='\r') # TODO prettify
            self.add_frame(image)
