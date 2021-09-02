# standard_diffusion_curve
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

from numpy import ndarray
from scipy.optimize import minimize_scalar
from tapsap.diffusion import standard_diffusion_curve


def opt_sdc(residence_time: float, flux: ndarray, times: ndarray) -> list:
    """

    Optimization of the residence time for the standard diffusion curve.

    Args:
        residence_time (float): The initial estimates of the residence time, see calculate_residence_time.

        flux (float ndarray): The outlet flux.

        times (float ndarray): An array of time

    Returns:
        optimized_sdc, residence_time (list): The standard diffusion curve of the flux and the optimized residence time.

    Citation:
        Gleaves et al, "TAP-2: An interrogative kinetics approach"

    Implementor:
        M. Ross Kunz

    Link:
        https://doi.org/10.1016/S0926-860X(97)00124-5

    """

    def min_sdc(residence_time: float, flux: ndarray, times: ndarray) -> float:
        estimated_sdc = standard_diffusion_curve(residence_time, times)
        peak_residence_time_diff = abs(max(flux) - max(estimated_sdc))
        return peak_residence_time_diff

    fit = minimize_scalar(lambda residence_time: min_sdc(residence_time, flux, times), bounds=(0, None))
    residence_time = fit.x
    optimized_sdc = standard_diffusion_curve(residence_time, times)
    result = {
        'flux':optimized_sdc, 
        'residence_time':residence_time
    }

    return result
