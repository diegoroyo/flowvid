import numpy as np
from numpy import genfromtxt
from flowvid.input.fileinput import FileInput


class TrackPointsIterator:
    def __init__(self, trackdata):
        self._index = -1
        self._max = trackdata._points.shape[0]
        self._data = trackdata._points

    def __next__(self):
        self._index = self._index + 1
        if self._index == self._max:
            raise StopIteration
        else:
            return self._data[self._index, :]


class TrackPoints(FileInput):

    @classmethod
    def rectangles(cls, file_name, rec_format='x0 y0 wx wy'):
        """
            TODO
            rec_format = 'p0 p1 p2 ...' where pi is:
                - <x0>: left side
                - <y0>: top side
                - <x1>: right side
                - <y1>: bottom side
                - <xw>: rectangle width
                - <yw>: rectangle height
                - <-->: ignore field
        """
        result = cls(file_name, 'file')
        result._points = result.__read_rectangles(result.source[0], rec_format)
        return result

    def __iter__(self):
        return TrackPointsIterator(self)

    @classmethod
    def __read_rectangles(self, source, rec_format):
        raw = genfromtxt(source, delimiter=' ')
        [cols, rows] = raw.shape
        if rows < 4:
            raise AssertionError(
                'File {f} has too few arguments ({a}) to describe a rectangle'.format(f=source, a=rows))
        elif rec_format.find('x0') < 0 or rec_format.find('y0') < 0:
            raise AssertionError(
                'rec_format=\'{r}\' needs x0 and y0 components.'.format(r=rec_format))
        elif ((rec_format.find('x1') < 0 or rec_format.find('y1') < 0) and
              (rec_format.find('xw') < 0 or rec_format.find('yw') < 0)):
            raise AssertionError(
                'rec_format=\'{r}\' needs x1/y1 or xw/yw components.'.format(r=rec_format))

        points = np.empty([cols, 4], dtype=np.float32)
        points[:, 0] = raw[:, rec_format.find('x0') // 3]
        points[:, 1] = raw[:, rec_format.find('y0') // 3]
        if rec_format.find('x1') < 0:
            points[:, 2] = points[:, 0] + raw[:, rec_format.find('xw') // 3]
            points[:, 3] = points[:, 1] + raw[:, rec_format.find('yw') // 3]
        else:
            points[:, 2] = raw[:, rec_format.find('x1') // 3]
            points[:, 3] = raw[:, rec_format.find('y1') // 3]

        return points
