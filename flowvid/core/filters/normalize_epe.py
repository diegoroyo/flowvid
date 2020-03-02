import numpy as np
from ..filterable import Filterable
from .base_filter import Filter


class NormalizeEPEFrame(Filter):
    """
        Normalize EPE (so module ranges from 0..1 instead of 0..n)
        with each frame's local maximum
    """

    def apply(self, data):
        """
            :param data: [h, w, 1] (endpoint error)
            :returns: [h, w, 1] where max(endpoint error) == 1 
        """
        if not isinstance(data, np.ndarray) or not data.ndim == 3:
            raise AssertionError('Data should be [h, w, 1] EPE data ndarray')

        return data / data.max()


class NormalizeEPEVideo(Filter):
    """
        Normalize EPE (so module ranges from 0..1 instead of 0..n)
        with the video's maximum. Can also apply a gamma curve with
        clamping to compensate if there's a high point
    """

    def __init__(self, epe_data, clamp_pct, gamma, verbose):
        Filter.__init__(self)
        if not isinstance(epe_data, Filterable):
            raise AssertionError('Invalid EPE data passed to NormalizeVideo')
        if clamp_pct < 0 or clamp_pct > 1:
            raise AssertionError(
                'Clamp value should be in [0, 1] range instead of {c}'.format(c=clamp_pct))
        epe_data.assert_type('epe')
        self._epe_data = epe_data
        self._max = self._find_max_epe()
        self._clamp = self._max * clamp_pct
        self._inv_gamma = 1.0 / gamma
        self._verbose = verbose

    def _find_max_epe(self):
        """
            Find max EPE in epe_data
            :returns: Largest EPE module in epe_data
        """
        fmax = 0.0
        if self._verbose:
            print('Applying normalization to the whole video...')
        for epe in self._epe_data:
            fmax = max(fmax, epe.max())

        return fmax

    def apply(self, data):
        """
            :param data: [h, w, 1] (endpoint error)
            :returns: [h, w, 1] where max(endpoint error) == 1 
        """
        if not isinstance(data, np.ndarray) or not data.ndim == 3:
            raise AssertionError('Data should be [h, w, 1] EPE data ndarray')

        idm = data > self._clamp
        data[idm] = 1
        data[~idm] = (data[~idm] / self._clamp) ** self._inv_gamma

        return data
