import numpy as np
import imageio
from PIL import Image
from flowvid.colorwheel import uv_to_rgb


def treat_flows(flows, normalize=None, subsamples=0):
    """
        Normalize flows and treat them as part of a multi-frame array
    """
    if flows.ndim == 3:
        flows = np.reshape(flows, [1] + list(flows.shape))

    fu = flows[:, :, :, 0]
    fv = flows[:, :, :, 1]
    if normalize == 'video':
        fmod = np.sqrt(fu ** 2 + fv ** 2)
        fmodmax = fmod.max()
        fu = fu / fmodmax
        fv = fv / fmodmax
    elif normalize == 'frame':
        for frame, (u, v) in enumerate(zip(fu, fv)):
            fmod = np.sqrt(u ** 2 + v ** 2)
            fmodmax = fmod.max()
            fu[frame, :, :] = u / fmodmax
            fv[frame, :, :] = v / fmodmax

    # TODO subsamples

    return fu, fv


def flows_to_colors(flows, filename, framerate, normalize):
    """
        TODO
        in shape [frame height width uv] dtype float32
        out shape [frame height width rgb] dtype uint8
    """
    fu, fv = treat_flows(flows, normalize=normalize)
    rgb = uv_to_rgb(fu, fv)

    with imageio.get_writer(filename, fps=framerate) as video:
        for frame in rgb:
            # TODO image
            # image = Image.fromarray(frame, 'RGB')
            # image.save('prueba.png')
            video.append_data(frame)
