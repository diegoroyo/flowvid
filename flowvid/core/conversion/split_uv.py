import numpy as np
from ..filterable import Filterable


class SplitUV(Filterable):
    """
        Split flow data into u, v channels (horizontal/vertical movement)
    """

    def __init__(self, flo_data, channel, data_type, ignore_rgb_warning):
        Filterable.__init__(self)
        if not isinstance(flo_data, Filterable):
            raise AssertionError('Invalid flow data passed to split_uv')
        if channel != 'u' and channel != 'U' and channel != 'v' and channel != 'V':
            raise AssertionError('Channel can only be either U or V')
        if data_type != 'ndarray' and data_type != 'rgb' and data_type != 'flo':
            raise AssertionError('Data type must be one of: ndarray, rgb, flo')
        flo_data.assert_type('flo')
        self._flo_data = flo_data
        self._channel = channel
        self._data_type = data_type
        self._ignore_rgb_warning = ignore_rgb_warning

    def _items(self):
        return (self._split_uv(flo) for flo in self._flo_data)

    def __len__(self):
        return len(self._flo_data)

    def get_type(self):
        return self._data_type

    def _split_uv(self, data):
        """
            :param data: [h, w, 2] flow data ndarray
            :returns: U or V channel with specified data type (see constructor)
        """
        if not isinstance(data, np.ndarray) or not data.ndim == 3 or not data.shape[2] == 2:
            raise AssertionError('Data should be [h, w, 2] flow data ndarray')

        if self._channel == 'u':
            dim = 0
        else:  # assume self._channel == 'v'
            dim = 0
        split = data[:, :, dim]

        if self._data_type == 'rgb':
            if not self._ignore_rgb_warning and max(split.max(), split.min() * -1) > 1:
                print('Warning: split_uv assumes that flow data is normalized. This might lead to incorrect images.')
                print('Consider using a normalization filter (see fv.normalize_frame(...) or fv.normalize_video(...).')
            split = np.expand_dims(split, 2)
            split = np.repeat(split, 3, axis=2)
            return (split * 127.5 + 127.5).astype(np.uint8)
        elif self._data_type == 'flo':
            split = np.expand_dims(split, 2)
            split = np.repeat(split, 2, axis=2)
            split[:, :, 1 - dim] = 0
            return split
        else:  # assume self._data_type == 'ndarray'
            return split
