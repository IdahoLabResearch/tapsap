# trapz
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

from numpy import ndarray


def trapz(flux: ndarray, times: ndarray) -> float:
    """

    Trapazoidal integration or integration by sum.  
    Times can either be a vector of time with the same length as the flux 
    or it can be the difference in time for each measurement point.
    
    Args:
        flux (float ndarray): The outlet flux.

        times (float ndarray): An array of time.

    Returns:
        integral (float): The integral of the flux

    Citation:
        None

    Implementor:
        M. Ross Kunz

    Link:
        https://en.wikipedia.org/wiki/Trapezoidal_rule

    """
    diff_1 = times[1] - times[0]
    diff_2 = times[2] - times[1]
    if diff_1 == diff_2:
        integral = sum(flux) * diff_1
    else:
        flux_len = len(flux)
        integral = 0.5 * sum((times[1:flux_len] - times[0:(flux_len - 1)])
                             * (flux[1:flux_len] + flux[0:(flux_len - 1)]))

    return integral
