import numpy as np
import random
from ..filterable import Filterable
from ..util.convert_to_axes import convert_to_axes
from ..util.image_draw import get_color, draw_points, draw_line
from .base_operator import Operator


class DrawPoints(Operator):
    """
        Given a list of images and points, draw each set of points in each
        of the images from the image list
    """

    def __init__(self, image_data, point_data, color, num_trail, figure_output):
        if not isinstance(image_data, Filterable):
            raise AssertionError(
                'image_data should contain a list of rgb data')
        if not isinstance(point_data, Filterable):
            raise AssertionError(
                'point_data should contain a list of points data')
        if (not isinstance(color, list) or len(color) != 3) and color != 'random':
            raise AssertionError(
                'color should be a [r, g, b] list where rgb range from 0 to 255, or \'random\' for random colors.')
        image_data.assert_type('rgb', 'figure')
        if image_data.get_type() == 'figure' and not figure_output:
            raise AssertionError(
                'Cannot convert a figure filterable to rgb. Maybe you need to enable the figure_output option.')
        point_data.assert_type('point')
        if num_trail <= 0:
            raise AssertionError(
                'num_trail should be bigger than 0 but it is {n}'.format(n=num_trail))
        Operator.__init__(self)
        self._image_data = image_data
        self._point_data = point_data
        if figure_output and color != 'random':
            self._color = (color[0] / 255, color[1] / 255, color[2] / 255, 1.0)
        else:
            self._color = color
        self._num_trail = num_trail
        self._figure_output = figure_output

    def _draw_line(self, canvas, i, p0, p1):
        if self._figure_output:
            color = get_color(self._color, i, normalize=True)
            canvas.plot((p0[0], p1[0]), (p0[1], p1[1]), color=color)
        else:
            color = get_color(self._color, i)
            line = np.reshape([p0, p1], (2, 2))
            draw_line(canvas, line, color)

    def _draw_points(self, canvas, points):
        if self._figure_output:
            colors = [get_color(self._color, i, normalize=True)
                      for i in range(len(points))]
            canvas.scatter(points[:, 0], points[:, 1],
                           marker='+', color=colors)
        else:
            draw_points(canvas, points, self._color, cross=True)

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

            if self._figure_output:
                canvas = convert_to_axes(image)
            else:
                canvas = image

            # draw all points with their trails
            last_points = None
            for curr_points in trail:
                if last_points is not None:
                    # Line between curr and last point
                    for i, (p0, p1) in enumerate(zip(last_points, curr_points)):
                        self._draw_line(canvas, i, p0, p1)
                last_points = curr_points

            self._draw_points(canvas, trail[-1])
            yield canvas

    def __len__(self):
        return min(len(self._image_data), len(self._point_data))

    def get_type(self):
        if self._figure_output:
            return 'figure'
        else:
            return 'rgb'
