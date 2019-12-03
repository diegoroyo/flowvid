import numpy as np
from ..filterable import Filterable
from .basefilter import Filter


class NormalizeFrame(Filter):
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
        fmax = np.sqrt(fu ** 2 + fv ** 2).max()
        data[:, :, 0] = fu / fmax
        data[:, :, 1] = fv / fmax
        return data


class NormalizeVideo(Filter):
    """
        Normalize flow (so module ranges from 0..1 instead of 0..n)
        with the video's maximum. Can also apply a gamma curve with
        clamping to compensate if there's a high point
    """

    def __init__(self, flow_data, clamp_pct, gamma):
        Filter.__init__(self)
        if not isinstance(flow_data, Filterable):
            raise AssertionError('Invalid flow data passed to NormalizeVideo')
        if clamp_pct < 0 or clamp_pct > 1:
            raise AssertionError(
                'Clamp value should be in [0, 1] range instead of {c}'.format(c=clamp_pct))
        flow_data.assert_type('flo')
        self._max = NormalizeVideo.__find_max_flow(flow_data)
        self._clamp = self._max * clamp_pct
        self._gamma = gamma

    @staticmethod
    def __find_max_flow(flow_data):
        """
            Find max flow module in flow_data
            :param flow_data: [h, w, 2] ndarray
            :returns: Largest flow vector module in flow_data
        """
        fmax = 0.0
        for flow in flow_data:
            fu = flow[:, :, 0]
            fv = flow[:, :, 1]
            fmax = max(fmax, np.sqrt(fu ** 2 + fv ** 2).max())

        return fmax

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
        fu[~idu] = np.sign(fu[~idu]) * (np.abs(fu[~idu]) ** self._gamma)

        idv = fv > self._clamp
        fv[idv] = 1
        fv[~idv] = fv[~idv] / self._clamp
        fv[~idv] = np.sign(fv[~idv]) * (np.abs(fv[~idv]) ** self._gamma)

        data[:, :, 0] = fu
        data[:, :, 1] = fv
        return data
