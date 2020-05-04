import sys
import argparse
import textwrap
import numpy as np

from .presets.preset_color_flow import preset_color_flow
from .presets.preset_color_epe import preset_color_epe
from .presets.preset_flow_arrows import preset_flow_arrows
from .presets.preset_plot_epe import preset_plot_epe
from .presets.preset_track_points import preset_track_points
from .presets.preset_track_side_by_side import preset_track_side_by_side
from .presets.utils import load_config, save_config

description = textwrap.dedent(
    '''\
    Generate an optical flow visualization using the available presets.

    Preset can be one of:
    * color_flow: Convert flow data to RGB using the Middlebury representation
    * color_epe: Calculate endpoint error and generate a video representation
    * flow_arrows: Draw arrows representing optical flow over a video
    * plot_epe: Generate a pyplot plot with the EPE distribution in all frames
    * track_points: Place points in a image and see how flow moves them
    * track_side_by_side: Place points in a image and see how flow can track them
    '''
)

parser = argparse.ArgumentParser(prog='flowvid',
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description=description)

# Preset / configuration
group_config = parser.add_argument_group('configuration')
group_config.add_argument('preset', type=str, metavar='<preset>',
                          help='Video preset, see above')
group_config.add_argument('-c', '--config', type=str, required=False, metavar='<path/to/config/file.yaml>',
                          help='Preset configuration file in YAML format')

# Input
group_input = parser.add_argument_group('input')
group_input.add_argument('--flo-dir', type=str, required=False, metavar='<path/to/flo/dir>',
                         help='Directory to look for .flo files')
group_input.add_argument('--flo-gt-dir', type=str, required=False, metavar='<path/to/flo-gt/dir>',
                         help='Directory to look for .flo GROUND TRUTH files')

group_input.add_argument('--image-dir', type=str, required=False, metavar='<path/to/image/dir>',
                         help='Directory to look for image files')

# Core / main processing
group_core = parser.add_argument_group('processing')
group_core.add_argument('--norm-type', type=str, choices=('video', 'frame'), required=False,
                        help='Normalize flow to 0-1 range using frame\'s maximum or video\'s')
group_core.add_argument('--norm-clamp', type=float, required=False, metavar='[0.0..1.0]',
                        help='Clamp percentage (0-1) when applying clamp-gamma curve in video normalization')
group_core.add_argument('--norm-gamma', type=float, required=False, metavar='[0.0..]',
                        help='Gamma factor (>0) when applying clamp-gamma curve in video normalization')

group_core.add_argument('--plot-cumulative', type=str, choices=('y', 'n'), required=False,
                        help='Use cumulative data for the given plot')
group_core.add_argument('--plot-normalize', type=str, choices=('y', 'n'), required=False,
                        help='Normalize data to 0-1 range for the given plot')

group_core.add_argument('--points-generation', type=str, choices=('random', 'interactive'), required=False,
                        help='Use user input to generate points or choose random ones')
group_core.add_argument('--points-number', type=int, required=False, metavar='[0..]',
                        help='Number of points to generate and use in the visualization')

group_core.add_argument('--use-flow-colors', type=str, choices=('y', 'n'), required=False,
                        help='Use flow colors for background instead of image data')
group_core.add_argument('--subsample-ratio', type=float, required=False, metavar='[0.0..]',
                        help='Do the mean in a square of given size in pixels')

# Output
group_output = parser.add_argument_group('output')
group_output.add_argument('--output-type', type=str, choices=('video', 'pyplot'), required=False,
                          help='Save video file or show interactive pyplot window')
group_output.add_argument('--output-framerate', type=int, required=False, metavar='<fps>',
                          help='Frames per second for the specified output type')
group_output.add_argument('--output-filename', type=str, required=False, metavar='<path/to/video.mp4>',
                          help='Filename generated for video output type')

# parsing
args = parser.parse_args()
video_type = args.preset

# validate preset from args
presets = {'color_flow': preset_color_flow,
           'color_epe': preset_color_epe,
           'flow_arrows': preset_flow_arrows,
           'plot_epe': preset_plot_epe,
           'track_points': preset_track_points,
           'track_side_by_side': preset_track_side_by_side}
if video_type not in presets:
    print(description)
    exit(1)

# try to load config from file
config = load_config(args.config)
if config is None:
    config = vars(args)
    config_from_file = False
else:
    config_from_file = True

# execute and save
try:
    presets[video_type](config)
except Exception as exc:
    print('')
    print('/!\ An error ocurred:')
    print('>', exc)
    print('Your current configuration can be saved, edited and later loaded with --config <config-file>')
    print('')

if not config_from_file:
    save_config(config, video_type)
