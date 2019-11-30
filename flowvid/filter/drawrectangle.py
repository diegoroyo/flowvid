import numpy as np
from flowvid.filter.basefilter import Filter

class DrawRectangle(Filter):
    def apply(self, img, rec, color):
        #clamping
        [h, w] = img.shape[0:2]
        [x0, y0, x1, y1] = rec.astype(int)

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
            img[y0, px, :] = color
            img[y1, px, :] = color
        for py in range(y0, y1):
            img[py, x0, :] = color
            img[py, x1, :] = color

        return img
