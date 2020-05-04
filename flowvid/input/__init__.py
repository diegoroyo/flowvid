from .flo_data import FloData
from .rgb_data import RGBData
from .track_points import TrackPoints, TrackRectangles
from .point_input import pyplot_prompt


def flo(path, dir_first=0, dir_total=None):
    """
        Read .flo files and process them as a list of flow data
        Files must be encoded with the Middlebury .flo format:
        http://vision.middlebury.edu/flow/code/flow-code/README.txt
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
    return RGBData(path, extensions=('.png', '.bmp', '.jpg', '.jpeg'), dir_first=dir_first, dir_total=dir_total)


def points(custom_points):
    """
        Convert a [n, 2] ndarray with (x, y) point data for one frame
        to an object usable by filters/operators.
        :param custom_points: [n, 2] ndarray which contains a set of points
                              for a video frame, in (x, y) pixel format
        :returns: Iterable and indexable object with 1 set of points
    """
    return TrackPoints(custom_points)


def prompt_points(n, image):
    """
        Prompt the user to select points on a given image
        :param n: Number of points to select
        :param image: Image background to select the points from. Either:
                      - (height, width) tuple for an empty image
                      - (height, width, 3) RGB ndarray for an image (see fv.input.rgb(...))
        :returns: Iterable and indexable object with 1 set of points
    """
    return TrackPoints(pyplot_prompt(n, image))


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
