#concentration_g
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

import numpy as np
from tapsap import utils, transient_analysis


def concentration_g(flux: np.ndarray, times: np.ndarray, zone_lengths: dict) -> np.ndarray:
    """

    Calculation of the concentration via the G-Procedure. 
    
    Args:
        flux (float ndarray): The outlet flux.

        times (float ndarray): An array of time.

        zone_lengths (dict): The reactor zone lengths.

    Returns:
        concentration (float ndarray): The gas concentration (1/second) of the given flux.

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
    # assuming a symmetric reactor for the time being, but this may be altered accordingly
    catalyst_ratio = zone_lengths['zone2'] / sum(zone_lengths.values())

    # altering the flux wrt the alpha parameter in the gamma distribution
    time_scalar = -(1 - catalyst_ratio**2) / 6
    temp_time_multiplier = times[1:len(times)]**time_scalar
    time_multiplier = np.array([0] + list(temp_time_multiplier))
    concentration = flux * time_multiplier
    concentration = transient_analysis.postprocess_g(concentration, flux.argmax())

    # Calculate the area
    concentration_area = utils.trapz(concentration, times)
    flux_area = utils.trapz(flux, times)
    # Dimensionless concentration
    concentration = concentration * flux_area / concentration_area

    return concentration
