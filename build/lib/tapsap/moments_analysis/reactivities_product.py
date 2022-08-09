# reactivities_product
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved
import pandas as pd

def reactivities_product(product_moments: dict, reactant_moments: dict, inert_moments: dict, reactant_reactivities: dict, zone_residence_time: dict, diffusions: list) -> dict:
    """

    Reactivities calculations for a product gas
    Zeroth reactivity is the apparent rate constant.
    First reactivity is the apparent gas uptake-release coefficient.
    Second reactivity is the delay caused by storage on the catalyst.

    Args:
        product_moments (dict | dataframe): A dict of the zeroth, first and second moment of the product.

        inert_moments (dict | dataframe): A dict of the zeroth, first and second moment of the inert.

        reactant_moments (dict | dataframe): A dict of the zeroth, first and second moment of the reactant.

        reactant_reactivities (dict | dataframe): A dict of the zeroth, first and second reactivity coefficients of the reactant.

        diffusions (list): A list of the diffusion coefficients for each gas: [inert_diffusion, reactant_diffusion, product_diffusion].

        zone_residence_time (dict): Residence times for each zone of the reactor.

    Returns:
        product_reactivities (dict): The zeroth, first and second reactivities of the product.

    Cite:
        Constales et al "Precises non-steady-state characterization of solid active materials with no prelimnary mechanistic assumptions"

        Shekhtman et al "'State defining' experiment in chemical kinetics primary characterization of catalyst activity in a TAP experiment"

    Implementor:
        M. Ross Kunz

    See also:
        tapsap.moments_analysis.moments

        tapsap.diffusion.calculate_residence_time

        tapsap.diffusion.calculate_zone_diffusion
    
    Link:
        https://doi.org/10.1016/j.cattod.2017.04.036

        https://doi.org/10.1016/j.ces.2003.08.005
    """
    # Must use normalized moment values to the inert M0, i.e., reactant M0 + product M0 = inert M0
    if isinstance(reactant_moments, pd.DataFrame):
        reactant_moments['M0'] = reactant_moments['M0'].values / inert_moments['M0'].values
        reactant_moments['M1'] = reactant_moments['M1'].values / inert_moments['M0'].values
        reactant_moments['M2'] = reactant_moments['M2'].values / inert_moments['M0'].values
        product_moments['M0'] = product_moments['M0'].values / inert_moments['M0'].values
        product_moments['M1'] = product_moments['M1'].values / inert_moments['M0'].values
        product_moments['M2'] = product_moments['M2'].values / inert_moments['M0'].values

        reactivity_0 = product_moments['M0'].values / (zone_residence_time['zone1'] * reactant_moments['M0'].values)
        reactivity_1 = reactivity_0 * (zone_residence_time['zone2'] / 12 * (8 * reactant_moments['M0'].values + 3 + 9 * diffusions[1] / diffusions[2])
                                    + zone_residence_time['zone1'] * reactant_moments['M0'].values * reactant_reactivities['r1'].values
                                    - product_moments['M1'].values / product_moments['M0'].values)
        reactivity_2 = reactivity_0 / 2 * (product_moments['M2'].values / product_moments['M0'].values
                                        - 19 *
                                        diffusions[1]**2 * zone_residence_time['zone2']**2 /
                                        (16 * diffusions[2]**2)
                                        - 19 * diffusions[1] * zone_residence_time['zone2'] / (16 * diffusions[2]) * (reactivity_0 * (
                                            (3 + 8 * reactant_moments['M0'].values) * zone_residence_time['zone2'] + 12 * reactant_moments['M0'].values * reactant_reactivities['r1'].values * zone_residence_time['zone1']) - 12 * reactivity_1)
                                        + reactivity_1 / (6 * reactivity_0) * (
                                            (3 + 8 * reactant_moments['M0'].values) * zone_residence_time['zone2'] + 12 * reactant_moments['M0'].values * reactant_reactivities['r1'].values * zone_residence_time['zone2'])
                                        - zone_residence_time['zone2']**2 * (
                                            5 / 48 + reactant_moments['M0'].values / 45 * (23 + 40 * reactant_moments['M0'].values))
                                        - reactant_moments['M0'].values / 6 * (3 + 16 * reactant_moments['M0'].values) * reactant_reactivities['r1'].values * zone_residence_time['zone1'] * zone_residence_time['zone2'] - 2 * reactant_moments['M0'].values * zone_residence_time['zone1'] * (reactant_moments['M0'].values * reactant_reactivities['r1']**2 * zone_residence_time['zone1'] - reactant_reactivities['r2'].values))
    else:
        for i in product_moments.keys():
            reactant_moments[i] /= inert_moments['M0']
            product_moments[i] /= inert_moments['M0']

        reactivity_0 = product_moments['M0'] / \
            (zone_residence_time['zone1'] * reactant_moments['M0'])
        reactivity_1 = reactivity_0 * (zone_residence_time['zone2'] / 12 * (8 * reactant_moments['M0'] + 3 + 9 * diffusions[1] / diffusions[2])
                                    + zone_residence_time['zone1'] * reactant_moments['M0'] * reactant_reactivities['r1']
                                    - product_moments['M1'] / product_moments['M0'])
        reactivity_2 = reactivity_0 / 2 * (product_moments['M2'] / product_moments['M0']
                                        - 19 *
                                        diffusions[1]**2 * zone_residence_time['zone2']**2 /
                                        (16 * diffusions[2]**2)
                                        - 19 * diffusions[1] * zone_residence_time['zone2'] / (16 * diffusions[2]) * (reactivity_0 * (
                                            (3 + 8 * reactant_moments['M0']) * zone_residence_time['zone2'] + 12 * reactant_moments['M0'] * reactant_reactivities['r1'] * zone_residence_time['zone1']) - 12 * reactivity_1)
                                        + reactivity_1 / (6 * reactivity_0) * (
                                            (3 + 8 * reactant_moments['M0']) * zone_residence_time['zone2'] + 12 * reactant_moments['M0'] * reactant_reactivities['r1'] * zone_residence_time['zone2'])
                                        - zone_residence_time['zone2']**2 * (
                                            5 / 48 + reactant_moments['M0'] / 45 * (23 + 40 * reactant_moments['M0']))
                                        - reactant_moments['M0'] / 6 * (3 + 16 * reactant_moments['M0']) * reactant_reactivities['r1'] * zone_residence_time['zone1'] * zone_residence_time['zone2'] - 2 * reactant_moments['M0'] * zone_residence_time['zone1'] * (reactant_moments['M0'] * reactant_reactivities['r1']**2 * zone_residence_time['zone1'] - reactant_reactivities['r2']))

    result = {
        'r0':reactivity_0,
        'r1':reactivity_1,
        'r2':reactivity_2
    }
    return result
