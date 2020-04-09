import numpy as np
from ..filterable import Filterable


class EPEToRGB(Filterable):
    """
        Convert EPE data to an image where brighter colors mean higher EPE
        EPE should be normalized before use
    """

    def __init__(self, epe_data, color):
        Filterable.__init__(self)
        if not isinstance(epe_data, Filterable):
            raise AssertionError('epe_data should contain a list of epe data')
        epe_data.assert_type('epe')

        self._epe_data = epe_data
        self._color = color

    def _items(self):
        return (self._epe_to_rgb(epe) for epe in self._epe_data)

    def __len__(self):
        return len(self._epe_data)

    def get_type(self):
        return 'rgb'

    def _epe_to_rgb(self, epe):
        """
            :param data: [h, w] ndarray (epe data, normalized)
            :returns: [h, w, 3] ndarray (rgb data)
        """
        if not isinstance(epe, np.ndarray) or not epe.ndim == 2:
            raise AssertionError('Data should be [h, w] epe data ndarray')

        def mult(f):
            return [self._color[0] * f, self._color[1] * f, self._color[2] * f]

        image = np.array(list(map(mult, epe))).astype(np.uint8)
        return np.swapaxes(image, 1, 2)
