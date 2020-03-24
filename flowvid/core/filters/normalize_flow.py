import numpy as np
from ..filterable import Filterable
from .base_filter import Filter


class NormalizeFlowFrame(Filter):
    """
        Normalize flow (so module ranges from 0..1 instead of 0..n)
        with each frame's local maximum
    """

    def apply(self, data):
        """
            :param data: [h, w, 2] (u, v components)
            :returns: [h, w, 2] where max(sqrt(u ** 2 + v ** 2)) == 1 
        """
        if not isinstance(data, np.ndarray) or not data.ndim == 3:
            raise AssertionError('Data should be [h, w, 2] flow data ndarray')

        fu = data[:, :, 0]
        fv = data[:, :, 1]
        # add small epsilon for float accuracy
        fmax = np.sqrt(fu ** 2 + fv ** 2).max() + 1e-3
        norm_data = np.empty(data.shape)
        if fmax == 0:
            norm_data[:, :, 0] = fu
            norm_data[:, :, 1] = fv
        else:
            norm_data[:, :, 0] = fu / fmax
            norm_data[:, :, 1] = fv / fmax
        return norm_data


class NormalizeFlowVideo(Filter):
    """
        Normalize flow (so module ranges from 0..1 instead of 0..n)
        with the video's maximum. Can also apply a gamma curve with
        clamping to compensate if there's a high point
    """

    def __init__(self, flow_data, clamp_pct, gamma, verbose):
        Filter.__init__(self)
        if not isinstance(flow_data, Filterable):
            raise AssertionError('Invalid flow data passed to NormalizeVideo')
        if clamp_pct < 0 or clamp_pct > 1:
            raise AssertionError(
                'Clamp value should be in [0, 1] range instead of {c}'.format(c=clamp_pct))
        flow_data.assert_type('flo')
        self._flow_data = flow_data
        self._inv_gamma = 1.0 / gamma
        self._verbose = verbose
        self._max = self._find_max_flow()
        self._clamp = self._max * clamp_pct

    def _find_max_flow(self):
        """
            Find max flow module in flow_data
            :returns: Largest flow vector module in flow_data
        """
        fmax = 0.0
        if self._verbose:
            print('Applying normalization to the whole video...')
        for flow in self._flow_data:
            fu = flow[:, :, 0]
            fv = flow[:, :, 1]
            fmax = max(fmax, np.sqrt(fu ** 2 + fv ** 2).max())

        # add small epsilon for float accurady
        return fmax + 1e-3

    def apply(self, data):
        """
            :param data: [h, w, 2] (u, v components)
            :returns: [h, w, 2] where max(sqrt(u ** 2 + v ** 2)) == 1 
        """
        if not isinstance(data, np.ndarray) or not data.ndim == 3:
            raise AssertionError('Data should be [h, w, 2] flow data ndarray')

        fu = data[:, :, 0]
        fv = data[:, :, 1]

        idu = fu > self._clamp
        fu[idu] = 1
        fu[~idu] = fu[~idu] / self._clamp
        fu[~idu] = np.sign(fu[~idu]) * (np.abs(fu[~idu]) ** self._inv_gamma)

        idv = fv > self._clamp
        fv[idv] = 1
        fv[~idv] = fv[~idv] / self._clamp
        fv[~idv] = np.sign(fv[~idv]) * (np.abs(fv[~idv]) ** self._inv_gamma)

        norm_data = np.empty(data.shape)
        norm_data[:, :, 0] = fu
        norm_data[:, :, 1] = fv
        return norm_data
