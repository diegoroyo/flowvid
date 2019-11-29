import os
import re
import numpy as np


TAG_FLOAT = 202021.25


class FloDataIterator:
    def __init__(self, flodata):
        self._iter = iter(flodata.source)

    def __next__(self):
        file_name = next(self._iter)
        return self.__read_flow(file_name)

    @classmethod
    def __read_flow(self, file_path):
        """
            TODO
        """
        with open(file_path, 'rb') as file:
            tag = np.frombuffer(file.read(4), dtype=np.float32, count=1)[0]
            if not tag == TAG_FLOAT:
                raise AssertionError(
                    'File {f} has wrong tag ({t})'.format(f=file_path, t=tag))

            [width, height] = np.frombuffer(
                file.read(8), dtype=np.int32, count=2)

            dimensions = 2  # u (horizontal) and v (vertical)
            items = width * height * dimensions

            # read flow values from file
            flow = np.frombuffer(file.read(4 * items),
                                 dtype=np.float32, count=items)
            flow = np.resize(flow, (height, width, dimensions))

        return flow


class FloData:

    def __init__(self, source):
        # .flo file source
        if os.path.isfile(source):
            self.source = list(source)
        elif os.path.isdir(source):
            self.source = (self.__list_directory(source))[0:1]
        else:
            raise AssertionError('Source does not exist')

    @classmethod
    def from_file(cls, file_name):
        return cls(file_name)

    @classmethod
    def from_directory(cls, dir_name):
        return cls(dir_name)

    def __iter__(self):
        return FloDataIterator(self)

    @classmethod
    def __list_directory(self, directory):
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

        return [file_tuple[1] for file_tuple in file_list]
