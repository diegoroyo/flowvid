import numpy as np
import os
import re

TAG_FLOAT = 202021.25


def read_flow(file_path):
    """
        TODO
    """
    with open(file_path, 'rb') as file:
        tag = np.frombuffer(file.read(4), dtype=np.float32, count=1)[0]
        if not tag == TAG_FLOAT:
            raise AssertionError(
                'File {f} has wrong tag ({t})'.format(f=file_path, t=tag))

        [width, height] = np.frombuffer(file.read(8), dtype=np.int32, count=2)

        dimensions = 2  # u (horizontal) and v (vertical)
        items = width * height * dimensions

        # read flow values from file
        flow = np.frombuffer(file.read(4 * items),
                             dtype=np.float32, count=items)
        flow = np.resize(flow, (height, width, dimensions))

    return flow


def read_flow_directory(directory):
    """
        TODO
    """
    pattern = re.compile(r'\d+')
    name_list = [f for f in os.listdir(directory) if f.endswith('.flo')]
    file_list = []  # (index, name) tuples

    if not name_list:
        raise AssertionError(
            'There are no .flo files in directory {d}'.format(d=directory))

    for name in name_list:
        match = pattern.match(name)
        if match is not None:
            file_index = match[0]
            file_path = os.path.join(directory, name)
            file_list.append((file_index, file_path))
    file_list = sorted(file_list, key=lambda tuple: tuple[0])

    flows = np.array([read_flow(item[1]) for item in file_list])

    return flows
