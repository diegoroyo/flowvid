import numpy as np
from ..filterable import Filterable
from .base_operator import Operator


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
        if len(flow_est) != len(flow_gt):
            raise AssertionError(
                'flow_est and flow_gt should be of the same length')
        flow_est.assert_type('flo')
        flow_gt.assert_type('flo')
        Operator.__init__(self)
        self._flow_est = flow_est
        self._flow_gt = flow_gt

    def _items(self):
        return (self._get_epe(est, gt) for (est, gt) in zip(self._flow_est, self._flow_gt))

    def __len__(self):
        return len(self._flow_est)

    def get_type(self):
        return 'epe'

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
