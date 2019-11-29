import numpy as np
from flowvid.filter.basefilter import Filter

class DrawRectangle(Filter):
    def apply(self, data, color, x, y, wx, wy):
        #clamping
        [h, w] = data.shape[0:2]
        if x > w - 1:
            x = w - 1
        if y > h - 1:
            y = h - 1
        if x + wx > w - 1:
            wx = w - x
        if y + wy > h - 1:
            wy = h - y
        
        #drawing
        for px in range(x, x+wx):
            data[y, px, :] = color
            data[y+wy, px, :] = color
        for py in range(y, y+wy):
            data[py, x, :] = color
            data[py, x+wx, :] = color

        return data
