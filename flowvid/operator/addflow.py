import numpy as np
from flowvid.operator.baseoperator import Operator

class AddFlow(Operator):
    def __init__(self, size):
        self._size = size
        self._remainder = np.zeros(list(size) + [3], dtype=np.float32)

    def apply(self, image, flow):
        [h, w] = image.shape[0:2]
        # TODO comprobar dimensiones

        image2 = np.zeros(list(self._size) + [3], dtype=np.uint8)
        remainder2 = np.zeros(list(self._size) + [2], dtype=np.float32)
        for y in range(h):
            for x in range(w):
                fx = flow[y, x, 0] + self._remainder[y, x, 0]
                fy = flow[y, x, 1] + self._remainder[y, x, 1]
                rx = int(round(fx))
                ry = int(round(fy))
                nx = x + rx
                ny = x + ry
                if nx >= 0 and nx < w and ny >= 0 and ny < h:
                    image2[ny, nx, :] += image[y, x, :]
                    remainder2[ny, nx, :] += [fx - rx, fy - ry]

        self._remainder = remainder2
        return image2