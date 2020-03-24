from .video_output import VideoOutput
from .image_output import ImageOutput
from .flo_output import FloOutput
from .plot_show import PlotShow
import os


def video(path, framerate=24):
    """
        Video output generator
        :param path: Where to save the video
        :param framerate: Video's FPS
        :returns: Video saver (see add_frame or add_all)
    """
    return VideoOutput(path, framerate)


def images(dir_path, name_format="{:04}.png", first_id=0):
    """
        Image sequence output generator
        :param dir_path: Directory to save the images
        :param name_format: Filename format
        :param first_id: First ID to apply to name_format
        :returns: Image saver (see save_image or save_all)
    """
    return ImageOutput(dir_path, name_format, first_id)


def flo(dir_path, name_format="{:04}.flo", first_id=0):
    """
        Flow file sequence output generator. Using Middlebury format:
        http://vision.middlebury.edu/flow/code/flow-code/README.txt
        :param dir_path: Directory to save the flow files
        :param name_format: Filename format
        :param first_id: First ID to apply to name_format
        :returns: Flow file saver (see save_file or save_all)
    """
    return FloOutput(dir_path, name_format, first_id)


def show_plot(title='', framerate=10):
    """
        Show the given images in an interactive pyplot plot
        :param title: Plot title to show
        :param framerate: Frames per seconds shown in animated plot
                          (must be bigger than 0)
        :returns: Image show object (see show or show_all)
    """
    return PlotShow(title, framerate)
