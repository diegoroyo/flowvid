from .utils import ask_string, ask_multichoice
import numpy as np
import flowvid as fv
import matplotlib.pyplot as plt


def preset_plot_epe():
    # Flow directories
    flo_est_dir = ask_string(
        'Estimated flow files directory ({s}): ', default='flo_est')
    flo_gt_dir = ask_string(
        'Ground truth flow files directory ({s}): ', default='flo_gt')

    # Plot options
    density = ask_multichoice('Normalize? (0-1 range) ({s}): ',
                              answer_map={'yes': True, 'no': False}, default='yes')
    cumulative = ask_multichoice('Cumulative? ({s}): ',
                                 answer_map={'yes': True, 'no': False}, default='yes')

    # Flow data and EPE
    flo_est = fv.input.flo(flo_est_dir)
    flo_gt = fv.input.flo(flo_gt_dir)
    epe = fv.endpoint_error(flo_est, flo_gt)
    [h, w] = flo_est[0].shape[0:2]

    # Flatten all data from all frames
    epe_flat = np.array([])
    for epe_frame in epe:
        epe_flat = np.append(epe_flat, epe_frame).flatten()

    # Generate plot
    plt.xscale('log')
    plt.grid()
    plt.title('EPE distribution\n' + str(len(flo_gt)) +
              ' frames @ ' + str(w) + 'x' + str(h) + 'px')
    plt.hist(epe_flat, bins=np.logspace(np.log10(1e-3), np.log10(1e2), num=40), label='Estimated EPE',
             cumulative=cumulative, density=density, histtype='step')
    plt.legend(loc='lower right')
    plt.show()
