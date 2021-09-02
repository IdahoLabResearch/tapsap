# calibration_teak
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

from numpy import ndarray
from tapsap import moments_analysis, preprocess, utils


def calibration_teak(flux: ndarray, inert_flux: ndarray, times: ndarray, flux_mass: float, inert_mass: float, huber_loss: bool = False, constraints:bool = True) -> dict:
    """

    This function determines the calibration coefficients for the flux based on the inert flux.
    Note that if the flux is a product, the difference between the inert and the calibrated reactant should be used as the flux value.
    For example, (Inert - Reactant) >= Product.
    
    Args:
        reactant_flux (float ndarray or list of ndarrays): The outlet flux of the reactant.

        product_flux (float ndarray or list of ndarrays): The outlet flux of the product.

        inert_flux (float ndarray): The outlet flux of the inert.

        times (float ndarray): An array of time.

        flux_mass (float): The mass of the flux.

        inert_mass (float): The mass of the inert flux.

        huber_loss (bool): Use a robust loss function rather than the standard square error loss.

        constraints (bool): Apply the molecule constraints. If false, tap_mix performs regular linear regression.

    Returns:
        [corrected_flux, calibration_amount] (dict): The calibration corrected flux and the calibration amount. 

    Citation:
        TODO TEAK

    Implementor:
        M. Ross Kunz

    See also:
        tapsap.preprocess.tap_mix

        tapsap.moments.isreversible

    Link:
        TODO TEAK
    """
    inert_area = utils.trapz(inert_flux, times)
    flux_area = utils.trapz(flux, times)
    # check if the flux is reversible
    if moments_analysis.isreversible(flux, times, inert_flux, flux_mass, inert_mass):
        calibration_coef = inert_area / flux_area
        new_flux = flux * calibration_coef

        result = {
            'flux':new_flux, 
            'calibration_coef':calibration_coef
        }
        return result
    else:
        result = preprocess.tap_mix(
            flux, inert_flux, times, huber_loss, constraints)
        result['calibration_coef'] = result['calibration_coef']

    return result
