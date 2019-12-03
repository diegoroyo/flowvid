import numpy as np
from ..filterable import Filterable

# All this code is adapted from the one available at:
# https://people.csail.mit.edu/celiu/OpticalFlow/
# which uses the following color circle idea:
# http://www.quadibloc.com/other/colint.htm


class FlowToRGBIterator:
    def __init__(self, obj):
        self._obj = obj
        self._iter = iter(obj._flo_data)

    def __next__(self):
        flow = next(self._iter)
        return self._obj._apply_filters(FlowToRGB._flow_to_rgb(flow))


class FlowToRGB(Filterable):
    """
        Convert Flow data into RGB data using this color circle:
        http://www.quadibloc.com/other/colint.htm
    """

    colorwheel = None

    def __init__(self, flo_data):
        Filterable.__init__(self)
        if FlowToRGB.colorwheel is None:
            FlowToRGB.colorwheel = FlowToRGB.__make_color_wheel()
        if not isinstance(flo_data, Filterable):
            raise AssertionError('flo_data should contain a list of flo data')
        flo_data.assert_type('flo')

        self._flo_data = flo_data

    def __iter__(self):
        return FlowToRGBIterator(self)

    def __len__(self):
        return len(self._flo_data)

    def get_type(self):
        return 'rgb'

    @staticmethod
    def __make_color_wheel():
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

    @staticmethod
    def _flow_to_rgb(data):
        """
            :param data: [h, w, 2] ndarray (flow data)
            :returns: [h, w, 3] ndarray (rgb data) using color wheel
        """
        if not isinstance(data, np.ndarray) or not data.ndim == 3:
            raise AssertionError('Data should be [h, w, 2] flow data ndarray')

        ncols = len(FlowToRGB.colorwheel)

        fu = data[:, :, 0]
        fv = data[:, :, 1]

        [h, w] = fu.shape
        data = np.empty([h, w, 3], dtype=np.uint8)

        rad = np.sqrt(fu ** 2 + fv ** 2)
        a = np.arctan2(-fv, -fu) / np.pi
        fk = (a + 1) / 2 * (ncols - 1)  # -1~1 mapped to 1~ncols
        k0 = fk.astype(np.uint8)
        k1 = (k0 + 1) % ncols
        f = fk - k0
        for i in range(3):  # r g b
            col0 = FlowToRGB.colorwheel[k0, i]/255.0
            col1 = FlowToRGB.colorwheel[k1, i]/255.0
            col = np.multiply(1.0-f, col0) + np.multiply(f, col1)

            # increase saturation with radius
            col = 1.0 - np.multiply(rad, 1.0 - col)

            # save to data channel i
            data[:, :, i] = np.floor(col * 255).astype(np.uint8)

        return data
