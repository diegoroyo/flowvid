import numpy as np
from ..filterable import Filterable
from ..util.add_flow import add_flows
from .base_filter import Filter


class AccumFlow(Filter):
    """
        Accumulate optical flow from first frame, so instead
        of it being from images 0->1, 1->2, 2->3, etc. it goes
        from images 0->1, 0->2, 0->3, etc.
    """

    def __init__(self, flow_data, interpolate):
        Filter.__init__(self)
        if not isinstance(flow_data, Filterable):
            raise AssertionError('Invalid flow data passed to AccumFlow')
        flow_data.assert_type('flo')

        [h, w] = next(iter(flow_data)).shape[0:2]
        self._accum = np.zeros((h, w, 2))
        self._interpolate = interpolate

    def apply(self, data):
        """
            :param data: [h, w, 2] (u, v components)
            :returns: [h, w, 2] with accumulated optical flow data
        """
        if not isinstance(data, np.ndarray) or not data.ndim == 3:
            raise AssertionError('Data should be [h, w, 2] flow data ndarray')
        self._accum = add_flows(self._accum, data, self._interpolate)
        return self._accum
