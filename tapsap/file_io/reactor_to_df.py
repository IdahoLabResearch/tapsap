# reactor_to_df
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

import pandas as pd
from tapsap import structures


def reactor_to_df(reactor_data: structures.Reactor) -> pd.DataFrame:
    """

    This function takes a Reactor class and returns a data frame.
    
    Args:
        reactor_data (class Reactor): A Reactor data class.

    Returns:
        reactor_df (DataFrame): The reactor_data as a data frame. 


    Implementor:
        M. Ross Kunz

    Link:
        None
    """
    reactor_keys = ['zone_lengths', 'zone_porosity', 'zone_diffusion', 'zone_residence_time',
                    'reactor_radius', 'catalyst_weight', 'mol_per_pulse']
    reactor_values = [str(getattr(reactor_data, i)) for i in reactor_keys]
    reactor_dict = {
        'Key': reactor_keys,
        'Value': reactor_values
    }
    reactor_df = pd.DataFrame(reactor_dict)

    return reactor_df
