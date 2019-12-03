import sys
import numpy as np
import flowvid as fv


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

    flo_data = fv.input.flo(flo_dir)
    if norm_type == 'frame':
        flo_data = fv.normalize_frame(flo_data)
    elif norm_type == 'video':
        flo_data = fv.normalize_video(flo_data, clamp_pct=0.8, gamma=0.7)
    rgb_data = fv.flow_to_rgb(flo_data)

    out = fv.output.video(out_name, framerate=framerate)
    out.add_all(rgb_data, verbose=True)

elif video_type == 'add':

    # ask_string('Flow files directory ({s}): ', default='flo')
    flo_dir = 'test/flo'
    image = 'test/png/0000.png'
    n = 10
    framerate = 1
    out_name = 'output.mp4'

    flo_data = fv.input.flo(flo_dir, dir_first=0, dir_total=n)
    image = fv.input.rgb(image)[0]
    # addoperator = AddFlow(imdata.shape[0:2])
    out = fv.output.video(out_name, framerate=framerate)
    # synth_image = fv.add_flow_image(image, flo_data)
    # out.add_all(synth_image)

elif video_type == 'rectangle_truth':

    # ask_string('Flow files directory ({s}): ', default='flo')
    flo_dir = 'test/flo'
    png_dir = 'test/png'
    track = 'test/track/video10_annot.txt'
    framerate = 8
    out_name = 'output_truth.mp4'

    rgb_data = fv.input.rgb(png_dir, dir_total=600)
    rect_data = fv.input.rect(track, rect_format='x0 y0 xw yw')
    # drawrec = DrawRectangle()
    rgb_rect = fv.draw_rectangle(rgb_data, rect_data, color=[0, 255, 0])

    out = fv.output.video(out_name, framerate=framerate)
    out.add_all(rgb_rect, verbose=True)

elif video_type == 'rectangle_flo':

    # ask_string('Flow files directory ({s}): ', default='flo')
    flo_dir = 'test/flo/video9'
    png_dir = 'test/png/video9'
    track = 'test/track/video9_annot.txt'
    framerate = 8
    out_name = 'output_flo.mp4'

    rgb_data = fv.input.rgb(png_dir, dir_first=0, dir_total=75)
    flo_data = fv.input.flo(flo_dir, dir_first=0, dir_total=75)
    track_data = fv.input.rect(
        track, rect_format='x0 y0 xw yw', elem_first=0, elem_total=75)
    first_rect = track_data[0]

    rgb_truth = fv.draw_rectangle(rgb_data, track_data, color=[0, 255, 0])
    flo_rect = fv.add_flow_rect(first_rect, flo_data)
    image_both = fv.draw_rectangle(rgb_truth, flo_rect, color=[0, 0, 255])

    out = fv.output.video(out_name, framerate=framerate)
    out.add_all(image_both)

else:
    print('Need parameter: {{ color | add | rectangle_truth | rectangle_flo }}'.format(
        p=sys.argv[0]))
