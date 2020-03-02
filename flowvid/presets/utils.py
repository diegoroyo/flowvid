import random
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


def ask_for_points(image):
    # Ask for options
    point_type = ask_multichoice('Point generation method ({s}): ',
                                 answer_map={'random': 'random', 'interactive': 'interactive'}, default='random')
    n_points = int(ask_string('Number of points ({s}): ', default='5'))

    # Generate points
    if point_type == 'random':
        [h, w] = image.shape[0:2]
        points = np.reshape([[random.randrange(0, w - 1), random.randrange(0, h - 1)]
                             for i in range(n_points)], (n_points, 2))
        points = fv.input.points(points)
    elif point_type == 'interactive':
        points = fv.input.prompt_points(n_points, image)

    return points


def ask_video_or_figure(video_name):
    out_type = ask_multichoice('Output type ({s}): ',
                               answer_map={'video': 'video', 'pyplot': 'figure'}, default='video')
    if out_type == 'video':
        # Output video options
        framerate = int(ask_string('Video framerate ({s}): ', default='24'))
        out_name = ask_string(
            'Output video name ({s}): ', default=video_name)
        return False, (framerate, out_name)
    elif out_type == 'figure':
        # Output plot option
        framerate = int(ask_string('Video framerate ({s}): ', default='10'))
        return True, (framerate)
