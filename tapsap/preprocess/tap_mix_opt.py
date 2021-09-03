# tap_mix_opt
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

import numpy as np
from scipy.optimize import minimize


def tap_mix_opt(X: np.ndarray, y: np.ndarray) -> dict:
    """

    This is an alteration of tap_mix, but with a simple solver.
    In some cases, the convex solver fails and if it does, this method should be applied.
    Optimization of the calibration coefficient or fragmentation.
    For example, given an inert and reactant, then y (of length n) would be the inert and X would be a matrix of a single flux with a shape of n by 1.
    This can also be used to extract fragmentation patterns from a single mass measurement.
    
    Args:
        X (float ndarray): A set of flux responses used in describing y.

        y (float ndarray): The flux that contains all of X.

    Returns:
        corrected_flux, calibration_amount (dict): The calibration corrected flux and the calibration amount. 

    Citation:
        Kunz et al, "A Priori Calibration of Transient Kinetics Data via Machine Learning" (In prep)

    Implementor:
        M. Ross Kunz

    Link:
        Kunz et al, "A Priori Calibration of Transient Kinetics Data via Machine Learning" (In prep)
    """
    def fit_beta_hat(betaHat, y, X):
            betaHat = np.array([betaHat]).transpose()
            
            temp_residuals = y - np.array(X @ betaHat).flatten()
            temp_objective = np.sqrt(np.mean(temp_residuals**2))
            min_residual = min(temp_residuals)
            internal_m0 = sum(temp_residuals)
            
            if ((min_residual < min(y)) | (internal_m0 < 0)):
                temp_objective = abs(temp_objective) + 1e3
            
            return temp_objective

    if len(X.shape) == 1:
        X = np.array([X]).transpose()

    p = X.shape[1]
    max_of_x = [max(X[:, i]) for i in range(p)]
    max_of_y = max(y)
    upper_bound = [max([max_of_y / i, 1e-5]) for i in max_of_x]
    initial_beta = [i / 2 for i in upper_bound]
    bounds = tuple([(0, i) for i in upper_bound])
    fit = minimize(fit_beta_hat, initial_beta, args =(y, X), bounds=bounds)
    fit_coefs = fit.x
    fit_list = list(fit_coefs)
    fitted_values = np.array(X @ np.array([fit_coefs]).transpose()).flatten()

    result = {
        'flux':fitted_values,
        'calibration_coef':fit_list
    }

    return result