# min_mean_max
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

import pandas as pd
import numpy as np

def min_mean_max(flux: np.ndarray) -> dict:
    """

    Calculation of the min, mean and max of the flux.
    
    Args:
        flux (ndarray | DataFrame): The outlet flux.

    Returns:
        min_mean_max (dict): The min mean and max of a flux.

    Implementor:
        M. Ross Kunz

    """
    if isinstance(flux, pd.DataFrame):
        temp_min = np.array(flux.apply(min, 0))
        temp_mean = np.array(flux.apply(np.mean, 0))
        temp_max = np.array(flux.apply(max, 0))
    else:
        temp_min = flux.min()
        temp_mean = flux.mean()
        temp_max = flux.max()

    result = {
        'min':temp_min,
        'mean':temp_mean,
        'max':temp_max
    }

    return result