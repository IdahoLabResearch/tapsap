# uptake
# Copyright 2022, Battelle Energy Alliance, LLC All Rights Reserved

import numpy as np

def uptake(rate: np.ndarray, times: np.ndarray) -> np.ndarray:
    """

    Calculation of the uptake as the cumulative integral of the rate. The rate can be given from previous calculations or by the Y or G Procedure
    
    Args:
        rate (float ndarray): The gas rate (temporal) of the given flux.

        times (float ndarray): An array of time.

    Returns:
        uptake (float ndarray): The uptake (temporal) of the given rate.

    Citation:
        Yablonsky et al, "The Y-procedure: How to extract the chemical transformation rate from reaction–diffusion data with no assumption on the kinetic model"

        Redekop et al, "The Y-Procedure methodology for the interpretation of transient kinetic data: Analysis of irreversible adsorption"

        Kunz et al, "Pulse response analysis using the Y-procedure: A data science approach"

    Implementor:
        M. Ross Kunz

    Link:
        https://doi.org/10.1016/j.ces.2007.04.050

        https://doi.org/10.1016/j.ces.2011.08.055

        https://doi.org/10.1016/j.ces.2018.06.078

    """

    uptake = rate.cumsum() * max(times) / len(times)

    return uptake
