from .utils import get_arg, ask_string, ask_for_points, ask_video_or_figure
import flowvid as fv


def preset_track_points(kwargs):
    # Flow files and RGB frames of video
    flo_dir = get_arg(kwargs, 'flo_dir',
                      lambda: ask_string('Flow files directory ({s}): ', default='flo', is_path=True))
    rgb_dir = get_arg(kwargs, 'image_dir',
                      lambda: ask_string('Image directory ({s}): ', default='png', is_path=True))

    # Output options
    out_figure, out_options = ask_video_or_figure(
        kwargs, 'output_track_points.mp4')

    # Add points and generate image
    flo_data = fv.input.flo(flo_dir)
    rgb_data = fv.input.rgb(rgb_dir)
    points = ask_for_points(kwargs, rgb_data[0])
    points = fv.add_flow_points(
        points[0], flo_data, interpolate=True, accumulate=True)
    image_data = fv.draw_points(
        rgb_data, points, color='random', num_trail=4, figure_output=out_figure)

    # Generate output
    if out_figure:
        (framerate) = out_options
        out = fv.output.show_plot(
            title='track_points result', framerate=framerate)
        out.show_all(image_data, show_count=True)
    else:
        (framerate, out_name) = out_options
        out = fv.output.video(out_name, framerate=framerate)
        out.add_all(image_data, verbose=True)
