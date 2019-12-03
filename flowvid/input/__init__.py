from .flodata import FloData
from .rgbdata import RGBData
from .trackpoints import TrackRectangles


def flo(path, dir_first=0, dir_total=None):
    """
        Read .flo files and process them as a list of flow data
        :param path: Either a file or a directory
        :param dir_first: If path is a directory and contains elements 0..n-1,
                            return elements from range dir_first..n-1
                            (defaults to 0)
        :param dir_total: If path is a directory, set number of elements to return
                            e.g. if it contains elements 0..n-1, return dir_first..dir_first+dir_total
                            (if None, return all elements from the directory)
        :returns: Iterable and indexable list of flow data
    """
    return FloData(path, extensions=('.flo'), dir_first=dir_first, dir_total=dir_total)


def rgb(path, dir_first=0, dir_total=None):
    """
        Read .png/.bmp/.jpg files and process them as a list of RGB data
        :param path: Either a file or a directory
        :param dir_first: If path is a directory and contains elements 0..n-1,
                            return elements from range dir_first..n-1
                            (defaults to 0)
        :param dir_total: If path is a directory, set number of elements to return
                            e.g. if it contains elements 0..n-1, return dir_first..dir_first+dir_total
                            (if None, return all elements from the directory)
        :returns: Iterable and indexable list of RGB data
    """
    return RGBData(path, extensions=('.png', '.bmp', '.jpg'), dir_first=dir_first, dir_total=dir_total)


def rect(path, rect_format='x0 y0 xw yw', elem_first=0, elem_total=None):
    """
        Read a file and return a list of rectangle data
        :param path: Text file, which contains one line per frame,
                        describing rectangle data in rect_format
        :param rect_format: Sequence of elements 'p0 p1 p2 ...' where pi is:
                            - <x0>: left side
                            - <y0>: top side
                            - <x1>: right side
                            - <y1>: bottom side
                            - <xw>: rectangle width
                            - <yw>: rectangle height
                            - <-->: ignore field
        :param elem_first: First line of the file to retrieve (elem_first..n-1)
        :param elem_total: Number of lines to retrieve (elem_first..elem_first+elem_total)
                            (if None, return all lines)
        :returns: Iterable and indexable list of flow data
    """
    return TrackRectangles(path, rect_format=rect_format, elem_first=elem_first, elem_total=elem_total)
