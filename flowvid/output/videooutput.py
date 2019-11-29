import numpy as np
import imageio
from PIL import Image


class VideoOutput:
    def __init__(self, filename, framerate):
        self._video = imageio.get_writer(filename, fps=framerate)

    def __del__(self):
        if self._video is not None:
            self._video.close()

    def add_frame(self, data):
        # image = Image.fromarray(data, 'RGB')
        # image.save('prueba.png')
        self._video.append_data(data)
