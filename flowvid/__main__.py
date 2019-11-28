import argparse

from flowvid.readflow import read_flow_directory
from flowvid.flowconversion import flows_to_colors

# TODO help
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--flo', nargs=1, type=str, required=True)
parser.add_argument('-b', '--base', nargs=1, choices=['color_frame', 'color_video'], default='color_video')
parser.add_argument('-r', '--framerate', nargs=1, default=24, type=float)
parser.add_argument('-o', '--output', nargs=1, type=str, default='video.mp4')

args = parser.parse_args()

flow = read_flow_directory(args.flo[0])

norm_type = None
if args.base[0] == 'color_frame':
    norm_type = 'frame'
elif args.base[0] == 'color_video':
    norm_type = 'video'

flows_to_colors(flow, filename=args.output[0], framerate=args.framerate[0], normalize=norm_type)

# from readflow import read_flow, read_flow_directory
# from flowconversion import flows_to_colors
# import numpy as np
# import colorsys
# from matplotlib import pyplot as plt

# flow = read_flow_directory("../test")
# flows_to_colors(flow, framerate=1)

# # flow = read_flow_directory("../test")

# # size = 200
# # colors = np.empty((size, size, 3), dtype=np.uint8)
# # for i in range(0, size):
# #     for j in range(0, size):
# #         u = (i - np.ceil(size / 2)) / np.floor(size / 2)
# #         v = (j - np.ceil(size / 2)) / np.floor(size / 2)
# #         angle = (np.arctan2(v, u) + np.pi) / (2 * np.pi)
# #         module = np.sqrt(u ** 2 + v ** 2)
# #         if module > 1:
# #             module = 1
# #         (r, g, b) = colorsys.hsv_to_rgb(angle, module, 1)
# #         colors[size - j - 1, size - i - 1] = np.array([r * 255, g * 255, b * 255])

# # plt.imshow(colors, interpolation='none')
# # plt.savefig("test.png")