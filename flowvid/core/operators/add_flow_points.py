import numpy as np
from ..filterable import Filterable
from ..util.add_flow import add_flow_points
from ..filters.accum_flow import AccumFlow
from .base_operator import Operator


class AddFlowPoints(Operator):
    """
        Given a list of points (for one frame) and a list of flow data,
        move the points with respect to the flow in that pixel
        for each given flow frame
    """

    def __init__(self, points, flow_data, interpolate, accumulate):
        if not isinstance(points, np.ndarray):
            raise AssertionError('points should be a [n, 2] ndarray')
        if points.ndim != 2 or points.shape[1] != 2:
            raise AssertionError(
                'points should be a [n, 2] ndarray, but is {s}'.format(points.shape))
        if not isinstance(flow_data, Filterable):
            raise AssertionError(
                'flow_data should contain a list of flow data')
        flow_data.assert_type('flo')
        Operator.__init__(self)
        self._points = np.copy(points).astype(float)
        self._flow_data = flow_data
        self._interpolate = interpolate
        self._accumulate = accumulate
        [self._h, self._w] = flow_data[0].shape[0:2]

    def _items(self):
        yield self._points
        for flow in self._flow_data:
            new_points = add_flow_points(
                flow, self._points, self._interpolate)
            if self._accumulate:
                self._points = new_points
            yield new_points

    def __len__(self):
        return 1 + len(self._flow_data)

    def get_type(self):
        return 'point'
