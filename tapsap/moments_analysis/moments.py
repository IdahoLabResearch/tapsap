# moments
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved


from tapsap import utils
import numpy as np
import pandas as pd

def moments(flux: np.ndarray, times: np.ndarray, integration_time_range: list = None) -> dict:
    """

    Calculation of the moments using the trapezoidal rule
    
    Args:
        flux (float ndarray | dataframe): The outlet flux.

        times (float ndarray): An array of time.

        integration_time_range (ints list, optional): A list contianing the start and end time to integrate the flux. If None, then set to the min and max time.

    Returns:
        moments (dict): The moments of the flux

    Citation:
        Gleaves et al, "TAP-2: An interrogative kinetics approach"

        Constales et al, "Multi-zone TAP-reactors theory and application: I. The global transfer matrix equation"

        Constales et al, "Multi-zone TAP-reactors theory and application: II. The three-dimensional theory"

    Implementor:
        M. Ross Kunz

    See also:
        tapsap.utils.trapz

    Link:
        https://doi.org/10.1016/S0926-860X(97)00124-5

        https://doi.org/10.1016/S0009-2509(00)00216-5

        https://doi.org/10.1016/S0009-2509(00)00217-7
    """
    if integration_time_range is not None:
        integration_time_range.sort()
            
    integration_index_start = 0
    integration_index_end = len(times)
    if integration_time_range is not None:
        integration_index_start = abs(times - integration_time_range[0]).argmin()
        integration_index_end = abs(times - integration_time_range[1]).argmin()

    index_len = integration_index_end - integration_index_start
    index_range = np.arange(integration_index_start, integration_index_end)

    if isinstance(flux, pd.DataFrame):
        num_pulse = flux.shape[1]        
        M0 = np.zeros(num_pulse)
        M1 = np.zeros(num_pulse)
        M2 = np.zeros(num_pulse)
        for i in range(num_pulse):
            if integration_time_range is None:
                temp_times = utils.find_integration_time(flux.iloc[:,i], times)
                temp_integration_index_start = abs(times - temp_times[0]).argmin()
                temp_integration_index_end = abs(times - temp_times[1]).argmin()
                index_len = temp_integration_index_end - temp_integration_index_start
                index_range = np.arange(temp_integration_index_start, temp_integration_index_end)

            sub_flux = flux.iloc[index_range, :].copy(deep=True)
            sub_times = times[np.arange(0, index_len)]

            M0[i] = utils.trapz(sub_flux.iloc[:,i].values * sub_times**0, sub_times)
            M1[i] = utils.trapz(sub_flux.iloc[:,i].values * sub_times**1, sub_times)
            M2[i] = utils.trapz(sub_flux.iloc[:,i].values * sub_times**2, sub_times)

    else:
        sub_flux = flux[index_range]
        sub_times = times[np.arange(0, index_len)]

        flux_M0 = sub_flux * sub_times**0
        flux_M1 = sub_flux * sub_times**1
        flux_M2 = sub_flux * sub_times**2

        M0 = utils.trapz(flux_M0, sub_times)
        M1 = utils.trapz(flux_M1, sub_times)
        M2 = utils.trapz(flux_M2, sub_times)

    result = {
        'M0':M0,
        'M1':M1,
        'M2':M2
    }

    return result
