import numpy as np
from ..filterable import Filterable
from .base_operator import Operator


class DrawRectangleIterator:
    """ Iterates through DrawRectangle's flow data to generate all the images """

    def __init__(self, obj):
        self._iter = iter(zip(obj._image_data, obj._rect_data))
        self._obj = obj

    def __next__(self):
        (image, rect) = next(self._iter)
        return self._obj._draw(image, rect)


class DrawRectangle(Operator):
    """
        Given a list of images and rectangles, draw each rectangle in each
        of the images from the image list
    """

    def __init__(self, image_data, rect_data, color):
        if not isinstance(image_data, Filterable):
            raise AssertionError(
                'image_data should contain a list of rgb data')
        if not isinstance(rect_data, Filterable):
            raise AssertionError(
                'rect_data should contain a list of rectangle points data')
        if not isinstance(color, list) or len(color) != 3:
            raise AssertionError(
                'color should be a [r, g, b] list where rgb range from 0 to 255')
        image_data.assert_type('rgb')
        rect_data.assert_type('rect')
        Operator.__init__(self)
        self._image_data = image_data
        self._rect_data = rect_data
        self._color = color

    def __len__(self):
        return len(self._rect_data)

    def get_type(self):
        return 'rgb'
        
    def __iter__(self):
        return DrawRectangleIterator(self)

    def _draw(self, image, rect):
        """
            :param image: [h, w, 3] rgb data
            :param rect: [4] ndarray (x0 y0 x1 y1)
            :returns: image with modified RGB such that rect is drawn with self._color
        """

        # Clamping
        [h, w] = image.shape[0:2]
        [x0, y0, x1, y1] = rect.astype(int)

        x0 = np.clip(x0, 0, w - 1)
        y0 = np.clip(y0, 0, h - 1)
        x1 = np.clip(x1, 0, w - 1)
        y1 = np.clip(y1, 0, h - 1)

        # Drawing
        for px in range(x0, x1):
            image[y0, px, :] = self._color
            image[y1, px, :] = self._color
        for py in range(y0, y1):
            image[py, x0, :] = self._color
            image[py, x1, :] = self._color

        return image
