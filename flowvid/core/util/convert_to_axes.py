import matplotlib.pyplot as plt
from matplotlib.axes import Axes


def convert_to_axes(image):
    """ image should be an Axes or rgb ndarray """
    if isinstance(image, Axes):
        return image
    else:
        ax = plt.axes()
        ax.imshow(image)
        return ax
