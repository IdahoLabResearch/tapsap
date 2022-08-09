# gamma_pdf
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

from numpy import ndarray, exp
from math import gamma


def gamma_pdf(times: ndarray, shape: float, scale: float) -> ndarray:
    """

    Generates the gamma distribution Probability Density Function (PDF) based on the given times, shape and scale (note that the rate is equal to 1/scale).
    
    Args:
        times (float ndarray): An array of time.

        shape (float): The shape parameter of the gamma distribution.

        scale (float): The scale parameter of the gamma distribution.

    Returns:
        pdf (float ndarray): The PDF of the generated gamma distribution.

    Citation:
        Casella & Berger, Statistical Inference.

    Implementor:
        M. Ross Kunz

    Link:
        https://en.wikipedia.org/wiki/Gamma_distribution
    """
    pdf = 1 / (gamma(float(shape)) * scale**shape) * \
        times**(shape - 1) * exp(-times / scale)
    return pdf
