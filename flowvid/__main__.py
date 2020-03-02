import sys
import argparse
import numpy as np
import flowvid as fv

from .presets.preset_color_flow import preset_color_flow
from .presets.preset_color_epe import preset_color_epe
from .presets.preset_plot_epe import preset_plot_epe
from .presets.preset_track_points import preset_track_points
from .presets.preset_track_side_by_side import preset_track_side_by_side

parser = argparse.ArgumentParser(prog='flowvid',
                                 description='Generate an optical flow visualization using the available presets.')
parser.add_argument('preset', type=str, nargs=1,
                    help='Preset, one of: (color_flow, color_epe, plot_epe, track_points, track_side_by_side)')

args = parser.parse_args()

video_type = args.preset[0]
presets = {'color_flow': preset_color_flow,
           'color_epe': preset_color_epe,
           'plot_epe': preset_plot_epe,
           'track_points': preset_track_points,
           'track_side_by_side': preset_track_side_by_side}

if video_type in presets:
    presets[video_type]()
else:
    parser.print_help()
