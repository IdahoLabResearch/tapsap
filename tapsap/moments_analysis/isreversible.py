# isreversible
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

from numpy import ndarray
from tapsap import diffusion, moments_analysis


def isreversible(flux: ndarray, times: ndarray, inert_flux: ndarray, flux_mass: float, inert_mass: float) -> bool:
    """

    Check to see if the flux is reversible when compared to the inert flux.
    This requires first that the inert flux be transformed to the same mass as the flux through Graham's law.
    Afterwhich, the normalized first moment of the flux is compared to the inert to determine reversibility.
    If M1_flux < M1_inert, then irreversible.
    
    Args:
        flux (float ndarray): The outlet flux.

        times (float ndarray): An array of time.

        inert_flux (float ndarray): The outlet flux of the inert.

        flux_mass (float): The mass of the flux.

        inert_mass (float): The mass of the inert flux.

    Returns:
        isreversible (bool): Determine if the outlet flux is reversible.

    Citation:
        Gleaves et al, "TAP-2: An interrogative kinetics approach"

        TODO TEAK

    Implementor:
        M. Ross Kunz

    See also:
        tapsap.diffusion.grahams_law
        
        tapsap.moments_analysis.moments

    Link:
        https://doi.org/10.1016/S0926-860X(97)00124-5
        
        TODO TEAK
    """
    # transform the inert
    inert_mod = diffusion.grahams_law(inert_flux, times, inert_mass, flux_mass)
    # calculate the moments
    flux_moments = moments_analysis.moments(flux, times)
    inert_moments = moments_analysis.moments(inert_mod, times)
    if (flux_moments['M1'] / flux_moments['M0']) < (inert_moments['M1'] / inert_moments['M0']):
        return False
    else:
        return True
