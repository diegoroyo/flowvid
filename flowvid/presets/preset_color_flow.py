from .utils import get_arg, ask_string, ask_multichoice, ask_video_or_figure
import flowvid as fv


def preset_color_flow(kwargs):
    # Flow files
    flo_dir = get_arg(kwargs, 'flo_dir',
                      lambda: ask_string('Flow files directory ({s}): ', default='flo', is_path=True))

    # Flow normalization
    norm_type = get_arg(kwargs, 'norm_type',
                        lambda: ask_multichoice('Vector normalization type ({s}): ',
                                                answer_map={'video': 'video', 'frame': 'frame', 'none': 'none'}, default='frame'))
    if norm_type == 'video':
        clamp_pct = get_arg(kwargs, 'norm_clamp', lambda: float(ask_string(
            'Normalization clamp percentage ({s}): ', default='1.0')))
        gamma = get_arg(kwargs, 'norm_gamma', lambda: float(ask_string(
            'Normalization gamma curve exponent ({s}): ', default='1.0')))

    # Output options
    out_figure, out_options = ask_video_or_figure(
        kwargs, 'output_color_flow.mp4')

    # Read flow data and normalize
    flo_data = fv.input.flo(flo_dir)
    if norm_type == 'frame':
        flo_data = fv.normalize_frame(flo_data)
    elif norm_type == 'video':
        flo_data = fv.normalize_video(
            flo_data, clamp_pct=clamp_pct, gamma=gamma, verbose=True)
    rgb_data = fv.flow_to_rgb(flo_data)

    # Generate output
    if out_figure:
        (framerate) = out_options
        out = fv.output.show_plot(
            title='color_flow result', framerate=framerate)
        out.show_all(rgb_data, show_count=True)
    else:
        (framerate, out_name) = out_options
        out = fv.output.video(out_name, framerate=framerate)
        out.add_all(rgb_data, verbose=True)
