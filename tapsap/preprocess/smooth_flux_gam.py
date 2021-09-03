# smooth_flux_gam
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

#from numpy import ndarray, floor, arange, pi, exp, linspace, round, concatenate, array
#from pygam import LinearGAM, s
#import warnings
from csaps import csaps
import numpy as np


def smooth_flux_gam(flux: np.ndarray, smooth_amount = 1e-4) -> np.ndarray:
    """

    Smoothing via a Generalized Additive Model applied to the flux.
    
    Args:
        flux (float array): The outlet flux

    Returns:
        smoothed_flux (float array): The smoothed outlet flux 

    Citation:
        Hastie et al. "Generalized additive models"

        Kunz et al, "A Priori Calibration of Transient Kinetics Data via Machine Learning" (In prep)

    Implementor:
        M. Ross Kunz

    Link:
        https://doi.org/10.1214/ss/1177013604

        Kunz et al, "A Priori Calibration of Transient Kinetics Data via Machine Learning" (In prep)
    """
    temp_index = np.arange(0, len(flux))
    smoothed_flux = csaps(temp_index, flux, temp_index, smooth = smooth_amount)
    peak_pos = np.argmax(flux)
    peak_prior = smoothed_flux[0:peak_pos]
    less_than_zero = np.where(peak_prior < min(flux))[0]
    len_less_than_zero = len(less_than_zero)
    if len_less_than_zero > 0:
        for i in less_than_zero:
            if i == 0:
                smoothed_flux[i] = np.median([smoothed_flux[i], smoothed_flux[i + 1], smoothed_flux[i + 2]])
            else:
                smoothed_flux[i] = np.median([smoothed_flux[i - 1], smoothed_flux[i], smoothed_flux[i + 1]])


    #smoothed_flux = apply_csaps(flux, smooth_amount)
    
    # while min(smoothed_flux) < min(flux):
    #     smooth_amount *= 2
    #     smoothed_flux = apply_csaps(flux, smooth_amount)


    # len_flux = len(flux)
    # max_position = flux.argmax()
    # num_knots = 30

    # if max_position < num_knots:
    #     max_position = num_knots

    # if max_position >= (len_flux - num_knots):
    #     max_position = len_flux - num_knots

    # sd_of_noise = floor(max_position / 2)
    # pre_index = arange(0, max_position)
    # mid_index = arange(int(max_position - sd_of_noise),
    #                    int(max_position + sd_of_noise))
    # if(max(mid_index) > len_flux):
    #     mid_index = arange(int(max_position - sd_of_noise), len_flux - 1)

    # post_index = arange(max_position, len_flux)
    # mid_transition = pi * exp(-0.5 * linspace(-5, 5, len(mid_index))**2)
    # mid_transition = mid_transition / max(mid_transition)

    # pre_peak = flux[pre_index]
    # mid_peak = flux[mid_index]
    # post_peak = flux[post_index]

    # num_knots = int(round(min(num_knots, len(pre_index) * 0.9,
    #                   len(mid_index) * 0.9, len(post_index) * 0.9)))

    # # this is incase there are outliers within the data
    # if num_knots < 1:
    #     all_index = arange(0, len(flux))
    #     fit = LinearGAM(s(0, 50)).fit(all_index, flux)
    #     fit_predict = fit.predict(all_index)
    #     return fit_predict


    # warnings.filterwarnings("ignore", category=DeprecationWarning)
    # warnings.filterwarnings("ignore", category=RuntimeWarning)
    # pre_fit = LinearGAM(s(0, num_knots)).fit(pre_index, pre_peak)
    # warnings.filterwarnings("ignore", category=DeprecationWarning)
    # warnings.filterwarnings("ignore", category=RuntimeWarning)
    # mid_fit = LinearGAM(s(0, num_knots)).fit(mid_index, mid_peak)
    # warnings.filterwarnings("ignore", category=DeprecationWarning)
    # warnings.filterwarnings("ignore", category=RuntimeWarning)
    # post_fit = LinearGAM(s(0, num_knots)).fit(post_index, post_peak)

    # smoothed_flux = concatenate(
    #     [pre_fit.predict(pre_index), post_fit.predict(post_index)])

    # smoothed_flux[mid_index] = mid_fit.predict(
    #     mid_index) * mid_transition + smoothed_flux[mid_index] * (1 - mid_transition)

    return smoothed_flux
