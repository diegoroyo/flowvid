import numpy as np

from flowvid.core.filterable import Filterable

from flowvid.core.filters.normalizeflow import NormalizeFrame, NormalizeVideo
from flowvid.core.filters.flowtorgb import FlowToRGB

from flowvid.core.operators.addflowrect import AddFlowRect
from flowvid.core.operators.drawrectangle import DrawRectangle


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


def flow_to_rgb(flow):
    """
        Convert Flow data into RGB data using this color circle:
        http://www.quadibloc.com/other/colint.htm
        :param flow: List of flow data, see fv.input.flo(...)
        :returns: List of RGB data
    """
    if not isinstance(flow, Filterable):
        raise AssertionError('flow should be a flow data list')
    return flow._add_filter(FlowToRGB())


"""
    Operators
"""


def draw_rectangle(image, rect, color=[255, 0, 0]):
    """
        Operator. Given a list of images and rectangles,
        draw each rectangle in each of the images from the image list
        :param image: List of rgb data, see fv.input.rgb(...)
        :param rect: List of rect data, see fv.input.rect((...)
        :returns: Iterable object with all the images, with each rectangle drawn
    """
    return DrawRectangle(image, rect, color)


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
