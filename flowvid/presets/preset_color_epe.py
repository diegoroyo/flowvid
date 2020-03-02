from .utils import ask_string, ask_multichoice, ask_video_or_figure
import numpy as np
import flowvid as fv


def preset_color_epe():
    # Flow directories
    flo_est_dir = ask_string(
        'Estimated flow files directory ({s}): ', default='flo_est')
    flo_gt_dir = ask_string(
        'Ground truth flow files directory ({s}): ', default='flo_gt')

    # Flow normalization
    norm_type = ask_multichoice('EPE normalization type ({s}): ',
                                answer_map={'video': 'video', 'frame': 'frame', 'none': None}, default='frame')
    if norm_type == 'video':
        clamp_pct = float(ask_string(
            'Normalization clamp percentage ({s}): ', default='1.0'))
        gamma = float(ask_string(
            'Normalization gamma curve exponent ({s}): ', default='1.0'))

    # Output options
    out_figure, out_options = ask_video_or_figure('output_color_epe.mp4')

    # Generate EPE data
    flo_est = fv.input.flo(flo_est_dir)
    flo_gt = fv.input.flo(flo_gt_dir)
    epe_data = fv.endpoint_error(flo_est, flo_gt)

    # Normalize EPE data and convert to image
    if norm_type == 'frame':
        epe_data = fv.normalize_frame(epe_data)
    elif norm_type == 'video':
        epe_data = fv.normalize_video(
            epe_data, clamp_pct=clamp_pct, gamma=gamma, verbose=True)
    image_data = fv.epe_to_rgb(epe_data, color=[255, 255, 255])

    # Generate output
    if out_figure:
        (framerate) = out_options
        out = fv.output.show_plot(
            title='epe_video result', framerate=framerate)
        out.show_all(image_data, show_count=True)
    else:
        (framerate, out_name) = out_options
        out = fv.output.video(out_name, framerate=framerate)
        out.add_all(image_data, verbose=True)
