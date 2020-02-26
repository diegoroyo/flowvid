import numpy as np

from .filterable import Filterable

from .filters.normalize_flow import NormalizeFrame, NormalizeVideo
from .filters.accum_flow import AccumFlow

from .conversion.flow_to_rgb import FlowToRGB

from .operators.add_flow_rect import AddFlowRect
from .operators.add_flow_points import AddFlowPoints
from .operators.draw_rectangle import DrawRectangle
from .operators.draw_points import DrawPoints
from .operators.endpoint_error import EndPointError
from .operators.track_from_first import TrackFromFirst
from .operators.synthesize_image import SynthesizeImage


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


def accumulate(flow, interpolate=True):
    """
        Accumulate optical flow from first frame, so instead
        of it being from images 0->1, 1->2, 2->3, etc. it goes
        from images 0->1, 0->2, 0->3, etc.
        :param flow: List of flow data, see fv.input.flo(...)
        :param interpolate: If true, flow in a point is added by interpolating from its
                            four closest pixels. If false, it only uses the closest pixel.
        :returns: List of flow data, accumulated from the first frame.
    """
    if not isinstance(flow, Filterable):
        raise AssertionError('flow should be a flow data list')
    return flow._add_filter(AccumFlow(flow, interpolate))


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


def draw_points(image, points, color='random', num_trail=1):
    """
        Operator. Given a list of images and sets of points,
        draw each set of points in each of the images from the image list
        :param image: List of rgb data, see fv.input.rgb(...)
        :param points: List of points data, see fv.input.points(...)
        :param color: [r, g, b] list, color of the points. Can be 'random' so each point
                      is of a random color (consistent between frames, default mode).
        :returns: Iterable object with all the images, with each rectangle drawn
    """
    return DrawPoints(image, points, color, num_trail)


def add_flow_rect(rect, flow, interpolate=True):
    """
        Operator. Given one rectangle and a list of flow data,
        move the rectangle with respect to the flow in that pixel
        for each given flow frame.
        :param rect: Rectangle, 4 element ndarray [x0, y0, x1, y1]
        :param flow: List of flow data, see fv.input.flo(...)
        :returns: Iterable object with all the rectangles
    """
    return AddFlowRect(rect, flow, interpolate)


def add_flow_points(points, flow, interpolate=True):
    """
        Operator. Given a list of points (for one frame) and a
        list of flow data, move the points with respect to the flow
        in that pixel for each given flow frame
        :param points: Set of points, [n, 2] ndarray (x, y)
        :param flow: List of flow data, see fv.input.flo(...)
        :returns: Iterable object with all the rectangles
    """
    return AddFlowPoints(points, flow, interpolate)


def endpoint_error(flow_est, flow_gt):
    """
        Operator. Given estimated flow data and its ground truth,
        calculate Average Endpoint Error for all frames
        :param flow_est: Estimated flow, see fv.input.flo(...)
        :param flow_gt: Flow ground truth, see fv.input.flo(...)
        :returns: Iterable object with EPE per pixel and frame
    """
    return EndPointError(flow_est, flow_gt)


def track_from_first(point_data, image_data, color='random', draw_lines=True, vertical=False):
    """
        Operator. Given a set of points and image data, track the set
        of points to see if they track the image's features correctly
        :param point_data: List of points data, see fv.input.points(...)
        :param image_data: List of rgb data, see fv.input.rgb(...)
        :returns: List of images with features' correspondences
    """
    return TrackFromFirst(point_data, image_data, color, draw_lines, vertical)


def synthesize_image(image, accum_flow_data):
    """
        Operator. Given an initial image and accumulated flow,
        generate synthesized images moving the pixels according to the flow
        :param image: Image, ndarray with [height, width, 3] RGB shape
        :param accum_flow_data: List of accumulated flow, see fv.accumulate(...)
        :returns: List of synthesized images from the first one
    """
    return SynthesizeImage(image, accum_flow_data)
