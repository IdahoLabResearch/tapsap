# rmse
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved
from numpy import ndarray, mean, sqrt


def rmse(x: ndarray, y: ndarray) -> float:
    """
    A function for the root mean square error between two arrays.

    Args:
        x (ndarray): An array of values.

        y (ndarray): An array of values.

    Returns:
        rmse_error (float): The root mean square error between x and y.
    """
    rmse_error = sqrt(mean((x - y)**2))
    return rmse_error
