# active_sites_by_pulse
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

import numpy as np
from tapsap import preprocess


def active_sites_by_pulse(flux_M0: np.ndarray, inert_M0:np.ndarray, stoichiometric_coef:float, first_order:bool = True, huber_loss:bool=False) -> dict:
    """

    A function for determining the diffusion coefficient from the moments of the flux.
    Note that this method only works for an irreversible process.
    
    Args:
        flux_M0 (ndarray): An array of M0 values based on the flux.

        inert_M0 (ndarray): An array of M0 values based on the inert/reference flux.

        stoichiometric_coef (float): The stoichimetric coefficient of the gas species.

        first_order (float): If the reaction is first ordered.  If False, then the reaction will be assumed to be second order.

        huber_loss (bool): Use a robust loss function rather than the standard square error loss.

    Returns:
        fitted, active_sites (dict): The fitted values by pulse number and the active sites.

    Citation:
        Constales et al, "Methods for determining the intrinsic kinetic characteristics of irreversible adsorption processes."

    Implementor:
        M. Ross Kunz

    See also:
        tapsap.moments_analysis.moments

    Link:
        https://doi.org/10.1016/j.ces.2019.06.026
    """
    conversion = 1 - flux_M0 / inert_M0
    damkoler = conversion / (1 - conversion)
    pulse_index = np.array(list(range(len(flux_M0)))) + 1
    pulse_index_mean = pulse_index.mean()
    pulse_index = pulse_index - pulse_index_mean
    # depending on if the reaction is first order or second order, the equation will change
    if first_order:
        regression_variable = -damkoler - np.log(damkoler)
    else:
        regression_variable = 1 / np.sqrt(damkoler) - np.sqrt(damkoler) - 1

    regression_variable_mean = regression_variable.mean()
    regression_variable = regression_variable - regression_variable_mean
    intercept = pulse_index_mean - regression_variable_mean

    fit = preprocess.tap_mix(regression_variable, pulse_index, times = 1, constraints=False, huber_loss= huber_loss)
    active_sites = stoichiometric_coef * fit['calibration_coef'][0] * np.sqrt(intercept)
    result = {
        'fitted':fit['flux'] + intercept,
        'active_sites':active_sites
    } 
    return result    