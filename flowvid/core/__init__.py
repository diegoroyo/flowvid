import numpy as np
# from flowvid.input.trackpoints import TrackRectangles
from flowvid.core.filterable import Filterable
from flowvid.core.filters.normalizeflow import NormalizeFrame, NormalizeVideo
from flowvid.core.filters.flowtorgb import FlowToRGB
from flowvid.core.operators.addflowrect import AddFlowRect
from flowvid.core.operators.drawrectangle import DrawRectangle


"""
    Filters
"""


def normalize_frame(flow):
    if not isinstance(flow, Filterable):
        raise AssertionError('TODO')
    return flow._add_filter(NormalizeFrame())


def normalize_video(flow, clamp_pct=1.0, gamma=1.0):
    if not isinstance(flow, Filterable):
        raise AssertionError('TODO')
    if clamp_pct < 0.0 or clamp_pct > 1.0:
        raise AssertionError('TODO')
    return flow._add_filter(NormalizeVideo(flow, clamp_pct, gamma))


def flow_to_rgb(flow):
    if not isinstance(flow, Filterable):
        raise AssertionError('TODO')
    return flow._add_filter(FlowToRGB())


"""
    Operators
"""


def draw_rectangle(image_data, rect_data, color=[255, 0, 0]):
    # if not isinstance(image, np.ndarray):
    #     raise AssertionError('TODO')
    # if not isinstance(rect_data, TrackRectangles):
    #     raise AssertionError('TODO')
    return DrawRectangle(image_data, rect_data, color)


def add_flow_rect(rect, flow_data):
    if not isinstance(rect, np.ndarray):
        raise AssertionError('TODO')
    if not isinstance(flow_data, Filterable):
        raise AssertionError('TODO')
    return AddFlowRect(rect, flow_data)
