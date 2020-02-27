import numpy as np


def _clip(flow, px, py):
    [h, w] = flow.shape[0:2]
    px = int(np.clip(px, 0, w - 1))
    py = int(np.clip(py, 0, h - 1))
    return px, py


def _clip_flow(flow, px, py):
    cx, cy = _clip(flow, px, py)
    return flow[cy, cx, :]


def _interpolate_flow(flow, fx, fy):
    px, py = int(fx) + 0.5, int(fy) + 0.5
    # get (x1, y1), (x2, y2) bounding square
    if fy - int(fy) > 0.5:
        y1 = py
    else:
        y1 = py - 1
    if fx - int(fx) > 0.5:
        x1 = px
    else:
        x1 = px - 1
    x2 = x1 + 1
    y2 = y1 + 1
    # bilinear interpolation
    t1 = _clip_flow(flow, x1, y1) * (x2 - fx) * (y2 - fy)
    t2 = _clip_flow(flow, x1, y2) * (x2 - fx) * (fy - y1)
    t3 = _clip_flow(flow, x2, y1) * (fx - x1) * (y2 - fy)
    t4 = _clip_flow(flow, x2, y2) * (fx - x1) * (fy - y1)
    return t1 + t2 + t3 + t4


def add_flows(flow1, flow2, interpolate):
    """
        Calculate the result of accumulating flow1 and flow2.
        :param interpolate: Use 4 closest pixels instead of just the closest one.
    """
    [h, w] = flow1.shape[0:2]
    for y in range(h):
        for x in range(w):
            # point to get flow from
            vec = flow1[y, x, :]
            fx = x + vec[0]
            fy = y + vec[1]
            # interpolate flow from points
            if interpolate:
                flow1[y, x, :] = flow1[y, x, :] + \
                    _interpolate_flow(flow2, fx, fy)
            else:
                cx, cy = _clip(flow2, fx, fy)
                flow1[y, x, :] = flow1[y, x, :] + flow2[cy, cx, :]

    return flow1


def add_flow_points(flow, points, interpolate):
    """
        :param points: [n, 2] ndarray (x0 y0)
        :param interpolate: Use 4 closest points to interpolate flow / use closest
        :returns: [n, 2] ndarray with the moved points
                    where (x, y) += flow[x, y]
    """
    new_points = np.empty(points.shape)
    for i, point in enumerate(points):
        if interpolate:
            new_points[i, :] = point + _interpolate_flow(flow, point[0], point[1])
        else:
            cx, cy = _clip(flow, point[0], point[1])
            new_points[i, :] = point + flow[cy, cx, :]
    return new_points
