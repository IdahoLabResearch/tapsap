# rtd_parameters
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

import pandas as pd

def rtd_parameters(moments: dict) -> dict:
    """

    Calculation of the residence time distribution parameters using the moments.
    This includes the shape and scale estimates assuming a Gamma distribution.
    
    Args:
        moments (dict | DataFrame): The integral of the flux

    Returns:
        rtd_parameters (dict): The mean residence time, variance residence time, gamma shape parameter, and gamma scale parameter

    Citation:
        Gleaves et al, "TAP-2: An interrogative kinetics approach"

        Constales et al, "Multi-zone TAP-reactors theory and application: I. The global transfer matrix equation"

        Constales et al, "Multi-zone TAP-reactors theory and application: II. The three-dimensional theory"

        Casella et al, "Statistical Inference"

    Implementor:
        M. Ross Kunz

    See also:
        tapsap.moments_analysis.moments

    Link:
        https://doi.org/10.1016/S0926-860X(97)00124-5

        https://doi.org/10.1016/S0009-2509(00)00216-5

        https://doi.org/10.1016/S0009-2509(00)00217-7

        https://en.wikipedia.org/wiki/Gamma_distribution
    """
    if isinstance(moments, pd.DataFrame):
        mean_residence_time = moments['M1'].values / moments['M0'].values
        variance_residence_time = moments['M2'].values / moments['M0'].values - mean_residence_time**2
    else:
        mean_residence_time = moments['M1'] / moments['M0']
        variance_residence_time = moments['M2'] / moments['M0'] - mean_residence_time**2

    gamma_shape = mean_residence_time**2 / variance_residence_time
    gamma_scale = mean_residence_time / variance_residence_time
    result = {
        'mean_residence_time':mean_residence_time, 
        'variance_residence_time':variance_residence_time, 
        'gamma_shape':gamma_shape, 
        'gamma_scale':gamma_scale
    }
    return result
