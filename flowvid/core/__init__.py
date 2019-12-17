import numpy as np

from .filterable import Filterable

from .filters.normalize_flow import NormalizeFrame, NormalizeVideo

from .conversion.flow_to_rgb import FlowToRGB

from .operators.add_flow_rect import AddFlowRect
from .operators.add_flow_points import AddFlowPoints
from .operators.draw_rectangle import DrawRectangle
from .operators.draw_points import DrawPoints


"""
    Filters
"""


def normalize_frame(flow):
    """
        Normalize flow data (so module ranges from 0..1 instead of 0..n)
        with each frame's local maximum.
        :param flow: List of flow data, see fv.input.flo(...)
        :returns: List of flow data, normalized.
    """
    if not isinstance(flow, Filterable):
        raise AssertionError('flow should be a flow data list')
    return flow._add_filter(NormalizeFrame())


def normalize_video(flow, clamp_pct=1.0, gamma=1.0):
    """
        Normalize flow (so module ranges from 0..1 instead of 0..n)
        with the video's maximum. Can also apply a gamma curve with
        clamping to compensate if there's a high point.
        :param flow: List of flow data, see fv.input.flo(...)
        :param clamp_pct: Modules higher than max * clamp_pct are clamped to 1
        :param gamma: Exponential curve (module01 = module01 ** gamma)
        :returns: List of flow data, normalized.
    """
    if not isinstance(flow, Filterable):
        raise AssertionError('flow should be a flow data list')
    return flow._add_filter(NormalizeVideo(flow, clamp_pct, gamma))


"""
    Conversion
"""


def flow_to_rgb(flow):
    """
        Convert Flow data into RGB data using this color circle:
        http://www.quadibloc.com/other/colint.htm
        :param flow: List of flow data, see fv.input.flo(...)
        :returns: List of RGB data
    """
    return FlowToRGB(flow)


"""
    Operators
"""


def draw_rectangle(image, rect, color=[255, 0, 0]):
    """
        Operator. Given a list of images and rectangles,
        draw each rectangle in each of the images from the image list
        :param image: List of rgb data, see fv.input.rgb(...)
        :param rect: List of rect data, see fv.input.rect(...)
        :param color: [r, g, b] list, color of the rectangle (default: red)
        :returns: Iterable object with all the images, with each rectangle drawn
    """
    return DrawRectangle(image, rect, color)


def draw_points(image, points, color='random'):
    """
        Operator. Given a list of images and sets of points,
        draw each set of points in each of the images from the image list
        :param image: List of rgb data, see fv.input.rgb(...)
        :param points: List of points data, see fv.input.points(...)
        :param color: [r, g, b] list, color of the points. Can be 'random' so each point
                      is of a random color (consistent between frames, default mode).
        :returns: Iterable object with all the images, with each rectangle drawn
    """
    return DrawPoints(image, points, color)


def add_flow_rect(rect, flow):
    """
        Operator. Given one rectangle and a list of flow data,
        move the rectangle with respect to the flow in that pixel
        for each given flow frame.
        :param rect: Rectangle, 4 element ndarray [x0, y0, x1, y1]
        :param flow: List of flow data, see fv.input.flo(...)
        :returns: Iterable object with all the rectangles
    """
    return AddFlowRect(rect, flow)


def add_flow_points(points, flow):
    """
        Operator. Given a list of points (for one frame) and a
        list of flow data, move the points with respect to the flow
        in that pixel for each given flow frame
        :param points: Set of points, [n, 2] ndarray (x, y)
        :param flow: List of flow data, see fv.input.flo(...)
        :returns: Iterable object with all the rectangles
    """
    return AddFlowPoints(points, flow)
