import numpy as np
from numpy import genfromtxt
from flowvid.fvinput.fileinput import FileInput


class TrackRectangles(FileInput):

    def __init__(self, path, rect_format, elem_first, elem_total):
        """
            TODO
            rect_format = 'p0 p1 p2 ...' where pi is:
                - <x0>: left side
                - <y0>: top side
                - <x1>: right side
                - <y1>: bottom side
                - <xw>: rectangle width
                - <yw>: rectangle height
                - <-->: ignore field
        """
        FileInput.__init__(self, path)
        self._points = self.__read_rectangles(
            self.source[0], rect_format, elem_first, elem_total)

    def __len__(self):
        return self._points.shape[0]

    def _getitem(self, index):
        # TODO index dentro de _points
        return self._points[index, :]

    @staticmethod
    def __read_rectangles(source, rec_format, elem_first, elem_total):
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

        if elem_total is None:
            elem_total = len(points) - elem_first

        points = points[elem_first:elem_first+elem_total, :]

        return points
