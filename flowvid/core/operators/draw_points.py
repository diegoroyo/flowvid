import numpy as np
import random
from ..filterable import Filterable
from ..util.image_draw import draw_line
from .base_operator import Operator


class DrawPoints(Operator):
    """
        Given a list of images and points, draw each set of points in each
        of the images from the image list
    """

    _random_colors = [[255, 255, 255], [0, 0, 255], [0, 255, 255], [255, 0, 0],
                      [255, 255, 0], [200, 200, 200], [0, 0, 200], [0, 0, 150],
                      [150, 150, 150], [150, 0, 0], [200, 0, 0], [0, 200, 200]]
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

    def _items(self):
        trail = np.array([])
        for image, points in zip(self._image_data, self._point_data):
            # update trail (last points) array
            if trail.size == 0:
                trail = np.resize(points, (1, len(points), 2))
            elif trail.shape[0] < self._num_trail:
                trail = np.concatenate(
                    (trail, np.resize(points, (1, len(points), 2))), axis=0)
            else:
                trail = np.roll(trail, -1, axis=0)
                trail[self._num_trail - 1, :] = points

            # draw all points with their trails
            last_points = None
            for curr_points in trail:
                if last_points is not None:
                    # Line between curr and last point
                    for i, (p0, p1) in enumerate(zip(last_points, curr_points)):
                        color = self._color
                        if self._color == 'random':
                            ind = i % len(DrawPoints._random_colors)
                            color = DrawPoints._random_colors[ind]
                        line = np.reshape([p0, p1], (2, 2))
                        draw_line(image, line, color)

                last_points = curr_points
            image = self._draw_point(image, trail[-1], cross=True)
            yield image

    def __len__(self):
        return min(len(self._image_data), len(self._point_data))

    def get_type(self):
        return 'rgb'

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
        points[:, 0] = np.clip(points[:, 0], 1, w - 2)
        points[:, 1] = np.clip(points[:, 1], 1, h - 2)

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
                # no need to check for bounds
                image[py, px - 1, :] = color
                image[py, px + 1, :] = color
                image[py - 1, px, :] = color
                image[py + 1, px, :] = color

        return image
