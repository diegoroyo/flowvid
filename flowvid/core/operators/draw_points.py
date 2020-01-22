import numpy as np
import random
from ..filterable import Filterable
from .base_operator import Operator


class DrawPointsIterator:
    """ Iterates through DrawPoints's point data to generate all the images """

    def __init__(self, obj):
        self._iter = iter(zip(obj._image_data, obj._point_data))
        self._obj = obj
        self._color = obj._color
        self._num_trail = obj._num_trail
        self._trail = np.array([])

    def __next__(self):
        (image, points) = next(self._iter)

        if self._trail.size == 0:
            self._trail = np.resize(points , (1, len(points), 2))
        elif self._trail.shape[0] < self._num_trail:
            self._trail = np.concatenate(
                (self._trail, np.resize(points, (1, len(points), 2))), axis=0)
        else:
            self._trail = np.roll(self._trail, -1, axis=0)
            self._trail[self._num_trail - 1, :] = points

        last_points = None
        for curr_points in self._trail:
            if last_points is not None:
                # Line between curr and last point
                for i, (p0, p1) in enumerate(zip(last_points, curr_points)):
                    color = self._color
                    if self._color == 'random':
                        ind = i % len(DrawPoints._random_colors)
                        color = DrawPoints._random_colors[ind]
                    line = np.reshape([p0, p1], (2, 2))
                    self._obj._draw_line(image, line, color)

            last_points = curr_points
        image = self._obj._draw_point(image, self._trail[-1], cross=True)
        return image


class DrawPoints(Operator):
    """
        Given a list of images and points, draw each set of points in each
        of the images from the image list
    """

    _random_colors = [[255, 255, 255], [0, 0, 255], [0, 255, 255], [255, 0, 0], [255, 255, 0], [200, 200, 200], [0, 0, 200], [0, 0, 150], [150, 150, 150], [150, 0, 0], [200, 0, 0], [0, 200, 200], [0, 150, 150]]
    # _random_colors = [[255, 0, 0], [128, 128, 0], [0, 255, 0],
    #                   [0, 128, 128], [0, 0, 255], [128, 0, 128]]

    def __init__(self, image_data, point_data, color, num_trail):
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
        if num_trail <= 0:
            raise AssertionError(
                'num_trail should be bigger than 0 but it is {n}'.format(n=num_trail))
        Operator.__init__(self)
        self._image_data = image_data
        self._point_data = point_data
        self._color = color
        self._num_trail = num_trail

    def __len__(self):
        return len(self._point_data)

    def get_type(self):
        return 'rgb'

    def __iter__(self):
        return DrawPointsIterator(self)

    def _draw_point(self, image, points, cross=False):
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
            if cross:
                if px > 0:
                    image[py, px - 1, :] = color
                if px < w - 1:
                    image[py, px + 1, :] = color
                if py > 0:
                    image[py - 1, px, :] = color
                if py < h - 1:
                    image[py + 1, px, :] = color

        return image

    def _draw_line(self, image, line, color):
        """
            :param image: [h, w, 3] rgb data
            :param line: [2, 2] ndarray ((p0x, p0y), (p1x, p1y)) line between p0-p1
            :param color: [r, g, b] color of the line
            :returns: image with modified RGB such that line is drawn on it
                      Note: if self_color == 'random', a different color is chosen for
                            each line (but each color is consistent between frames)
        """

        # Clamping
        [h, w] = image.shape[0:2]
        line = line.astype(int)
        line[:, 0] = np.clip(line[:, 0], 0, w - 1)
        line[:, 1] = np.clip(line[:, 1], 0, h - 1)
        p0 = line[0, :]
        p1 = line[1, :]
        # Simple line algorithm
        # TODO prettify / change to a cleaner module?
        if abs(p1[0] - p0[0]) > abs(p1[1] - p0[1]):
            # X axis is bigger, iterate through it
            if p0[0] > p1[0]:
                p0, p1 = p1, p0
            for lx in range(p0[0], p1[0]):
                y = int(p0[1] + (lx - p0[0]) * (p1[1] - p0[1]) / (p1[0] - p0[0]))
                image[y, lx, :] = color
        else:
            # Y axis is bigger, iterate through it
            if p0[1] > p1[1]:
                p0, p1 = p1, p0
            for ly in range(p0[1], p1[1]):
                x = int(p0[0] + (ly - p0[1]) * (p1[0] - p0[0]) / (p1[1] - p0[1]))
                image[ly, x, :] = color
        
