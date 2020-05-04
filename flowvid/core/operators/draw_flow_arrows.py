import matplotlib.pyplot as plt
import numpy as np
import itertools
import math
from ..filterable import Filterable
from ..util.convert_to_axes import convert_to_axes
from ..util.color_flow import flow_to_rgb
from .base_operator import Operator


class DrawFlowArrows(Operator):
    """
        Given a list of images and flow data, draw a visual representation
        of the flow using arrows on top of the image
    """

    def __init__(self, image_data, flow_data, background_attenuation,
                 color, flat_colors, arrow_min_alpha,
                 subsample_ratio, ignore_ratio_warning):
        if not isinstance(image_data, Filterable):
            raise AssertionError(
                'image_data should contain a list of rgb data')
        if not isinstance(flow_data, Filterable):
            raise AssertionError(
                'flow_data should contain a list of flow data')
        if (not isinstance(color, list) or len(color) != 3) and color != 'flow':
            raise AssertionError(
                'color should be a [r, g, b] list where rgb range from 0 to 255, or \'flow\' for flow colors.')
        image_data.assert_type('rgb', 'figure')
        flow_data.assert_type('flo')

        if background_attenuation < 0 or background_attenuation > 1:
            raise AssertionError(
                'background_attenuation should be in 0-1 range but it is {n}.'.format(n=background_attenuation))
        if background_attenuation != 0 and image_data.get_type() != 'rgb':
            raise AssertionError(
                'Can\'t apply background attenuation to non-rgb image data (it is \'{d}\').'.format(d=image_data.get_type()))
        if subsample_ratio < 1:
            raise AssertionError(
                'subsample_ratio should be a positive integer but it is {n}.'.format(n=subsample_ratio))
        if arrow_min_alpha < 0 or arrow_min_alpha > 1:
            raise AssertionError(
                'arrow_min_alpha should be in 0-1 range but it is {n}.'.format(n=arrow_min_alpha))
        Operator.__init__(self)
        self._image_data = image_data
        self._flow_data = flow_data
        self._attenuation = 1.0 - background_attenuation
        self._color = color
        self._flat_colors = flat_colors
        self._arrow_min_alpha = arrow_min_alpha

        [h, w] = flow_data[0].shape[0:2]
        self._subsample_x = subsample_ratio
        self._subsample_y = subsample_ratio
        if (h % subsample_ratio != 0 or w % subsample_ratio != 0) and not ignore_ratio_warning:
            rem_w = (w % subsample_ratio) / (w // subsample_ratio)
            rem_h = (h % subsample_ratio) / (h // subsample_ratio)
            self._subsample_x = subsample_ratio + rem_w
            self._subsample_y = subsample_ratio + rem_h
            print('Warning: subsample_ratio resized from ({o}, {o}) to ({nx}, {ny}) to fit image size of ({w}, {h})\nYou can try to fix it by modifying subsample_ratio parameter, but this should work too.\n'.format(
                o=subsample_ratio, nx=self._subsample_x, ny=self._subsample_y, w=w, h=h))
        self._arrow_width = subsample_ratio / 20.0

    def _items(self):
        return (self._draw(image, flow, self._color) for image, flow in zip(self._image_data, self._flow_data))

    def __len__(self):
        return min(len(self._image_data), len(self._flow_data))

    def get_type(self):
        return 'figure'

    @staticmethod
    def _mean_flow(flow, px, py, qx, qy):
        """ qx > px, qy > py and all inside flow bounds """
        pyc = math.ceil(py)
        pxc = math.ceil(px)
        qyf = math.floor(qy)
        qxf = math.floor(qx)

        # inside the rectangle
        total_sum = np.sum(flow[pyc:qyf, pxc:qxf, :], axis=(0, 1))
        total_area = (qyf - pyc) * (qxf - pxc)

        # rectangle's border might not be exact to pixel edges
        # add to total_area and sum
        rem_px = 1.0 - (px - int(px))
        rem_py = 1.0 - (py - int(py))
        rem_qx = qx - int(qx)
        rem_qy = qy - int(qy)
        # left edge
        if rem_px < 1:
            total_area += (qyf - pyc) * rem_px
            total_sum += np.sum(flow[pyc:qyf, pxc-1, :], axis=0) * rem_px
            # top-left edge
            if rem_py < 1:
                total_area += rem_py * rem_px
                total_sum += flow[int(py), int(px), :] * rem_py * rem_px
        # top edge
        if rem_py < 1:
            total_area += (qxf - pxc) * rem_py
            total_sum += np.sum(flow[pyc-1, pxc:qxf, :], axis=0) * rem_py
            # top-right edge
            if rem_qx > 0:
                total_area += rem_qx * rem_py
                total_sum += flow[int(py), int(qx), :] * rem_qx * rem_py
        # right-edge
        if rem_qx > 0:
            total_area += (qyf - pyc) * rem_qx
            total_sum += np.sum(flow[pyc:qyf, qxf, :], axis=0) * rem_qx
            # bottom-right edge
            if rem_qy > 0:
                total_area += rem_qy * rem_qx
                total_sum += flow[int(qy), int(qx), :] * rem_qy * rem_qx
        # bottom edge
        if rem_qy > 0:
            total_area += (qxf - pxc) * rem_qy
            total_sum += np.sum(flow[qyf, pxc:qxf, :], axis=0) * rem_qy
            # bottom-left edge
            if rem_px < 1:
                total_area += rem_px * rem_qy
                total_sum += flow[int(qy), int(px), :] * rem_px * rem_qy

        return total_sum / total_area

    def _draw(self, image, flow, color):
        if self._attenuation < 1:
            image = (image * self._attenuation).astype(np.uint8)
        ax = convert_to_axes(image)

        [h, w] = flow.shape[0:2]
        ix = round(w / self._subsample_x)
        iy = round(h / self._subsample_y)
        arrows = np.empty((iy, ix, 2))

        for y in range(iy):
            for x in range(ix):
                # flow zone
                px = max(x * self._subsample_x, 0)
                py = max(y * self._subsample_y, 0)
                qx = min(px + self._subsample_x, w)
                qy = min(py + self._subsample_y, h)
                # get mean flow in zone
                arrows[y, x, :] = DrawFlowArrows._mean_flow(
                    flow, px, py, qx, qy)

        if self._color == 'flow':
            fu = arrows[:, :, 0]
            fv = arrows[:, :, 1]
            arrows_norm = np.copy(arrows) / np.sqrt(fu ** 2 + fv ** 2).max()
            colors = flow_to_rgb(arrows_norm)
            alpha = np.ones((iy, ix, 1)) * 255.0
            # concatenate alpha component
            colors = np.concatenate((colors, alpha), axis=2)
            # convert to 0-1 range
            colors /= 255.0
            colors = np.reshape(colors, (iy * ix, 4))
        else:
            colors = self._color
            # convert to 0-1 range and add alpha
            colors = (colors[0] / 255.0, colors[1] / 255.0,
                      colors[2] / 255.0, 1.0)
            colors = np.reshape(np.repeat(colors, iy * ix),
                                (iy * ix, 4), order='F')

        origins = np.reshape([((x + 0.5) * self._subsample_x - 0.5,
                               (y + 0.5) * self._subsample_y - 0.5)
                              for y, x in itertools.product(range(iy), range(ix))], (iy * ix, 2))
        arrows = np.reshape(arrows, (iy * ix, 2))

        if not self._flat_colors:
            fu = arrows[:, 0]
            fv = arrows[:, 1]
            modules = np.reshape(fu ** 2 + fv ** 2, (iy * ix, 1))
            alpha_base = self._arrow_min_alpha
            alpha_mod = 1.0 - alpha_base
            modules = np.sqrt((modules / modules.max())) * \
                alpha_mod + alpha_base
            colors = np.multiply(colors, modules)

        ax.quiver(origins[:, 0], origins[:, 1], arrows[:, 0],
                  arrows[:, 1], scale_units='width', scale=w, angles='xy', color=colors, minlength=-1)

        return ax
