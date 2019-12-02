import sys
import numpy as np
from flowvid.input.flodata import FloData
from flowvid.input.rgbdata import RGBData
from flowvid.input.trackpoints import TrackPoints
from flowvid.filter.basefilter import Filter
from flowvid.filter.normalizeflow import NormalizeFrame, NormalizeVideo
from flowvid.operator.drawrectangle import DrawRectangle
from flowvid.operator.baseoperator import Operator
from flowvid.operator.addflow import AddFlow
from flowvid.filter.flowtorgb import FlowToRGB
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
    rgbfilter = FlowToRGB()
    for i, flow in enumerate(flodata):
        print('Frame', i)
        out.add_frame(rgbfilter.apply(datafilter.apply(flow)))

elif video_type == 'add':    

    flo_dir = 'test/flo'#ask_string('Flow files directory ({s}): ', default='flo')
    image = 'test/png/0000.png'
    n = 10
    framerate = 1
    out_name = 'output.mp4'

    flodata = FloData.from_directory(flo_dir, 0, n)
    imdata = next(iter(RGBData.from_file(image)))
    addoperator = AddFlow(imdata.shape[0:2])
    out = VideoOutput(filename=out_name, framerate=framerate)
    out.add_frame(imdata)
    for i, flow in enumerate(flodata):
        print('Frame', i)
        imdata = addoperator.apply(imdata, flow)
        out.add_frame(imdata)

elif video_type == 'rectangle_truth':

    flo_dir = 'test/flo'#ask_string('Flow files directory ({s}): ', default='flo')
    png_dir = 'test/png'
    track = 'test/track/video10_annot.txt'
    framerate = 8
    out_name = 'output_truth.mp4'

    pngdata = RGBData.from_directory(png_dir, num_files=600)
    drawrec = DrawRectangle()
    recdata = TrackPoints.rectangles(track, rec_format='x0 y0 xw yw')

    out = VideoOutput(filename=out_name, framerate=framerate)

    for i, (image, rec) in enumerate(zip(pngdata, recdata)):
        print('Frame', i)
        image = drawrec.apply(image, rec, [0, 255, 0])
        out.add_frame(image)

elif video_type == 'rectangle_flo':

    flo_dir = 'test/flo/video9'#ask_string('Flow files directory ({s}): ', default='flo')
    png_dir = 'test/png/video9'
    track = 'test/track/video9_annot.txt'
    framerate = 8
    out_name = 'output_flo.mp4'

    rgb_data = RGBData.from_directory(png_dir, first=0, num_files=75)
    flo_data = FloData.from_directory(flo_dir, first=0, num_files=75)
    track_data = TrackPoints.rectangles(track, rec_format='x0 y0 xw yw', first=0, num=75)
    first_rec = track_data[0]
    drawrec = DrawRectangle()

    out = VideoOutput(filename=out_name, framerate=framerate)
    for i, (flow, image, truth_rec) in enumerate(zip(flo_data, rgb_data, track_data)):
        print('Frame', i)
        x0 = int(np.clip(first_rec[0], 0, 639))
        y0 = int(np.clip(first_rec[1], 0, 479))
        x1 = int(np.clip(first_rec[2], 0, 639))
        y1 = int(np.clip(first_rec[3], 0, 479))
        add = [flow[y0, x0, 0], flow[y0, x0, 1], flow[y1, x1, 0], flow[y1, x1, 1]]
        first_rec = first_rec + add
        image = drawrec.apply(image, first_rec, [0, 0, 255])
        image = drawrec.apply(image, truth_rec, [0, 255, 0])
        out.add_frame(image)

else:
    print('Need parameter: {{ color | add | rectangle_truth | rectangle_flo }}'.format(p=sys.argv[0]))
