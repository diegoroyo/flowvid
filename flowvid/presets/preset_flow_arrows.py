from .utils import get_arg, ask_string, ask_multichoice, ask_video_or_figure
import numpy as np
import flowvid as fv


def preset_flow_arrows(kwargs):
    # Flow files and RGB frames of video
    flo_dir = get_arg(kwargs, 'flo_dir',
                      lambda: ask_string('Flow files directory ({s}): ', default='flo', is_path=True))

    # Background settings
    use_flow = get_arg(kwargs, 'use_flow_colors',
                       lambda: ask_multichoice('Use flow colors for image? ({s}): ',
                                               answer_map={'y': True, 'n': False}, default='n'))
    if use_flow:
        arrow_color = [0, 0, 0]
    else:
        arrow_color = 'flow'
        rgb_dir = get_arg(kwargs, 'image_dir',
                          lambda: ask_string('Image directory ({s}): ', default='png', is_path=True))

    # Arrow subsampling
    subsample_ratio = get_arg(kwargs, 'subsample_ratio',
                              lambda: float(ask_string('Flow subsample ratio ({s}): ', default='16.0')))

    # Output options
    out_figure, out_options = ask_video_or_figure(
        kwargs, 'output_flow_arrows.mp4')

    # Add points and generate image
    flo_data = fv.input.flo(flo_dir)
    if use_flow:
        flo_data_norm = fv.normalize_frame(flo_data)
        rgb_data = fv.flow_to_rgb(flo_data_norm)
        background_attenuation = 0.0
        flat_colors = True
        arrow_color = [0, 0, 0]
    else:
        rgb_data = fv.input.rgb(rgb_dir)
        background_attenuation = 0.4
        flat_colors = False
        arrow_color = 'flow'

    arrow_data = fv.draw_flow_arrows(
        rgb_data, flo_data, background_attenuation=background_attenuation,
        color=arrow_color, flat_colors=flat_colors, arrow_min_alpha=0.7,
        subsample_ratio=subsample_ratio, ignore_ratio_warning=False)

    # Generate output
    if out_figure:
        (framerate) = out_options
        out = fv.output.show_plot(
            title='color_flow result', framerate=framerate)
        out.show_all(arrow_data, show_count=True)
    else:
        (framerate, out_name) = out_options
        out = fv.output.video(out_name, framerate=framerate)
        out.add_all(arrow_data, verbose=True)
