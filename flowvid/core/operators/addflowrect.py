import numpy as np
from ..filterable import Filterable
from .baseoperator import Operator


class AddFlowRectIterator:
    """ Iterates through AddFlowRect's flow data to generate all the rectangles """

    def __init__(self, obj):
        self._obj = obj
        self._rect = obj._rect
        self._iter = iter(obj._flow_data)

    def __next__(self):
        flow = next(self._iter)
        self._rect = self._obj._add(self._rect, flow)
        return self._obj._apply_filters(self._rect)


class AddFlowRect(Operator):
    """
        Given one rectangle and a list of flow data, move the rectangle with
        respect to the flow in that pixel for each given flow frame
    """

    def __init__(self, rect, flow_data):
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
        self._rect = rect
        self._flow_data = flow_data
        [self._h, self._w] = flow_data[0].shape[0:2]

    def __len__(self):
        return len(self._flow_data)

    def get_type(self):
        return 'rect'

    def __iter__(self):
        return AddFlowRectIterator(self)

    def _add(self, rect, flow):
        """
            :param rect: [4] ndarray (x0 y0 x1 y1)
            :returns: [4] ndarray with the moved rectangle
                        where (x0, y0) += flow[x0, y0]
                          and (x1, y1) += flow[x1, y1]
        """
        x0 = int(np.clip(rect[0], 0, self._w))
        y0 = int(np.clip(rect[1], 0, self._h))
        x1 = int(np.clip(rect[2], 0, self._w))
        y1 = int(np.clip(rect[3], 0, self._h))
        add = [flow[y0, x0, 0], flow[y0, x0, 1],
               flow[y1, x1, 0], flow[y1, x1, 1]]
        return rect + add
