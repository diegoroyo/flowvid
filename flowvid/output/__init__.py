from .video_output import VideoOutput
from .image_output import ImageOutput
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
