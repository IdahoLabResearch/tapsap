# baseline correction
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

from numpy import floor, ndarray


def baseline_correction(flux: ndarray, times: ndarray, baseline_time_range: list = None, baseline_amount: float = None) -> dict:
    """

    Baseline correction of the flux through user input.
    The user can either provide a list of baseline time ranges ([start, end]), the baseline amount (0.2), or neither where the last 95% of the flux will be taken as the baseline.
    
    Args:
        flux (float ndarray): The outlet flux.

        times (float ndarray): An array of time.

        baseline_time_range (float list): The points in time in which to take the baseline.

        baseline_amount (float): The amount of baseline correction to apply.

    Returns:
        corrected_flux, baseline_amount (dict): The baseline corrected flux and the baseline amount.

    Citation:
        None

    Implementor:
        M. Ross Kunz

    Link:
        None

    """
    if baseline_time_range is not None:
        baseline_time_range.sort()

    if baseline_amount is None:
        if baseline_time_range is not None:
            baseline_start_index = abs(times - baseline_time_range[0]).argmin()
            baseline_end_index = abs(times - baseline_time_range[1]).argmin()
        else:
            baseline_start_index = int(floor(len(times) * 0.95))
            baseline_end_index = len(times)

        baseline_amount = (
            flux[baseline_start_index:baseline_end_index]).mean()

    corrected_flux = flux - baseline_amount
    result = {
        'flux':corrected_flux,
        'baseline_amount':baseline_amount
    }
    return result
