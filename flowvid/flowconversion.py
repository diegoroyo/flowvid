import numpy as np
import imageio
from PIL import Image
from flowvid.colorwheel import uv_to_rgb
from flowvid.readflow import read_flow, list_directory, find_max_flow


def treat_flow(flow, norm=None, normalize=False, subsamples=0):
    """
        Normalize flows and treat them as part of a multi-frame array
    """
    if flows.ndim == 3:
        flows = np.reshape(flows, [1] + list(flows.shape))

    fu = flows[:, :, 0]
    fv = flows[:, :, 1]
    if normalize:
        if norm is not None:
            fu = fu / norm
            fv = fv / norm
        else:
            fmax = np.sqrt(fu ** 2 + fv ** 2).max()
            fu = fu / fmax
            fv = fv / fmax

    # TODO subsamples

    return fu, fv


def flows_to_colors(flowdir, filename, framerate, normalize):
    """
        TODO
        in shape [frame height width uv] dtype float32
        out shape [frame height width rgb] dtype uint8
    """
    file_list = list_directory(flowdir)#[1:100]

    norm = None
    if normalize == 'video':
        norm = find_max_flow(file_list)
    
    with imageio.get_writer(filename, fps=framerate) as video:
        for flo_file in file_list:
            flow = read_flow(flo_file)
            fu = flow[:, :, 0]
            fv = flow[:, :, 1]
            if normalize == 'video':
                # normalize options
                norm_threshold = 0.8
                norm_curve = 0.65
                # normalize data
                idu = fu > (norm * norm_threshold)
                fu[idu] = 1
                fu[~idu] = fu[~idu] / (norm * norm_threshold)
                fu[~idu] = np.sign(fu[~idu]) * (np.abs(fu[~idu]) ** norm_curve)
                idv = fv > (norm * norm_threshold)
                fv[idv] = 1
                fv[~idv] = fv[~idv] / (norm * norm_threshold)
                fv[~idv] = np.sign(fv[~idv]) * (np.abs(fv[~idv]) ** norm_curve)
            elif normalize == 'frame':
                # normalize data
                fmax = np.sqrt(fu ** 2 + fv ** 2).max()
                fu = fu / fmax
                fv = fv / fmax
            rgb = uv_to_rgb(fu, fv)
            # TODO image
            print('frame', flo_file)
            # image = Image.fromarray(frame, 'RGB')
            # image.save('prueba.png')
            video.append_data(rgb)


def flows_to_added(image0, flowdir, filename, framerate, normalize):
