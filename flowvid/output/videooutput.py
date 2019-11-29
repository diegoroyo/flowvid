import numpy as np
import imageio
from PIL import Image


class VideoOutput:
    def __init__(self, filename, framerate):
        self._video = imageio.get_writer(filename, fps=framerate)

    def add_frame(self, frame):
        image = Image.fromarray(frame, 'RGB')
        image.save('prueba.png')
        # self._video.append_data(data)

    def close(self):
        self._video.close()
