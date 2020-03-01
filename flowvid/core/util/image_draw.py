import numpy as np


_random_colors = [(1.0, 1.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0), (0.0, 1.0, 1.0, 1.0),
                  (1.0, 0.0, 0.0, 1.0), (1.0, 1.0, 0.0, 1.0), (0.8, 0.8, 0.8, 1.0),
                  (0.0, 0.0, 0.8, 1.0), (0.0, 0.0, 0.6, 1.0), (0.6, 0.6, 0.6, 1.0),
                  (0.6, 0.0, 0.0, 1.0), (0.8, 0.0, 0.0, 1.0), (0.0, 0.8, 0.8, 1.0)]


def get_color(color, i, normalize=False):
    if color == 'random':
        color = _random_colors[i % len(_random_colors)]
        if not normalize:
            color = (color[0] * 255.0, color[1] * 255.0, color[2] * 255.0)
    return color


def draw_points(image, points, color, cross=True):
    """
        :param image: [h, w, 3] rgb data
        :param points: [n, 2] ndarray (x, y)
        :returns: image with modified RGB such that points are drawn with color
                  Note: if color == 'random', a different color is chosen for
                  each point (but each color is consistent between frames)
    """
    # Clamping
    [h, w] = image.shape[0:2]
    points = points.astype(int)
    points[:, 0] = np.clip(points[:, 0], 1, w - 2)
    points[:, 1] = np.clip(points[:, 1], 1, h - 2)

    # Drawing
    for i, [px, py] in enumerate(points):
        # Get color
        point_color = get_color(color, i)
        # Draw point as a small cross
        image[py, px, :] = point_color
        if cross:
            # no need to check for bounds
            image[py, px - 1, :] = point_color
            image[py, px + 1, :] = point_color
            image[py - 1, px, :] = point_color
            image[py + 1, px, :] = point_color

    return image


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
