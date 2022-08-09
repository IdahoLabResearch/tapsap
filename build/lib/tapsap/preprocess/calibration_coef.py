# calibration_coef
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

from numpy import ndarray


def calibration_coef(flux: ndarray, calibration_amount: float = None) -> dict:
    """

    Apply calibration correction to the flux through user input.
    This will result in a value of the flux multiplied by the calibration amount.
    
    Args:
        flux (float ndarray): The outlet flux.

        calibration_amount (float): The amount to scale the flux.

    Returns:
        corrected_flux, calibration_amount (dict): The calibration corrected flux and the calibration amount.

    Citation:
        None

    Implementor:
        M. Ross Kunz

    Link:
        None

    """

    corrected_flux = flux * calibration_amount

    result = {
        'flux':corrected_flux,
        'calibration_coef':calibration_amount,
        'intercept': 0
    }
    return result
