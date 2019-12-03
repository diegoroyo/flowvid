from .video_output import VideoOutput
from .image_output import ImageOutput
import os


def video(path, framerate=24):
    return VideoOutput(path, framerate)


def images(dir_path, name_format="{:04}.png", first_id=0):
    return ImageOutput(dir_path, name_format, first_id)
