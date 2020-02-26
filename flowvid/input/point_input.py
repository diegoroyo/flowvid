from matplotlib import pyplot as plt
import numpy as np


def pyplot_prompt(n, background):
    """
        Show a pyplot prompt with the given background and
        return a [n, 2] ndarray with all the points selected
    """
    if isinstance(background, tuple):
        (h, w) = background
        background = np.zeros((h, w, 3))
    elif not (isinstance(background, np.ndarray) and background.ndim == 3 and background.shape[2] == 3):
        raise AssertionError(
            'background must be either a (height, width) tuple or a (height, width, 3) image ndarray')
    plt.imshow(background)
    plt.title('Select {n} points from the image'.format(n=n))
    points = plt.ginput(n=n)
    plt.close()
    return np.array(points)
