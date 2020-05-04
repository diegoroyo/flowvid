import numpy as np

from .filterable import Filterable

from .filters.normalize_flow import NormalizeFlowFrame, NormalizeFlowVideo
from .filters.normalize_epe import NormalizeEPEFrame, NormalizeEPEVideo
from .filters.accum_flow import AccumFlow

from .conversion.flow_to_rgb import FlowToRGB
from .conversion.epe_to_rgb import EPEToRGB
from .conversion.split_uv import SplitUV

from .operators.add_flow_rect import AddFlowRect
from .operators.add_flow_points import AddFlowPoints
from .operators.draw_rectangle import DrawRectangle
from .operators.draw_points import DrawPoints
from .operators.draw_flow_arrows import DrawFlowArrows
from .operators.endpoint_error import EndPointError
from .operators.track_from_first import TrackFromFirst
from .operators.synthesize_image import SynthesizeImage


"""
    Filters
"""


def normalize_frame(data):
    """
        Normalize flow/epe data (so module ranges from 0..1 instead of 0..n)
        with each frame's local maximum.
        :param data: List of flo/epe data, see fv.input.flo(...) or fv.endpoint_error(...)
        :returns: List of flow/epe data, normalized.
    """
    if not isinstance(data, Filterable):
        raise AssertionError('data should be a flow/epe data list')
    data.assert_type('flo', 'epe')
    if data.get_type() == 'flo':
        return data._add_filter(NormalizeFlowFrame())
    else:
        return data._add_filter(NormalizeEPEFrame())


def normalize_video(data, clamp_pct=1.0, gamma=1.0, verbose=False):
    """
        Normalize flow/epe (so module ranges from 0..1 instead of 0..n)
        with the video's maximum. Can also apply a gamma curve with
        clamping to compensate if there's a high point.
        :param data: List of flo/epe data, see fv.input.flo(...) or fv.endpoint_error(...)
        :param clamp_pct: Modules higher than max * clamp_pct are clamped to 1
        :param gamma: Exponential curve (module01 = module01 ** gamma)
        :param verbose: Log console messages for progress
        :returns: List of flow/epe data, normalized.
    """
    if not isinstance(data, Filterable):
        raise AssertionError('data should be a flow/epe data list')
    data.assert_type('flo', 'epe')
    if data.get_type() == 'flo':
        return data._add_filter(NormalizeFlowVideo(data, clamp_pct, gamma, verbose))
    else:
        return data._add_filter(NormalizeEPEVideo(data, clamp_pct, gamma, verbose))


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


def epe_to_rgb(epe, color=[255, 255, 0]):
    """
        Convert EPE data into RGB data, where brighter color means higher EPE
        :param epe: List of EPE data, see fv.endpoint_error(...)
        :param color: Brightest color to set in the image
        :returns: List of RGB data
    """
    return EPEToRGB(epe, color)


def split_uv(flow, channel='u', data_type='ndarray', ignore_rgb_warning=False):
    """
        Split flow data into u, v channels (horizontal/vertical movement)
        :param flow: List of flow data, see fv.input.flo(...)
        :param channel: U for horizontal flow, V for vertical
        :param data_type: ndarray (raw), flo or rgb data.
                          Either 1 channel (ndarray), 2 channels with the other set to 0 (flo),
                          or 3 channels as RGB grayscale data (rgb)
                          Important note: If you use rgb, you must also normalize
                          the flow data (see fv.normalize_frame(...) or fv.normalize_video(...))
        :param ignore_rgb_warning: Ignore the important note about using rgb data_type
        :returns: List of modified data, according to channel and data_type
    """
    return SplitUV(flow, channel, data_type, ignore_rgb_warning)


"""
    Operators
"""


def draw_rectangle(image, rect, color=[255, 0, 0], figure_output=False):
    """
        Operator. Given a list of images and rectangles,
        draw each rectangle in each of the images from the image list
        :param image: List of rgb data, see fv.input.rgb(...)
        :param rect: List of rect data, see fv.input.rect(...)
        :param color: [r, g, b] list, color of the rectangle (default: red)
        :param figure_output: Output as a figure instead of RGB image
        :returns: Iterable object with all the images, with each rectangle drawn
    """
    return DrawRectangle(image, rect, color, figure_output)


def draw_points(image, points, color='random', num_trail=1, figure_output=False):
    """
        Operator. Given a list of images and sets of points,
        draw each set of points in each of the images from the image list
        :param image: List of rgb data, see fv.input.rgb(...)
        :param points: List of points data, see fv.input.points(...)
        :param color: [r, g, b] list, color of the points. Can be 'random' so each point
                      is of a random color (consistent between frames, default mode).
        :param num_trail: Draw a line across the N last sets of points
        :param figure_output: Output as a figure instead of RGB image
        :returns: Iterable object with all the images, with each rectangle drawn
    """
    return DrawPoints(image, points, color, num_trail, figure_output)


def draw_flow_arrows(image_data, flow_data, background_attenuation=0,
                     color='flow', flat_colors=False, arrow_min_alpha=1,
                     subsample_ratio=5, ignore_ratio_warning=False):
    """
        Operator. Given a list of images and flow data, draw a visual representation
        of the flow using arrows on top of the image
        :param image_data: List of rgb data, see fv.input.rgb(...)
        :param flow_data: List of flow data, see fv.input.flo(...)
        :param background_attenuation: Fade the background image to black,
                                       0 means normal background, 1 means all black
        :param color: [r, g, b] list, color of the arrows. Can be 'flow' so each arrow
                      is colored according to its direction using this color circle:
                      http://www.quadibloc.com/other/colint.htm
        :param flat_colors: If True, larger arrows are painted in lighter colors,
                            and smaller flow is darker.
        :param arrow_min_alpha: If flat_colors=False, arrows can be transparent
                                if the flow is lower in that zone. This sets the minimum
                                value for the alpha channel (with zero flow), with 0-1 range.
        :param subsample_ratio: For a ratio of N, calculate mean flow in patches of NxN
                                for each arrow drawn.
        :param ignore_ratio_warning: Don't stretch the ratio if it doesn't fit exactly in the image
        :returns: List of images with arrows drawn
    """
    return DrawFlowArrows(image_data, flow_data, background_attenuation,
                          color, flat_colors, arrow_min_alpha,
                          subsample_ratio, ignore_ratio_warning)


def add_flow_rect(rect, flow, interpolate=True, accumulate=True):
    """
        Operator. Given one rectangle and a list of flow data,
        move the rectangle with respect to the flow in that pixel
        for each given flow frame.
        :param rect: Rectangle, 4 element ndarray [x0, y0, x1, y1]
        :param flow: List of flow data, see fv.input.flo(...)
        :param interpolate: Use bilinear interpolation for flow estimation,
                            or approximate using nearest pixel
        :param accumulate: Use True for frame-by-frame flow data,
                           or False for accumulated flow data
        :returns: Iterable object with all the rectangles
    """
    return AddFlowRect(rect, flow, interpolate, accumulate)


def add_flow_points(points, flow, interpolate=True, accumulate=True):
    """
        Operator. Given a list of points (for one frame) and a
        list of flow data, move the points with respect to the flow
        in that pixel for each given flow frame
        :param points: Set of points, [n, 2] ndarray (x, y)
        :param flow: List of flow data, see fv.input.flo(...)
        :param interpolate: Use bilinear interpolation for flow estimation,
                            or approximate using nearest pixel
        :param accumulate: Use True for frame-by-frame flow data,
                           or False for accumulated flow data
        :returns: Iterable object with all the rectangles
    """
    return AddFlowPoints(points, flow, interpolate, accumulate)


def endpoint_error(flow_est, flow_gt):
    """
        Operator. Given estimated flow data and its ground truth,
        calculate Average Endpoint Error for all frames
        :param flow_est: Estimated flow, see fv.input.flo(...)
        :param flow_gt: Flow ground truth, see fv.input.flo(...)
        :returns: Iterable object with EPE per pixel and frame
    """
    return EndPointError(flow_est, flow_gt)


def track_from_first(point_data, image_data, color='random', draw_lines=True, vertical=False, figure_output=False):
    """
        Operator. Given a set of points and image data, track the set
        of points to see if they track the image's features correctly
        :param point_data: List of points data, see fv.input.points(...)
        :param image_data: List of rgb data, see fv.input.rgb(...)
        :param color: [r, g, b] list, color of the points. Can be 'random' so each point
                      is of a random color (consistent between frames, default mode).
        :param vertical: False for horizontal side-by-side, True for vertical
        :param figure_output: Output as a figure instead of RGB image
        :returns: List of images with features' correspondences
    """
    return TrackFromFirst(point_data, image_data, color, draw_lines, vertical, figure_output)


def synthesize_image(image, accum_flow_data):
    """
        Operator. Given an initial image and accumulated flow,
        generate synthesized images moving the pixels according to the flow
        :param image: Image, ndarray with [height, width, 3] RGB shape
        :param accum_flow_data: List of accumulated flow, see fv.accumulate(...)
        :returns: List of synthesized images from the first one
    """
    # TODO remove when finished
    raise NotImplementedError("synthesize_image hasn't been finished yet.")
    # return SynthesizeImage(image, accum_flow_data)
