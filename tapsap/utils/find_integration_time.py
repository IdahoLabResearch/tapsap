# find_integration_time
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

import numpy as np


def find_integration_time(flux: np.ndarray, times: np.ndarray, min_value: float = 0) -> list:
    """

    Find the integration time based on the support (non-negative values assuming a distribution of the molecules).
    
    Args:
        flux (float ndarray): The outlet flux.

        times (float ndarray): An array of time.

        min_value (float): The minimal value allowed for the flux.

    Returns:
        integration_time_range (list): A list contianing the start and end time to integrate the flux. If None, then set to the min and max time.
        
    Citation:
        TODO TEAK

    Implementor:
        M. Ross Kunz

        TODO TEAK
    """
    flux_max = np.argmax(flux)
    if flux_max < 30:
        flux_max = 30

    pre_max_zeros = np.where(flux[0:flux_max] < min_value)[0]
    post_max_zeros = np.where(flux[(flux_max + 1):len(flux)] < min_value)[0] + flux_max

    integration_index_start = 0
    integration_index_end = len(flux)
    if len(pre_max_zeros) != 0:
        integration_index_start = max(pre_max_zeros)

    if len(post_max_zeros) != 0:
        integration_index_end = min(post_max_zeros)

    total_len = integration_index_end - integration_index_start
    if total_len < 30:
        if integration_index_start < 30:
            integration_index_end = integration_index_start + 30
        elif integration_index_end > (len(flux) - 30):
            integration_index_start = integration_index_end - 30
        else:
            integration_index_end = integration_index_start + 30

    integration_time_range = [times[integration_index_start], times[integration_index_end - 1]]

    
    return integration_time_range