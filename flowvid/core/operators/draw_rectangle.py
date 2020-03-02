import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from ..util.convert_to_axes import convert_to_axes
from ..filterable import Filterable
from .base_operator import Operator


class DrawRectangle(Operator):
    """
        Given a list of images and rectangles, draw each rectangle in each
        of the images from the image list
    """

    def __init__(self, image_data, rect_data, color, figure_output):
        if not isinstance(image_data, Filterable):
            raise AssertionError(
                'image_data should contain a list of rgb data')
        if not isinstance(rect_data, Filterable):
            raise AssertionError(
                'rect_data should contain a list of rectangle points data')
        if not isinstance(color, list) or len(color) != 3:
            raise AssertionError(
                'color should be a [r, g, b] list where rgb range from 0 to 255')
        image_data.assert_type('rgb', 'figure')
        if image_data.get_type() == 'figure' and not figure_output:
            raise AssertionError(
                'Cannot convert a figure filterable to rgb. Maybe you need to enable the figure_output option.')
        rect_data.assert_type('rect')
        Operator.__init__(self)
        self._image_data = image_data
        self._rect_data = rect_data
        if figure_output:
            self._color = (color[0] / 255, color[1] / 255, color[2] / 255, 1.0)
        else:
            self._color = color
        self._figure_output = figure_output

    def _items(self):
        return (self._draw(image, rect) for image, rect in zip(self._image_data, self._rect_data))

    def __len__(self):
        return min(len(self._image_data), len(self._rect_data))

    def get_type(self):
        if self._figure_output:
            return 'figure'
        else:
            return 'rgb'

    def _draw(self, image, rect):
        """
            :param image: [h, w, 3] rgb data
            :param rect: [4] ndarray (x0 y0 x1 y1)
            :returns: image with modified RGB such that rect is drawn with self._color
        """
        if self._figure_output:
            ax = convert_to_axes(image)

            # Get rectangle data & draw
            [x0, y0, x1, y1] = rect
            xw = x1 - x0
            yw = y1 - y0
            rect = patches.Rectangle(
                (x0, y0), xw, yw, linewidth=1, edgecolor=self._color, facecolor='none')

            # Add the patch to the Axes
            ax.add_patch(rect)
            return ax
        else:
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
