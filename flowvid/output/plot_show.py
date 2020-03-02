import numpy as np
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.widgets import Button
from ..core.filterable import Filterable


class PlotShow:
    """ Show images with pyplot """

    TIME_POLL_PAUSE = 0.1  # seconds

    def __init__(self, plot_title, framerate):
        if framerate <= 0.0:
            raise AssertionError('Framerate should be bigger than 0')
        self._plot_title = plot_title
        self._framerate = framerate
        self._pause_secs = 1.0 / framerate

        self._fig = plt.figure()
        self._fig.canvas.mpl_connect('close_event', self._action_close)

        # Create buttons for playing menu
        axpause = plt.axes([0.5, 0.05, 0.43, 0.075])
        bpause = plt.Button(axpause, 'Pause')
        bpause.on_clicked(self._action_pause)
        self._axpause = axpause

        # Create buttons for paused menu
        axcontinue = plt.axes([0.5, 0.05, 0.1, 0.075])
        axnext = plt.axes([0.61, 0.05, 0.1, 0.075])
        axnext10 = plt.axes([0.72, 0.05, 0.1, 0.075])
        axnext100 = plt.axes([0.83, 0.05, 0.1, 0.075])
        bcontinue = plt.Button(axcontinue, 'Play')
        bcontinue.on_clicked(self._action_continue)
        bnext = plt.Button(axnext, 'Next')
        bnext.on_clicked(self._action_next)
        bnext10 = plt.Button(axnext10, 'Next 10')
        bnext10.on_clicked(self._action_next_10)
        bnext100 = plt.Button(axnext100, 'Next 100')
        bnext100.on_clicked(self._action_next_100)
        self._axcontinue = axcontinue
        self._axnext = axnext
        self._axnext10 = axnext10
        self._axnext100 = axnext100

        # must keep a reference to buttons so they stay responsive
        self._buttons = (bcontinue, bnext, bnext10, bnext100, bpause)

    def _action_pause(self, event):
        self._paused = True
        self._fig.subplots_adjust(bottom=0.2)
        self._fig.add_axes(self._axcontinue)
        self._fig.add_axes(self._axnext)
        self._fig.add_axes(self._axnext10)
        self._fig.add_axes(self._axnext100)
        self._fig.delaxes(self._axpause)

    def _action_continue(self, event):
        self._paused = False
        self._fig.subplots_adjust(bottom=0.2)
        self._fig.delaxes(self._axcontinue)
        self._fig.delaxes(self._axnext)
        self._fig.delaxes(self._axnext10)
        self._fig.delaxes(self._axnext100)
        self._fig.add_axes(self._axpause)

    def _action_next(self, event):
        self._next += 1

    def _action_next_10(self, event):
        self._next += 10

    def _action_next_100(self, event):
        self._next += 100

    def _action_close(self, event):
        self._closed = True

    def _show(self, image, i, n, show_count):
        """
            Show an image using pyplot
            :param image: [h, w, 3] rgb ndarray OR figure
            :param i: Image number
            :param n: Total number of images
            :param show_count: Show progress in title (i of n)
            :param number: Add frame number to title display
                           ({i} of {n}) or None for nothing
        """
        # check for rgb ndarray (rgb type) or axes pyplot object (figure type)
        if isinstance(image, np.ndarray):
            if image.ndim != 3 or image.shape[2] != 3:
                raise AssertionError(
                    'RGB image should be a [h, w, 3] rgb ndarray')
            ax = self._fig.add_subplot()
            ax.imshow(image)
        else:
            ax = image
            if not isinstance(ax, Axes):
                raise AssertionError(
                    'image should be either a figure or RGB ndarray')

        # Figure title
        title = self._plot_title
        if show_count:
            # Add space only if title is present
            title = ' '.join([title, '({i} of {n})'.format(i=i, n=n)])

        # Create figure with title
        ax.set_title(title)
        self._fig.add_axes(ax)

        # Show and wait for event
        self._fig.show()
        while self._paused and self._next == 0 and not self._closed:
            plt.pause(PlotShow.TIME_POLL_PAUSE)
        if self._next > 0:
            self._next -= 1
        elif not self._paused and not self._closed:
            plt.pause(self._pause_secs)

        # Don't delaxe on last image
        if i != n:
            self._fig.delaxes(ax)

    def show_all(self, images, show_count=True):
        """
            Show all images using pyplot
            :param images: List of rgb or figure data
        """
        if not isinstance(images, Filterable):
            raise AssertionError(
                'images should contain a list of figure or rgb data')
        images.assert_type('rgb', 'figure')

        # Prepare figure variables
        self._closed = False  # figure hasn't been closed
        self._action_pause(None)  # not paused, show buttons
        self._next = 0  # next -> # of frames to skip

        # Show all figures in the plot
        n = len(images)
        for i, image in enumerate(images):
            if self._closed:
                break
            self._show(image, i + 1, n, show_count)

        # Wait for figure closed
        while not self._closed:
            plt.pause(PlotShow.TIME_POLL_PAUSE)
