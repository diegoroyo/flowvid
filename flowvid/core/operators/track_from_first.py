import numpy as np
import copy
from ..filterable import Filterable
from ..util.image_draw import get_color, draw_points, draw_line
from .base_operator import Operator


class TrackFromFirst(Operator):
    """
        Given a set of points and image data, track the set of points
        to see if they track the image's features correctly
    """

    def __init__(self, point_data, image_data, color, draw_lines, vertical, svg):
        if not isinstance(point_data, Filterable):
            raise AssertionError(
                'point_data should contain a list of point data')
        if not isinstance(image_data, Filterable):
            raise AssertionError(
                'image_data should contain a list of image data')
        point_data.assert_type('point')
        image_data.assert_type('rgb')
        Operator.__init__(self)
        self._point_data = point_data
        self._image_data = image_data
        self._color = color
        self._draw_lines = draw_lines
        self._vertical = vertical
        self._svg = svg

    def _items(self):
        first_point = copy.copy(next(iter(self._point_data)))
        first_image = next(iter(self._image_data))
        height, width = first_image.shape[0:2]
        for curr_point, image in zip(self._point_data, self._image_data):
            axis = 1  # cols
            if self._vertical:
                axis = 0  # rows
                curr_point = curr_point + np.array([0, height])
            else:
                curr_point = curr_point + np.array([width, 0])
            concat_image = np.concatenate((first_image, image), axis=axis)
            draw_points(concat_image, first_point, self._color, cross=True)
            draw_points(concat_image, curr_point, self._color, cross=True)
            if self._draw_lines:
                for i, (p0, p1) in enumerate(zip(first_point, curr_point)):
                    color = get_color(self._color, i)
                    draw_line(concat_image, np.reshape(
                        (p0, p1), (2, 2)), color)
            yield concat_image

    def __len__(self):
        return min(len(self._point_data), len(self._image_data))

    def get_type(self):
        if self._svg:
            return 'svg'
        else:
            return 'rgb'
