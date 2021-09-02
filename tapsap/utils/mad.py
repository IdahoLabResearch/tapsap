# mad
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved
import numpy as np

def mad(x:np.ndarray) -> bool:
    """

    The median absolute deviation MAD of a ndarray.
    
    Args:
        x (ndarray): A numpy array.

    Returns:
        mad (float): the median absolute deviation of x.
    """
    return np.median(abs(x - np.median(x)))
