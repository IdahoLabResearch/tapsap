# rate_y
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

import numpy as np

def rate_y(flux: np.ndarray, times: np.ndarray, diffusion: float, zone_lengths: dict, zone_porosity: dict, inert_flux: np.ndarray = None,  smoothing_amt: float = 3) -> np.ndarray:
    """

    Calculation of the rate via the Y-Procedure. 
    Note that they Y-Procedure is extremely sensitive on the smoothing amount provided.  
    
    Args:
        flux (float ndarray): The outlet flux.

        times (float ndarray): An array of time.

        diffusion (float): The diffusion coefficient within the catalyst zone.

        zone_lengths (dict): The reactor zone lengths.

        inert_flux (float ndarray, optional): The outlet flux of the inert.

        smoothing_amt (float, optional): The amount of smoothing to be applied to the Y-Procedure. 

        zone_porosity (dict): The assumed bed porosity within the catalyst.

    Returns:
        concentration (float ndarray): The gas concentration of the given flux.

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
    if inert_flux is None:
        flux_diff = flux
    else:
        flux_diff = inert_flux - flux

    len_flux = len(flux)
    gamma_1 = diffusion / zone_lengths['zone0']
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

    rate_scalar = (np.cosh(iwt3) + np.sqrt(tau_1 * gamma_1**2 / (tau_3 * gamma_3**2))
                   * np.sinh(iwt1) * np.sinh(iwt3) / np.cosh(iwt1)) * smoothing_vector
    rate = np.real(np.fft.ifft(np.fft.fft(flux_diff) * rate_scalar))

    return rate
