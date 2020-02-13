import numpy as np
from ..filterable import Filterable
from .base_operator import Operator


class EndPointErrorIterator:
    """ Iterates through EndPointError's AEE data to generate all the values """

    def __init__(self, obj):
        self._obj = obj
        self._iter_est = iter(obj._flow_est)
        self._iter_gt = iter(obj._flow_gt)

    def __next__(self):
        flow_est = next(self._iter_est)
        flow_gt = next(self._iter_gt)
        self._epe = self._obj._get_epe(flow_est, flow_gt)
        return self._obj._apply_filters(self._epe)


class EndPointError(Operator):
    """
        Calculate Endpoint Error for each frame, comparing
        estimated flow data to its ground truth
    """

    def __init__(self, flow_est, flow_gt):
        if not isinstance(flow_est, Filterable):
            raise AssertionError(
                'flow_est should contain a list of flow data')
        if not isinstance(flow_gt, Filterable):
            raise AssertionError(
                'flow_gt should contain a list of flow data')
        flow_est.assert_type('flo')
        flow_gt.assert_type('flo')
        Operator.__init__(self)
        self._flow_est = flow_est
        self._flow_gt = flow_gt

    def __len__(self):
        return len(self._flow_est)

    def get_type(self):
        return 'float'

    def __iter__(self):
        return EndPointErrorIterator(self)

    def _get_epe(self, flow_est, flow_gt):
        """
            :param flow_est: [h, w, 2] (u, v components)
                             estimated flow vectors
            :param flow_gt: [h, w, 2] (u, v components)
                            ground truth flow vectors
            :returns: [h, w] Endpoint error per-pixel ||Vest - Vgt||
        """
        dif = flow_est - flow_gt
        difu = dif[:, :, 0]
        difv = dif[:, :, 1]
        return np.sqrt(difu ** 2 + difv ** 2)
