import numpy as np
import imageio
from colorwheel import uv_to_rgb

def treat_flows(flows, normalize=False, subsamples=0):
    """
        Normalize flows and treat them as part of a multi-frame array
    """
    if flows.ndim == 3:
        flows = np.reshape(flows, [1] + list(flows.shape))
    
    fu = flows[:, :, :, 0]
    fv = flows[:, :, :, 1]
    if normalize:
        fmod = np.sqrt(fu ** 2 + fv ** 2)
        fmodmax = fmod.max()
        fu = fu / fmodmax
        fv = fv / fmodmax

    # TODO subsamples

    return fu, fv


def flows_to_colors(flows, filename='video.mp4', framerate=24):
    """
        TODO
        in shape [frame height width uv] dtype float32
        out shape [frame height width rgb] dtype uint8
    """
    fu, fv = treat_flows(flows, normalize=True)
    rgb = uv_to_rgb(fu, fv)

    with imageio.get_writer(filename, fps=framerate) as video:
        for frame in rgb:
            video.append_data(frame)





