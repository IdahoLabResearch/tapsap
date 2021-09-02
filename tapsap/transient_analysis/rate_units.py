# rate_units
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

import numpy as np

def rate_units(mol_per_pulse:float = 1, catalyst_weight:float = 1) -> float:
    """

    Calculation of the concentration via the G-Procedure. 
    
    Args:
        mol_per_pulse (float): The mol per injection.

        catalyst_weight (float): The weight of the catalyst
      

    Returns:
        units (float): The units units (mol/m2/s).

    Citation:
        Yablonsky et al, "The Y-procedure: How to extract the chemical transformation rate from reaction–diffusion data with no assumption on the kinetic model"

        Redekop et al, "The Y-Procedure methodology for the interpretation of transient kinetic data: Analysis of irreversible adsorption"

        Kunz et al, "Pulse response analysis using the Y-procedure: A data science approach"

        Kunz et al, "Probability theory for inverse diffusion: Extracting the transport/kinetic time-dependence from transient experiments"

    Implementor:
        M. Ross Kunz

    Link:
        https://doi.org/10.1016/j.ces.2007.04.050

        https://doi.org/10.1016/j.ces.2011.08.055

        https://doi.org/10.1016/j.ces.2018.06.078

        https://doi.org/10.1016/j.cej.2020.125985
    """
    units = mol_per_pulse / catalyst_weight
    return units