# tap_mix
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

import numpy as np
import cvxpy as cp
import warnings
import copy
from tapsap import preprocess, utils


def tap_mix(X: np.ndarray, y: np.ndarray, times: np.ndarray, huber_loss: bool = False, constraints: bool = True, fit_intercept:bool = True) -> dict:
    """

    Optimization of the calibration coefficient or fragmentation.
    This method is a convex optimization fitting the response (y) to a single or set of flux.
    For example, given an inert and reactant, then y (of length n) would be the inert and X would be a matrix of a single flux with a shape of n by 1.
    This can also be used to extract fragmentation patterns from a single mass measurement.
    
    Args:
        X (float ndarray): A set of flux responses used in describing y.

        y (float ndarray): The flux that contains all of X.

        times (float ndarray): An array of time.

        huber_loss (bool): Use a robust loss function rather than the standard square error loss.

        constraints (bool): Apply the molecule constraints. If false, tap_mix performs regular linear regression.

        fit_intercept (bool): Fit the intercept within the convex optimization.

    Returns:
        corrected_flux, calibration_amount (dict): The calibration corrected flux and the calibration amount. 

    Citation:
        TODO TEAK

    Implementor:
        M. Ross Kunz

    Link:
        TODO TEAK
    """
    
    if len(X.shape) == 1:
        flux_ci = np.median(X) + 6 * utils.mad(X)
        flux_max = np.max(X)
        if flux_max < flux_ci:
            result = {
                'flux':X,
                'intercept':0,
                'calibration_coef':1,
                'all_coefs': []
            }
            return result


        X = np.array([X]).transpose()
        
                
    # including the intercept
    n = X.shape[0]
    if fit_intercept:
        intercept = np.array([np.ones(n)])
        X = np.concatenate((intercept.T, X), axis = 1)

    p = X.shape[1]
    orig_y = y
    orig_X = copy.deepcopy(X)

    sum_y = y.sum()
    m0_X = [sum(i) / sum_y for i in X.transpose()]
    m0_X = np.array([m0_X])

    warnings.filterwarnings("ignore", category=DeprecationWarning)
    beta_hat = cp.Variable(p)
    resids = y - X @ beta_hat
    if huber_loss:
        objective = cp.Minimize(cp.sum(cp.huber(resids, M=1e-5)))
    else:
        objective = cp.Minimize(cp.sum_squares(resids))  # resids

    if fit_intercept:
        temp_constraints = [
            beta_hat[1:p] >= 0,
            #(np.sum(m0_X * beta_hat[1:p]) + cp.sum(resids) / sum_y) <= 1,
            cp.sum(resids) * (times[1] - times[0]) >= 1e-5,
            resids >= (orig_y.min() * 2)
        ]
    else:
        temp_constraints = [
            beta_hat >= 0,
            #(np.sum(m0_X * beta_hat[1:p]) + cp.sum(resids) / sum_y) <= 1,
            cp.sum(resids) * (times[1] - times[0]) >= 1e-5,
            resids >= (orig_y.min() * 2)
        ]
        
    if constraints:
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        prob = cp.Problem(objective, temp_constraints)
    else:
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        prob = cp.Problem(objective)

    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    prob.solve(solver=cp.ECOS)

    warnings.filterwarnings("ignore", category=DeprecationWarning)
    fit_coefs = beta_hat.value
    fit_list = [float(i) for i in fit_coefs]
    fitted_values = orig_X @ fit_coefs
    #fit_rmse = utils.rmse(y, fitted_values)

    # if sum(fit_list) < 0.01:
    #     opt_result = preprocess.tap_mix_opt(X, y)
    #     opt_rmse = utils.rmse(y, opt_result['flux'])

    if fit_intercept:
        result = {
            'flux':fitted_values,
            'intercept':fit_list[0],
            'calibration_coef':fit_list[1],
            'all_coefs': fit_list
        }
    else:
        result = {
            'flux':fitted_values,
            'intercept':0,
            'calibration_coef':fit_list[0],
            'all_coefs': fit_list
        }

    # if sum(fit_list) < 0.01:
    #     if opt_rmse < fit_rmse:
    #         result = opt_result

    return result
