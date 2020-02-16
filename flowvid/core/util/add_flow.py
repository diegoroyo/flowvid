import numpy as np


def _clip(flow, px, py):
    [h, w] = flow.shape[0:2]
    px = int(np.clip(px, 0, w - 1))
    py = int(np.clip(py, 0, h - 1))
    return px, py


def _weight(fx, fy, px, py):
    return (2 - abs(fx - px) - abs(fy - py)) / 4


def _weight_flow(flow, fx, fy, px, py):
    cx, cy = _clip(flow, px, py)
    return _weight(fx, fy, px, py) * flow[cy, cx, :]


def _interpolate_flow(flow, fx, fy):
    ox, oy = int(fx) + 0.5, int(fy) + 0.5
    px, py = ox, oy
    # closest pixel (same as non-interpolation)
    vec = _weight_flow(flow, fx, fy, ox, oy)
    # pixel up/down
    if fy - int(fy) > 0.5:
        vec = vec + _weight_flow(flow, fx, fy, px, py + 1)
    else:
        vec = vec + _weight_flow(flow, fx, fy, px, py - 1)
    # two pixels to the left/right
    if fx - int(fx) > 0.5:
        px = px + 1
    else:
        px = px - 1
    vec = vec + _weight_flow(flow, fx, fy, px, py)
    if fy - int(fy) > 0.5:
        vec = vec + _weight_flow(flow, fx, fy, px, py + 1)
    else:
        vec = vec + _weight_flow(flow, fx, fy, px, py - 1)
    # return weighted interpolated flow
    return vec


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
    for i, point in enumerate(points):
        if interpolate:
            points[i, :] = point + _interpolate_flow(flow, point[0], point[1])
        else:
            cx, cy = _clip(flow, point[0], point[1])
            points[i, :] = point + flow[cy, cx, :]
    return points