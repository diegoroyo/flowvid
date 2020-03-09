import numpy as np
from ..filterable import Filterable
from .base_operator import Operator


class SynthesizeImage(Operator):
    """
        Given an initial image and accumulated flow, generate synthesized
        images moving the pixels according to the flow
    """

    def __init__(self, image, accum_flow_data):
        if not isinstance(image, np.ndarray):
            raise AssertionError('image should be a [h, w, 3] ndarray')
        if image.ndim != 3 or image.shape[2] != 3:
            raise AssertionError(
                'image should be a [h, w, 3] ndarray, but is {s}'.format(image.shape))
        if not isinstance(accum_flow_data, Filterable):
            raise AssertionError(
                'image_data should contain a list of image data')
        accum_flow_data.assert_type('flo')
        Operator.__init__(self)
        self._image = np.copy(image)
        self._flow_data = accum_flow_data

    def _items(self):
        [h, w] = self._image.shape[0:2]
        yield self._image
        for flow in self._flow_data:
            moved_pixels = []
            print('A')
            for y in range(h):
                for x in range(w):
                    u, v = flow[y, x, :]
                    color = self._image[y, x, :]
                    # don't need to add 0.5 as we don't add it later
                    moved_pixels.append([y + v, x + u, color])
            moved_pixels = np.array(moved_pixels)
            synth_image = np.zeros((h, w, 3))
            print('B')
            for py in range(h):
                print(py)
                for px in range(w):
                    for fx, fy, color in moved_pixels:
                        d = abs(fx - px) ** 2 + abs(fy - py) ** 2
                        if d < 2:
                            w_color = color * (2 - d) / 3
                            synth_image[py, px, :] = synth_image[py, px, :] + w_color

            yield synth_image

    def __len__(self):
        return 1 + len(self._flow_data)

    def get_type(self):
        return 'rgb'
