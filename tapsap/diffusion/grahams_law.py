# grahams_law
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

from numpy import array, ndarray, interp, sqrt, round, linspace, nan_to_num
from tapsap import utils


def grahams_law(flux: list, times: ndarray, current_mass: float, new_mass: float) -> ndarray:
    """

    This function uses linear interpolation to shift the flux to appear to be another mass.
    This uses the property of Graham's law of diffusion where the rate of diffusion is proportional to the square root ratio of masses.

    Args:
        flux (float ndarray): The outlet flux.

        times (float ndarray): An array of time.

        current_mass (float): The current mass of the given flux.

        new_mass (float): The mass in which you are transforming the flux to have the same diffusion.

    Returns:
        flux (array): The outlet flux after application of Graham's law.

    Citation:
        None

    See also:
        tapsap.utils.trapz

    Implementor:
        M. Ross Kunz

    Link:
        https://en.wikipedia.org/wiki/Graham%27s_law
    """
    grahams_constant = sqrt(current_mass / new_mass)
    min_time = min(times)
    max_time = max(times)
    graham_stop_point = int(round(len(times) / grahams_constant))

    min_flux = min(flux)
    if(min_flux < 0):
        flux = flux - min_flux

    original_m0 = utils.trapz(flux, times)
    len_flux = len(flux)


    if grahams_constant >= 1:
        flux_tail = list(flux[graham_stop_point:len_flux]) #[flux[len_flux - 1]] * int(len_flux - graham_stop_point)
        flux = array(list(interp(list(linspace(min_time, max_time,
                     graham_stop_point)), times, flux)) + flux_tail)
    else:
        flux = interp(list(times * grahams_constant), times, flux)

    flux = flux / utils.trapz(flux, times) * original_m0    
    flux = nan_to_num(flux)
    
    if(min_flux < 0):
        flux = flux + min_flux

    

    return flux
