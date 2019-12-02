import numpy as np
from flowvid.fvcore.operators.baseoperator import Operator

class DrawRectangleIterator:
    def __init__(self, obj):
        self._iter = iter(zip(obj._image_data, obj._rect_data))
        self._obj = obj

    def __next__(self):
        (image, rect) = next(self._iter)
        return self._obj._draw(image, rect)

class DrawRectangle(Operator):
    def __init__(self, image_data, rect_data, color):
        Operator.__init__(self)
        self._image_data = image_data
        self._rect_data = rect_data
        self._color = color

    def __iter__(self):
        return DrawRectangleIterator(self)

    def __len__(self):
        return len(self._rect_data)

    def _draw(self, image, rect):
        #clamping
        [h, w] = image.shape[0:2]
        [x0, y0, x1, y1] = rect.astype(int)

        # TODO mejor clampeo
        if x0 > w - 1:
            x0 = w - 1
        if y0 > h - 1:
            y0 = h - 1
        if x1 > w - 1:
            x1 = w - 1
        if y1 > h - 1:
            y1 = h - 1
        
        #drawing
        for px in range(x0, x1):
            image[y0, px, :] = self._color
            image[y1, px, :] = self._color
        for py in range(y0, y1):
            image[py, x0, :] = self._color
            image[py, x1, :] = self._color

        return image
