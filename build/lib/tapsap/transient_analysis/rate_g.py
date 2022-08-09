# rate_g
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

import numpy as np
from tapsap import utils, transient_analysis


def rate_g(flux: np.ndarray, times: np.ndarray, zone_lengths: dict, inert_flux: np.ndarray = None) -> np.ndarray:
    """

    Calculation of the rate via the G-Procedure. 
    If the flux is derived from the reactant gas, then flux must be the difference of the inert_flux and reactant_flux or inert_flux must be populated with the flux of the inert.
    
    Args:
        flux (float ndarray): The outlet flux.

        times (float ndarray): An array of time.

        zone_lengths (dict): The reactor zone lengths.

        inert_flux (float ndarray, optional): The outlet flux of the inert.

    Returns:
        rate (float ndarray): The gas rate (temporal) of the given flux.

    Citation:
        Yablonsky et al, "The Y-procedure: How to extract the chemical transformation rate from reaction–diffusion data with no assumption on the kinetic model"

        Redekop et al, "The Y-Procedure methodology for the interpretation of transient kinetic data: Analysis of irreversible adsorption"

        Kunz et al, "Pulse response analysis using the Y-procedure: A data science approach"

        Kunz et al, "Probability theory for inverse diffusion: Extracting the transport/kinetic time-dependence from transient experiments"

    Implementor:
        M. Ross Kunz

    See also:
        tapsap.utils.trapz

    Link:
        https://doi.org/10.1016/j.ces.2007.04.050

        https://doi.org/10.1016/j.ces.2011.08.055

        https://doi.org/10.1016/j.ces.2018.06.078

        https://doi.org/10.1016/j.cej.2020.125985
    """
    original_m0 = utils.trapz(flux, times)

    catalyst_ratio = zone_lengths['zone2'] / sum(zone_lengths.values())

    if inert_flux is None:
        flux_diff = flux
    else:
        flux_diff = inert_flux - flux
        original_m0 = utils.trapz(flux_diff, times) / utils.trapz(inert_flux, times)

    # this is put here just incase there is no reaction, i.e., the inert flux is equal to the reactant flux
    if flux_diff.sum() == 0:
        return flux_diff

    flux_diff[0] = 0
    # altering the flux wrt the alpha parameter in the gamma distribution
    time_scalar = -(1 - catalyst_ratio**2) * 1.5
    temp_time_multiplier = times[1:len(times)]**time_scalar
    time_multiplier = np.array([0] + list(temp_time_multiplier))
    rate = flux_diff * time_multiplier
    rate[0] = 0

    rate = transient_analysis.postprocess_g(rate, flux.argmax())

    rate_area = utils.trapz(rate, times)
    # Appropriately scale the M0
    areaScalar = original_m0 / rate_area
    rate = rate * areaScalar * (-time_scalar) 

    return rate
