from .video_output import VideoOutput
from .image_output import ImageOutput
from .flo_output import FloOutput
from .plot_show import PlotShow


def video(path: str, framerate: float = 24, ignore_plot_warning: bool = False):
    """
        Video output generator
        :param path: Where to save the video
        :param framerate: Video's FPS
        :param ignore_plot_warning: Disable the warning given when you try to use this
                                    at the same time as other matplotlib plots.
        :returns: Video saver (see add_frame or add_all)
    """
    return VideoOutput(path, framerate, ignore_plot_warning)


def images(dir_path: str, name_format: str = '{:04}.png', first_id: int = 0):
    """
        Image sequence output generator
        :param dir_path: Directory to save the images
        :param name_format: Filename format
        :param first_id: First ID to apply to name_format
        :returns: Image saver (see save_image or save_all)
    """
    return ImageOutput(dir_path, name_format, first_id)


def flo(dir_path: str, name_format: str = '{:04}.flo', first_id: int = 0):
    """
        Flow file sequence output generator. Using Middlebury format:
        http://vision.middlebury.edu/flow/code/flow-code/README.txt
        :param dir_path: Directory to save the flow files
        :param name_format: Filename format
        :param first_id: First ID to apply to name_format
        :returns: Flow file saver (see save_file or save_all)
    """
    return FloOutput(dir_path, name_format, first_id)


def show_plot(title: str = '', framerate: float = 10, ignore_plot_warning: bool = False):
    """
        Show the given images in an interactive pyplot plot
        :param title: Plot title to show
        :param framerate: Frames per seconds shown in animated plot
                          (must be bigger than 0)
        :param ignore_plot_warning: Disable the warning given when you try to use this
                                    at the same time as other matplotlib plots.
        :returns: Image show object (see show or show_all)
    """
    return PlotShow(title, framerate, ignore_plot_warning)
