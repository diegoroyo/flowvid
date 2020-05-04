import datetime
import random
import os
import yaml
import numpy as np
import flowvid as fv


def get_arg(kwargs, arg_name, fallback_prompt=None):
    if arg_name in kwargs.keys() and kwargs[arg_name] is not None:
        return kwargs[arg_name]
    elif fallback_prompt is not None:
        print('[--{n}] '.format(n=arg_name.replace('_', '-')), end='')
        option = fallback_prompt()
        kwargs[arg_name] = option
        return option
    else:
        raise AssertionError(
            'No default argument given for {n}'.format(n=arg_name))


def ask_string(format_prompt, default, is_path=False):
    answer = input(format_prompt.format(s='default: ' + default))
    answer = answer or default

    if is_path and not answer.startswith('/'):
        answer = os.path.join(os.getcwd(), answer)

    return answer


def ask_multichoice(format_prompt, answer_map, default):
    keys = map(lambda a: '['+a+']' if a == default else a, answer_map.keys())
    answer = input(format_prompt.format(s=', '.join(keys)))
    if answer in answer_map:
        return answer_map[answer]
    else:
        if answer:
            print('  \'{s}\' didn\'t match any of the options, going with default \'{d}\''.format(
                s=answer, d=default))
        return answer_map[default]


def ask_for_points(kwargs, image):
    # Ask for options
    point_type = get_arg(kwargs, 'points_generation',
                         lambda: ask_multichoice('Point generation method ({s}): ',
                                                 answer_map={'random': 'random', 'interactive': 'interactive'}, default='random'))
    n_points = get_arg(kwargs, 'points_number',
                       lambda: int(ask_string('Number of points ({s}): ', default='5')))

    # Generate points
    if point_type == 'random':
        [h, w] = image.shape[0:2]
        points = np.reshape([[random.randrange(0, w - 1), random.randrange(0, h - 1)]
                             for i in range(n_points)], (n_points, 2))
        points = fv.input.points(points)
    elif point_type == 'interactive':
        points = fv.input.prompt_points(n_points, image)

    return points


def ask_video_or_figure(kwargs, video_name):
    out_type = get_arg(kwargs, 'output_type',
                       lambda: ask_multichoice('Output type ({s}): ',
                                               answer_map={'video': 'video', 'pyplot': 'pyplot'}, default='video'))
    if out_type == 'video':
        # Output video options
        framerate = get_arg(kwargs, 'output_framerate',
                            lambda: int(ask_string('Video framerate ({s}): ', default='24')))
        out_name = get_arg(kwargs, 'output_filename',
                           lambda: ask_string('Output video name ({s}): ', default=video_name))
        return False, (framerate, out_name)
    elif out_type == 'pyplot':
        # Output plot option
        framerate = get_arg(kwargs, 'output_framerate',
                            lambda: int(ask_string('Video framerate ({s}): ', default='10')))
        return True, (framerate)
    else:
        raise AssertionError('Invalid output type: {s}'.format(s=out_type))


def load_config(config_filename):
    if config_filename is None:
        return None

    with open(config_filename, 'r') as config_file:
        try:
            return yaml.safe_load(config_file)
        except yaml.YAMLError as exc:
            print('An error ocurred when parsing config file ({f}):'.format(
                f=config_filename))
            print('This configuration will be unused.')
            print(exc)

    return None


def save_config(kwargs, preset_name):
    should_save = ask_multichoice('Save configuration in a file? ({s}): ',
                                  answer_map={'y': True, 'n': False}, default='n')

    if not should_save:
        return

    config_filename = ask_string('Output configuration filename ({s}): ',
                                 default='preset_{p}.yaml'.format(p=preset_name))

    kwargs.pop('config')
    kwargs.pop('preset')

    with open(config_filename, 'w+') as f:
        f.write('# flowvid v{v} configuration file: https://pypi.org/project/flowvid/\n'.format(
                v=fv.__version__))
        f.write('# Created on {d} for preset {p}\n'.format(
                d=datetime.datetime.now(), p=preset_name))
        f.write('#\n')
        f.write('# You can edit/delete this file, as you like\n')
        f.write('# Usage: python3 -m flowvid {p} --config {f}\n'.format(
                p=preset_name, f=config_filename))
        f.write('\n')
        f.write(yaml.dump(kwargs))

    print('')
    print('Saved configuration file in {f}'.format(
        f=os.path.join(os.getcwd(), config_filename)))
