import numpy as np


def _make_color_wheel():
    """ :returns: [ncols, 3] ndarray colorwheel """
    # how many hues ("cols") separate each color
    # (for this color wheel)
    RY = 15  # red-yellow
    YG = 6   # yellow-green
    GC = 4   # green-cyan
    CB = 11  # cyan-blue
    BM = 13  # blue-magenta
    MR = 6   # magenta-red
    ncols = RY + YG + GC + CB + BM + MR
    colorwheel = np.zeros((ncols, 3), dtype=np.uint8)  # r g b

    col = 0
    # RY
    colorwheel[col:col+RY, 0] = 255
    colorwheel[col:col+RY, 1] = np.floor(255*np.arange(RY)/RY)
    col = col + RY
    # YG
    colorwheel[col:col+YG, 0] = np.ceil(255*np.arange(YG, 0, -1)/YG)
    colorwheel[col:col+YG, 1] = 255
    col = col + YG
    # GC
    colorwheel[col:col+GC, 1] = 255
    colorwheel[col:col+GC, 2] = np.floor(255*np.arange(GC)/GC)
    col = col + GC
    # CB
    colorwheel[col:col+CB, 1] = np.ceil(255*np.arange(CB, 0, -1)/CB)
    colorwheel[col:col+CB, 2] = 255
    col = col + CB
    # BM
    colorwheel[col:col+BM, 2] = 255
    colorwheel[col:col+BM, 0] = np.floor(255*np.arange(BM)/BM)
    col = col + BM
    # MR
    colorwheel[col:col+MR, 2] = np.ceil(255*np.arange(MR, 0, -1)/MR)
    colorwheel[col:col+MR, 0] = 255

    return colorwheel


_colorwheel = _make_color_wheel()


def flow_to_rgb(flo_data):
    """
        :param flo_data: [h, w, 2] ndarray (flow data)
                         (must be normalized to 0-1 range)
        :returns: [h, w, 3] ndarray (rgb data) using color wheel
    """
    if not isinstance(flo_data, np.ndarray) or not flo_data.ndim == 3:
        raise AssertionError('Data should be [h, w, 2] flow data ndarray')

    ncols = len(_colorwheel)

    fu = flo_data[:, :, 0]
    fv = flo_data[:, :, 1]

    [h, w] = fu.shape
    rgb_data = np.empty([h, w, 3], dtype=np.uint8)

    rad = np.sqrt(fu ** 2 + fv ** 2)
    a = np.arctan2(-fv, -fu) / np.pi
    fk = (a + 1) / 2 * (ncols - 1)  # -1~1 mapped to 1~ncols
    k0 = fk.astype(np.uint8)
    k1 = (k0 + 1) % ncols
    f = fk - k0
    for i in range(3):  # r g b
        col0 = _colorwheel[k0, i]/255.0
        col1 = _colorwheel[k1, i]/255.0
        col = np.multiply(1.0-f, col0) + np.multiply(f, col1)

        # increase saturation with radius
        col = 1.0 - np.multiply(rad, 1.0 - col)

        # save to data channel i
        rgb_data[:, :, i] = np.floor(col * 255).astype(np.uint8)

    return rgb_data
