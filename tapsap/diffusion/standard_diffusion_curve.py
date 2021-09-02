# standard_diffusion_curve
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

from numpy import ndarray, linspace, array, pi, where, mod, exp, insert
import warnings


def standard_diffusion_curve(residence_time: float, times: ndarray) -> ndarray:
    """

    The standard diffusion curve representing the transport within the TAP reactor.

    Args:
        residence_time (dict): The residence time, see calculate_residence_time

        times (float ndarray): An array of time

    Returns:
        flux (array): The outlet flux of the standard diffusion curve

    Citation:
        Gleaves et al, "TAP-2: An interrogative kinetics approach"

    Implementor:
        M. Ross Kunz

    Link:
        https://doi.org/10.1016/S0926-860X(97)00124-5

    """
    if min(times) != 0:
        times = times - min(times)
    # remove zero
    times = times[1:len(times)]

    n_terms = 100
    j_vals = linspace(start=0, stop=n_terms, num=(n_terms + 1))
    negative_iteration = array([1] * (n_terms + 1))
    negative_iteration[where(mod(j_vals, 2) == 1)[0]] = -1
    j_negative = negative_iteration * (2 * j_vals + 1)

    warnings.filterwarnings("ignore", category=RuntimeWarning)
    exponent_terms = -0.5 * pi**2 * (j_vals + 0.5)**2 / residence_time
    exponent_terms = array([exponent_terms]).transpose()
    times = array([times])
    j_negative = array([j_negative])
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    exponent_with_time = (j_negative @ exp(exponent_terms @ times))[0]
    flux = pi * exponent_with_time / (residence_time * 2)
    flux = insert(flux, 0, 0)

    return flux
