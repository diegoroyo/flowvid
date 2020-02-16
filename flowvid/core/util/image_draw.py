import numpy as np


def draw_line(image, line, color):
    """
        :param image: [h, w, 3] rgb data
        :param line: [2, 2] ndarray ((p0x, p0y), (p1x, p1y)) line between p0-p1
        :param color: [r, g, b] color of the line
        :returns: image with modified RGB such that line is drawn on it
                    Note: if self_color == 'random', a different color is chosen for
                        each line (but each color is consistent between frames)
    """

    # Clamping
    [h, w] = image.shape[0:2]
    line = line.astype(int)
    line[:, 0] = np.clip(line[:, 0], 0, w - 1)
    line[:, 1] = np.clip(line[:, 1], 0, h - 1)
    p0 = line[0, :]
    p1 = line[1, :]
    # Simple line algorithm
    if abs(p1[0] - p0[0]) > abs(p1[1] - p0[1]):
        # X axis is bigger, iterate through it
        if p0[0] > p1[0]:
            p0, p1 = p1, p0
        for lx in range(p0[0], p1[0]):
            y = int(p0[1] + (lx - p0[0]) *
                    (p1[1] - p0[1]) / (p1[0] - p0[0]))
            image[y, lx, :] = color
    else:
        # Y axis is bigger, iterate through it
        if p0[1] > p1[1]:
            p0, p1 = p1, p0
        for ly in range(p0[1], p1[1]):
            x = int(p0[0] + (ly - p0[1]) *
                    (p1[0] - p0[0]) / (p1[1] - p0[1]))
            image[ly, x, :] = color
