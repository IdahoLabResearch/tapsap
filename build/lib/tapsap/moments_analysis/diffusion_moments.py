# diffusion_moments
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

import numpy as np
import pandas as pd


def diffusion_moments(moments: dict, zone_lengths:dict, zone_porosity:dict, current_mass:float=None, new_mass:float=None) -> dict:
    """

    A function for determining the diffusion coefficient from the moments of the flux.
    
    Args:
        moments (dict | dataframe): The moments of the flux

        zone_lengths (dict): The zone lengths for the reactor, e.g., {0.002, 0.000001, 0.002}

        zone_porosity (dict): The bed porosity within each zone

        current_mass (float): The current mass of the given flux.

        new_mass (float): The mass in which you are transforming the flux to have the same diffusion (typically the inert mass).

    Returns:
        diffusion (dict): The diffusion coefficients per pulse.

    Citation:
        Gleaves et al, "TAP-2: An interrogative kinetics approach"

    Implementor:
        M. Ross Kunz

    See also:
        tapsap.moments_analysis.moments

    Link:
        https://doi.org/10.1016/S0926-860X(97)00124-5
    """
    if isinstance(moments, pd.DataFrame):
        moment_ratio = moments['M0'].values / (2 * moments['M1'].values)
    else:
        moment_ratio = moments['M0'] / (2 * moments['M1'])

    diffusion = np.mean(list(zone_porosity.values())) * sum(list(zone_lengths.values()))**2 * moment_ratio

    if (current_mass is not None) & (new_mass is not None):
        diffusion_scalar = np.sqrt(new_mass / current_mass) 
        diffusion *= diffusion_scalar

    return {'diffusion':diffusion}

