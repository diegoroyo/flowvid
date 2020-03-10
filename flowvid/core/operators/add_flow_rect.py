import numpy as np
from ..filterable import Filterable
from ..filters.accum_flow import AccumFlow
from ..util.add_flow import add_flow_points
from .base_operator import Operator


class AddFlowRect(Operator):
    """
        Given one rectangle and a list of flow data, move the rectangle with
        respect to the flow in that pixel for each given flow frame
    """

    def __init__(self, rect, flow_data, interpolate, accumulate):
        if not isinstance(rect, np.ndarray):
            raise AssertionError('rect should be a size 4 ndarray')
        if rect.ndim != 1 or rect.size != 4:
            raise AssertionError(
                'rect should be a size 4 ndarray, but is {s}'.format(rect.shape))
        if not isinstance(flow_data, Filterable):
            raise AssertionError(
                'flow_data should contain a list of flow data')
        flow_data.assert_type('flo')
        Operator.__init__(self)
        self._rect = np.copy(rect).astype(float)
        self._flow_data = flow_data
        self._interpolate = interpolate
        self._accumulate = accumulate
        [self._h, self._w] = flow_data[0].shape[0:2]

    def _items(self):
        yield self._rect
        for flow in self._flow_data:
            new_rect = self._add(self._rect, flow)
            if self._accumulate:
                self._rect = new_rect
            yield new_rect

    def __len__(self):
        return 1 + len(self._flow_data)

    def get_type(self):
        return 'rect'

    def _add(self, rect, flow):
        """
            :param rect: [4] ndarray (x0 y0 x1 y1)
            :returns: [4] ndarray with the moved rectangle
                        where (x0, y0) += flow[x0, y0]
                          and (x1, y1) += flow[x1, y1]
        """
        return add_flow_points(flow, rect.reshape((2, 2)), self._interpolate).flatten()
