# reactivities_reactant
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

import pandas as pd

def reactivities_reactant(reactant_moments: dict, inert_moments: dict, zone_residence_time: dict) -> dict:
    """
    
    Reactivities calculations for a reactant gas.
    Zeroth reactivity is the apparent rate constant.
    First reactivity is the apparent gas uptake-release coefficient.
    Second reactivity is the delay caused by storage on the catalyst.

    Args:
        reactant_moments (dict | dataframe): A dictionary of the zeroth, first and second moment of the reactant.

        inert_moments (dict | dataframe): A dictionary of the zeroth, first and second moment of the inert.

        zone_residence_time (dict): Residence times for each zone of the reactor.

    Returns:
        reactant_reactivities (dict): The reactivity coefficients of the reactant.

    Citation:
        Constales et al "Precises non-steady-state characterization of solid active materials with no prelimnary mechanistic assumptions"

        Shekhtman et al "'State defining' experiment in chemical kinetics primary characterization of catalyst activity in a TAP experiment"

    Implementor:
        M. Ross Kunz

    See also:
        tapsap.moments_analysis.moments

        tapsap.diffusion.calculate_residence_time

    Link:
        https://doi.org/10.1016/j.cattod.2017.04.036

        https://doi.org/10.1016/j.ces.2003.08.005
    """
    # Must use normalized moment values to the inert M0, i.e., reactant M0 + product M0 = inert M0
    if isinstance(reactant_moments, pd.DataFrame):
        reactant_moments['M0'] = reactant_moments['M0'].values / inert_moments['M0'].values
        reactant_moments['M1'] = reactant_moments['M1'].values / inert_moments['M0'].values
        reactant_moments['M2'] = reactant_moments['M2'].values / inert_moments['M0'].values

        reactivity_0 = -1 / zone_residence_time['zone1'] + 1 / (zone_residence_time['zone1'] * reactant_moments['M0'].values)
        reactivity_1 = (-2 * zone_residence_time['zone2'] / (3 * zone_residence_time['zone1'])
                        - zone_residence_time['zone2'] / (3 * zone_residence_time['zone1'] * reactant_moments['M0'].values)
                        + reactant_moments['M1'].values / (zone_residence_time['zone1'] * reactant_moments['M0'].values**2))
        reactivity_2 = (4 * zone_residence_time['zone2']**2 / (45 * zone_residence_time['zone1'])
                        + 7 *
                        zone_residence_time['zone2']**2 /
                        (90 * zone_residence_time['zone1'] * reactant_moments['M0'].values)
                        - zone_residence_time['zone2'] * reactant_moments['M1'].values /
                        (3 * zone_residence_time['zone1'] * reactant_moments['M0'].values**2)
                        - reactant_moments['M2'].values / (2 * zone_residence_time['zone1'] * reactant_moments['M0'].values**2)
                        + reactant_moments['M1'].values**2 / (zone_residence_time['zone1'] * reactant_moments['M0'].values**3))
    else:
        for i in reactant_moments.keys():
            reactant_moments[i] = reactant_moments[i] / inert_moments['M0']

        reactivity_0 = -1 / zone_residence_time['zone1'] + 1 / (zone_residence_time['zone1'] * reactant_moments['M0'])
        reactivity_1 = (-2 * zone_residence_time['zone2'] / (3 * zone_residence_time['zone1'])
                        - zone_residence_time['zone2'] / (3 * zone_residence_time['zone1'] * reactant_moments['M0'])
                        + reactant_moments['M1'] / (zone_residence_time['zone1'] * reactant_moments['M0']**2))
        reactivity_2 = (4 * zone_residence_time['zone2']**2 / (45 * zone_residence_time['zone1'])
                        + 7 *
                        zone_residence_time['zone2']**2 /
                        (90 * zone_residence_time['zone1'] * reactant_moments['M0'])
                        - zone_residence_time['zone2'] * reactant_moments['M1'] /
                        (3 * zone_residence_time['zone1'] * reactant_moments['M0']**2)
                        - reactant_moments['M2'] / (2 * zone_residence_time['zone1'] * reactant_moments['M0']**2)
                        + reactant_moments['M1']**2 / (zone_residence_time['zone1'] * reactant_moments['M0']**3))

    result = {
        'r0':reactivity_0,
        'r1':reactivity_1,
        'r2':reactivity_2
    }
    return result
