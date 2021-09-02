#postprocess_g
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

import numpy as np
import math

def postprocess_g(flux: np.ndarray, flux_argmax: int = None) -> np.ndarray:
    """

    Correction of negative values within the concentration and rate via the G-Procedure due to noise early within the flux. 
    
    Args:
        flux (float ndarray): The outlet flux. More specifically, the concentration or rate.

        flux_argmax (float, optional): The index of the maximum of the flux (typically the flux not the concentration or rate).

    Returns:
        flux (float ndarray): The flux without the negative values before the maximum of the flux response.

    Citation:
        None

    Implementor:
        M. Ross Kunz

    See also:
        None

    Link:
        None
    """
    if flux_argmax is None:
        flux_argmax = flux.argmax()

    initial_portion = flux[0:flux_argmax]
    max_noise = np.std(flux[(len(flux) - 30):len(flux)])
    negative_values = np.where(initial_portion < max_noise * 3)[0]
    if len(negative_values) > 0:
        negative_max = max(negative_values)
        flux_tail = [flux[-1]] * (negative_max + 1)
        flux = np.array(list(flux[(negative_max + 1):len(flux)]) + flux_tail)

        # sub_times = times[1:(flux_argmax + 1)]
        # time_range = times[flux_argmax]
        # temp_mean = time_range / 2 
        # temp_sd = temp_mean / 3
        # temp_cdf = np.array([0.5 * (1 + math.erf((i - temp_mean) / (temp_sd * np.sqrt(2)))) for i in sub_times])
        # flux[1:(flux_argmax +1 )] = temp_cdf * max(flux)

    return flux
