import sys
import argparse
import numpy as np
import flowvid as fv

parser = argparse.ArgumentParser(prog='flowvid',
                                 description='Generate an optical flow visualization using the available presets.')
parser.add_argument('preset', type=str, nargs=1,
                    help='Preset, one of: (color_flow)')

args = parser.parse_args()


def ask_string(format_prompt, default):
    answer = input(format_prompt.format(s='default: ' + default))
    if answer:
        return answer
    else:
        return default


def ask_multichoice(format_prompt, answer_map, default):
    keys = map(lambda a: '['+a+']' if a == default else a, answer_map.keys())
    answer = input(format_prompt.format(s=', '.join(keys)))
    if answer in answer_map:
        return answer_map[answer]
    else:
        return answer_map[default]


video_type = args.preset[0]
if video_type == 'color_flow':

    flo_dir = ask_string('Flow files directory ({s}): ', default='flo')
    norm_type = ask_multichoice('Vector normalize type ({s}): ',
                                answer_map={'video': 'video', 'frame': 'frame', 'none': None}, default='frame')
    if norm_type == 'video':
        clamp_pct = float(ask_string(
            'Normalization clamp percentage ({s}): ', default='1.0'))
        gamma = float(ask_string(
            'Normalization gamma curve exponent ({s}): ', default='1.0'))
    framerate = int(ask_string('Video framerate ({s}): ', default='24'))
    out_name = ask_string(
        'Output video name ({s}): ', default='output_flo.mp4')

    flo_data = fv.input.flo(flo_dir)
    if norm_type == 'frame':
        flo_data = fv.normalize_frame(flo_data)
    elif norm_type == 'video':
        flo_data = fv.normalize_video(
            flo_data, clamp_pct=clamp_pct, gamma=gamma)
    rgb_data = fv.flow_to_rgb(flo_data)

    out = fv.output.video(out_name, framerate=framerate)
    out.add_all(rgb_data, verbose=True)

elif video_type == 'track_points':

    raise NotImplementedError("TODO")

else:
    raise NotImplementedError("Whoops.")