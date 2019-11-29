import sys
import numpy as np
from flowvid.input.flodata import FloData
from flowvid.filter.normalize import Filter, NormalizeFrame, NormalizeVideo
from flowvid.filter.flotorgb import FloToRGB
from flowvid.output.videooutput import VideoOutput


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


video_type = sys.argv[1] if len(sys.argv) > 0 else ''
if video_type == 'color':
    flo_dir = ask_string('Flow files directory ({s}): ', default='flo')
    norm_type = ask_multichoice('Vector normalize type ({s}): ',
                                answer_map={'video': 'video', 'frame': 'frame', 'none': None}, default='frame')
    framerate = int(ask_string('Video framerate ({s}): ', default='24'))
    out_name = ask_string(
        'Output video name ({s}): ', default='output_flo.mp4')

    flodata = FloData.from_directory(flo_dir)
    datafilter = Filter()
    if norm_type == 'frame':
        datafilter = NormalizeFrame()
    elif norm_type == 'video':
        datafilter = NormalizeVideo(flodata, clamp_pct=0.8, gamma=0.7)
    out = VideoOutput(filename=out_name, framerate=framerate)
    rgbfilter = FloToRGB()
    for i, flow in enumerate(flodata):
        normflow = datafilter.apply(flow)
        rgb = rgbfilter.apply(normflow)
        out.add_frame(rgb)
    out.close()
else:
    print('Need parameter: {{ color | add }}'.format(p=sys.argv[0]))
