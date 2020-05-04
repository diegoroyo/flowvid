from .utils import get_arg, ask_string, ask_multichoice
import numpy as np
import flowvid as fv
import matplotlib.pyplot as plt


def preset_plot_epe(kwargs):
    # Flow directories
    flo_est_dir = get_arg(kwargs, 'flo_dir',
                          lambda: ask_string('Estimated flow files directory ({s}): ', default='flo_est', is_path=True))
    flo_gt_dir = get_arg(kwargs, 'flo_gt_dir',
                         lambda: ask_string('Ground truth flow files directory ({s}): ', default='flo_gt'))

    # Plot options
    cumulative = get_arg(kwargs, 'plot_cumulative',
                         lambda: ask_multichoice('Cumulative? ({s}): ',
                                                 answer_map={'y': True, 'n': False}, default='y'))
    density = get_arg(kwargs, 'plot_normalize',
                      lambda: ask_multichoice('Normalize? (0-1 range) ({s}): ',
                                              answer_map={'y': True, 'n': None}, default='y'))

    # Flow data and EPE
    flo_est = fv.input.flo(flo_est_dir)
    flo_gt = fv.input.flo(flo_gt_dir)
    epe = fv.endpoint_error(flo_est, flo_gt)
    [h, w] = flo_est[0].shape[0:2]

    # Flatten all data from all frames
    epe_flat = np.array([epe_frame for epe_frame in epe]).flatten()

    # Generate plot
    weights = np.ones(len(epe_flat))

    if density:  # probability density function using weights instead of density parameter
        weights /= len(weights)

    plt.hist(epe_flat, bins=np.logspace(np.log10(1e-4), np.log10(1e3), num=40), label='Estimated EPE',
             cumulative=cumulative, weights=weights, density=False, histtype='step')
    plt.xscale('log')
    plt.grid()
    plt.title('EPE distribution\n' + str(len(flo_gt)) +
              ' frames @ ' + str(w) + 'x' + str(h) + 'px')

    if cumulative:
        plt.legend(loc='lower right')
    else:
        plt.legend(loc='upper right')

    plt.show()
