import numpy as np
from flowvid.fvcore.filterable import Filterable
from flowvid.fvcore.filters.basefilter import Filter


class NormalizeFrame(Filter):
    def apply(self, data):
        if not isinstance(data, np.ndarray) or not data.ndim == 3:
            raise AssertionError('Data should be [h, w, 2] flow data ndarray')

        fu = data[:, :, 0]
        fv = data[:, :, 1]
        fmax = np.sqrt(fu ** 2 + fv ** 2).max()
        data[:, :, 0] = fu / fmax
        data[:, :, 1] = fv / fmax
        return super().apply(data)


class NormalizeVideo(Filter):
    def __init__(self, flo_data, clamp_pct, gamma):
        Filter.__init__(self)
        if not isinstance(flo_data, Filterable):
            raise AssertionError('Invalid flow data passed to NormalizeVideo')
        self._max = NormalizeVideo.__find_max_flow(flo_data)
        self._clamp = self._max * clamp_pct
        self._gamma = gamma

    @staticmethod
    def __find_max_flow(flo_data):
        fmax = 0.0
        for flow in flo_data:
            fu = flow[:, :, 0]
            fv = flow[:, :, 1]
            fmax = max(fmax, np.sqrt(fu ** 2 + fv ** 2).max())

        print(fmax)
        return fmax

    def apply(self, data):
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
        return super().apply(data)
