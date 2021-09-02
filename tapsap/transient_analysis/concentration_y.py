# concentration_y
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

import numpy as np
from tapsap import utils

def concentration_y(flux: np.ndarray, times: np.ndarray, diffusion: float, zone_lengths: dict, zone_porosity: dict, smoothing_amt: float = 3) -> np.ndarray:
    """

    Calculation of the concentration via the Y-Procedure. 
    Note that they Y-Procedure is extremely sensitive on the smoothing amount provided.  
    
    Args:
        flux (float ndarray): The outlet flux.

        times (float ndarray): An array of time.

        diffusion (float): The diffusion coefficient within the catalyst zone.

        zone_lengths (dict): The reactor zone lengths.

        zone_porosity (dict): The assumed bed porosity within the catalyst.

        smoothing_amt (float, optional): The amount of smoothing to be applied to the Y-Procedure. 

    Returns:
        concentration (float ndarray): The gas concentration (1/second) of the given flux.

    Citation:
        Yablonsky et al, "The Y-procedure: How to extract the chemical transformation rate from reaction–diffusion data with no assumption on the kinetic model"

        Redekop et al, "The Y-Procedure methodology for the interpretation of transient kinetic data: Analysis of irreversible adsorption"

        Kunz et al, "Pulse response analysis using the Y-procedure: A data science approach"

        Kunz et al, "Probability theory for inverse diffusion: Extracting the transport/kinetic time-dependence from transient experiments"

    Implementor:
        M. Ross Kunz

    Link:
        https://doi.org/10.1016/j.ces.2007.04.050

        https://doi.org/10.1016/j.ces.2011.08.055

        https://doi.org/10.1016/j.ces.2018.06.078

        https://doi.org/10.1016/j.cej.2020.125985
    """
    len_flux = len(flux)

    gamma_3 = diffusion / zone_lengths['zone2']
    tau_1 = zone_porosity['zone0'] * zone_lengths['zone0']**2 / diffusion
    tau_3 = zone_porosity['zone2'] * zone_lengths['zone2']**2 / diffusion

    k = np.array(list(np.arange(0, np.ceil(len_flux / 2) + 1)) +
                list(np.arange(-np.floor(len_flux / 2), -1)))
    omega = 2 * np.pi * k / (len_flux * (times[1] - times[0]))
    omega[0] = 1e-10
    smoothing_vector = np.exp(-omega**2 * (times[1] - times[0])**2 * smoothing_amt**2 / 2)
    iwt1 = np.sqrt(1.j * omega * tau_1)
    iwt3 = np.sqrt(1.j * omega * tau_3)
    gas_scalar = np.sinh(iwt3) / iwt1
    gas_scalar[0] = 1
    gas_scalar = gas_scalar * smoothing_vector / gamma_3
    
    concentration = np.real(np.fft.ifft(np.fft.fft(flux) * gas_scalar))
    concentration_area = utils.trapz(concentration, times)
    flux_area = utils.trapz(flux, times)
    # Area normalize the concentration
    concentration = concentration * flux_area / concentration_area

    return concentration
