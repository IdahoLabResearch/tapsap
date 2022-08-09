# baseline_gamma
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

from numpy import ndarray, sign, arange
from tapsap import utils

def baseline_gamma(flux: ndarray, times: ndarray) -> dict:
    """

    Baseline the flux through examining the tail of the gamma distribution.
    
    Args:
        flux (float ndarray): The outlet flux.

        times (float ndarray): An array of time.

    Returns:
        corrected_flux, baseline_amount (dict): The baseline corrected flux and the baseline amount.
        
    Citation:
        Kunz et al, "A Priori Calibration of Transient Kinetics Data via Machine Learning" (In prep)

    Implementor:
        M. Ross Kunz

    See also:
        tapsap.utils.gamma_pdf

    Link:
        https://en.wikipedia.org/wiki/Gamma_distribution

        https://arxiv.org/abs/2109.15042
    """
    original_flux = flux
    peak_index = flux.argmax()
    # Set the peak location to an arbitrary value of the flux starts with a maximum value in the case of pure noise
    if peak_index == 0:
        peak_index = 5

    peak_residence_time = times[peak_index]
    flux_min = flux[arange(peak_index, len(flux))].min()
    tail_position = arange(len(flux) - 30, len(flux))
    # This assumes an inert gamma distribution where the shape is equal to 1.5 and the scale = 1/3.
    # The relationship between the mode (peak residence time) and the gamma distribution parameters are (shape - 1) * scale = mode.
    # Then combining both statements, the peak residence time / (1.5 - 1) is equal to the scale.
    #tail_gamma = utils.gamma_pdf(
    #    times[tail_position], shape=1.5, scale=peak_residence_time * 2)


    #peak_gamma = utils.gamma_pdf(times[peak_index], shape=1.5, scale=peak_residence_time * 2)

    tail_gamma = utils.gamma_pdf(times[-1], shape=1.5, scale=peak_residence_time * 2)
    #baseline_offset = (flux[tail_position] -
    #                   flux_min).mean() - tail_gamma.mean()
    baseline_offset = ((flux[tail_position]).mean() - flux_min) - tail_gamma
    baseline_amount = flux_min - sign(flux_min) * abs(baseline_offset)
    corrected_flux = original_flux - baseline_amount

    result = {
        'flux':corrected_flux,
        'baseline_amount':baseline_amount
    }
    return result
