import numpy as np
import os
from ..core.filterable import Filterable


class FloOutput:
    """
        Save as flow files sequence with the Middlebury .flo format:
        http://vision.middlebury.edu/flow/code/flow-code/README.txt
    """

    def __init__(self, path, name_format, first_id):
        if not os.path.isdir(path):
            raise AssertionError('{p} is not a directory.'.format(p=path))
        self._path = path
        self._id_template = name_format
        self._next_id = first_id

    TAG_FLOAT = 202021.25

    def save_file(self, flow):
        """
            Save one flow file with the next ID filename
            :param image: [h, w, 2] flow ndarray
        """
        if not isinstance(flow, np.ndarray) or flow.ndim != 3 or flow.shape[2] != 2:
            raise AssertionError(
                'Flow should be a [h, w, 2] flow ndarray with (u, v) components')

        [h, w] = flow.shape[0:2]
        tag = np.array([FloOutput.TAG_FLOAT], dtype=np.float32)
        size = np.array([w, h], dtype=np.int32)
        flow = flow.astype(np.float32)
        filename = os.path.join(
            self._path, self._id_template.format(self._next_id))
        with open(filename, "wb+") as file:
            file.write(tag.tobytes())
            file.write(size.tobytes())
            file.write(flow.tobytes())
        self._next_id = self._next_id + 1

    def save_all(self, flow, verbose=False):
        """
            Save all frames of flow data in files
            :param images: List of flow data
            :param verbose: Show progress bar
        """
        if not isinstance(flow, Filterable):
            raise AssertionError('flow should contain a list of flow data')
        flow.assert_type('flow')

        n = len(flow)
        for i, image in enumerate(flow):
            if verbose:
                print(' File', i + 1, 'of', n, end='\r')  # TODO prettify
            self.save_file(image)
