from .flodata import FloData
from .rgbdata import RGBData
from .trackpoints import TrackRectangles


def flo(path, dir_first=0, dir_total=None):
    return FloData(path, extensions=('.flo'), dir_first=dir_first, dir_total=dir_total)


def rgb(path, dir_first=0, dir_total=None):
    return RGBData(path, extensions=('.png', '.bmp', '.jpg'), dir_first=dir_first, dir_total=dir_total)


def rect(path, rect_format='x0 y0 xw yw', elem_first=0, elem_total=None):
    return TrackRectangles(path, rect_format=rect_format, elem_first=elem_first, elem_total=elem_total)
