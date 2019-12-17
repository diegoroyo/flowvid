import numpy as np
from ..filterable import Filterable
from .base_operator import Operator


class AddFlowPointsIterator:
    """ Iterates through AddFlowPoints's flow data to generate all the points """

    def __init__(self, obj):
        self._obj = obj
        self._points = obj._points
        self._iter = iter(obj._flow_data)

    def __next__(self):
        flow = next(self._iter)
        self._points = self._obj._add(self._points, flow)
        return self._obj._apply_filters(self._points)


class AddFlowPoints(Operator):
    """
        Given a list of points (for one frame) and a list of flow data,
        move the points with respect to the flow in that pixel
        for each given flow frame
    """

    def __init__(self, points, flow_data):
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
        self._points = points
        self._flow_data = flow_data
        [self._h, self._w] = flow_data[0].shape[0:2]

    def __len__(self):
        return len(self._flow_data)

    def get_type(self):
        return 'point'

    def __iter__(self):
        return AddFlowPointsIterator(self)

    def _add(self, points, flow):
        """
            :param points: [n, 2] ndarray (x0 y0 x1 y1)
            :returns: [n, 2] ndarray with the moved points
                        where (x, y) += flow[x, y]
        """
        points[:, 0] = np.clip(points[:, 0], 0, self._w - 1)
        points[:, 1] = np.clip(points[:, 1], 0, self._h - 1)
        points = points.astype(int)
        flow = flow[points[:, 1], points[:, 0], :]
        return points + flow
