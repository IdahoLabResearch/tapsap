# calculate_residence_time
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

def calculate_residence_time(zone_lengths: dict, zone_porosity: dict, zone_diffusion: dict) -> dict:
    """

    Calculate the residence time within the each zone in the reactor.
    Please note that some manuscripts either invert the residence time or scale by a factor of one half.
    This residence time calculation is done via Constales et al.
    See other citations to note the difference in implementation.
    
    Args:
        zone_lengths (dict): The zone lengths for the reactor, e.g., {0.002, 0.000001, 0.002}

        zone_diffusion (dict): The diffusion coefficient for each zone

        zone_porosity (dict): The bed porosity within each zone

    Returns:
        zone_residence_time (dict): The residence time within each zone

    Citation:
        Constales et al, "Precises non-steady-state characterization of solid active materials with no prelimnary mechanistic assumptions"

        Gleaves et al, "TAP-2: An interrogative kinetics approach"

        Yablonsky et al, "The Y-procedure: How to extract the chemical transformation rate from reaction–diffusion data with no assumption on the kinetic model"

    Implementor:
        M. Ross Kunz

    Link:
        https://doi.org/10.1016/j.cattod.2017.04.036

        https://doi.org/10.1016/S0926-860X(97)00124-5

        https://doi.org/10.1016/j.ces.2007.04.050
    """

    inert_zone_0 = zone_porosity['zone0'] * (zone_lengths['zone0'] +
                                       zone_lengths['zone2'])**2 / (2 * zone_diffusion['zone0'])
    catalyst_zone = zone_lengths['zone1'] * (
        zone_lengths['zone0'] + zone_lengths['zone2']) / (2 * zone_diffusion['zone1'])
    inert_zone_1 = zone_porosity['zone2'] * (zone_lengths['zone0'] +
                                       zone_lengths['zone2'])**2 / (2 * zone_diffusion['zone2'])

    result = {
        'zone0':inert_zone_0,
        'zone1':catalyst_zone,
        'zone2':inert_zone_1
    }
    return result
