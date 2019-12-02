import numpy as np
from flowvid.fvcore.operators.baseoperator import Operator


class AddFlowRectIterator:
    def __init__(self, obj):
        self._obj = obj
        self._rect = obj._rect
        self._iter = iter(obj._flow_data)

    def __next__(self):
        flow = next(self._iter)
        self._rect = self._obj._add(self._rect, flow)
        return self._obj._apply_filters(self._rect)


class AddFlowRect(Operator):
    def __init__(self, rect, flow_data):
        Operator.__init__(self)
        self._rect = rect
        self._flow_data = flow_data
        [self._h, self._w] = flow_data[0].shape[0:2]

    def __len__(self):
        return len(self._flow_data)

    def __iter__(self):
        return AddFlowRectIterator(self)

    def _add(self, rect, flow):
        x0 = int(np.clip(rect[0], 0, self._w))
        y0 = int(np.clip(rect[1], 0, self._h))
        x1 = int(np.clip(rect[2], 0, self._w))
        y1 = int(np.clip(rect[3], 0, self._h))
        add = [flow[y0, x0, 0], flow[y0, x0, 1],
               flow[y1, x1, 0], flow[y1, x1, 1]]
        return rect + add
