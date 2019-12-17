import numpy as np
import random
from ..filterable import Filterable
from .base_operator import Operator


class DrawPointsIterator:
    """ Iterates through DrawPoints's point data to generate all the images """

    def __init__(self, obj):
        self._iter = iter(zip(obj._image_data, obj._point_data))
        self._obj = obj

    def __next__(self):
        (image, points) = next(self._iter)
        return self._obj._draw(image, points)


class DrawPoints(Operator):
    """
        Given a list of images and points, draw each set of points in each
        of the images from the image list
    """

    _random_colors = [[255, 0, 0], [128, 128, 0], [0, 255, 0],
                      [0, 128, 128], [0, 0, 255], [128, 0, 128]]

    def __init__(self, image_data, point_data, color):
        if not isinstance(image_data, Filterable):
            raise AssertionError(
                'image_data should contain a list of rgb data')
        if not isinstance(point_data, Filterable):
            raise AssertionError(
                'point_data should contain a list of points data')
        if (not isinstance(color, list) or len(color) != 3) and color != 'random':
            raise AssertionError(
                'color should be a [r, g, b] list where rgb range from 0 to 255, or \'random\' for random colors.')
        image_data.assert_type('rgb')
        point_data.assert_type('point')
        Operator.__init__(self)
        self._image_data = image_data
        self._point_data = point_data
        self._color = color

    def __len__(self):
        return len(self._point_data)

    def get_type(self):
        return 'rgb'

    def __iter__(self):
        return DrawPointsIterator(self)

    def _draw(self, image, points):
        """
            :param image: [h, w, 3] rgb data
            :param points: [n, 2] ndarray (x, y)
            :returns: image with modified RGB such that points are drawn with self._color
                      Note: if self_color == 'random', a different color is chosen for
                            each point (but each color is consistent between frames)
        """

        # Clamping
        [h, w] = image.shape[0:2]
        points = points.astype(int)
        points[:, 0] = np.clip(points[:, 0], 0, w - 1)
        points[:, 1] = np.clip(points[:, 1], 0, h - 1)

        # Drawing
        for i, [px, py] in enumerate(points):
            # Get color
            color = self._color
            if self._color == 'random':
                ind = i % len(DrawPoints._random_colors)
                color = DrawPoints._random_colors[ind]
            # Draw point as a small cross
            image[py, px, :] = color
            if px > 0:
                image[py, px - 1, :] = color
            if px < w - 1:
                image[py, px + 1, :] = color
            if py > 0:
                image[py - 1, px, :] = color
            if py < h - 1:
                image[py + 1, px, :] = color

        return image
