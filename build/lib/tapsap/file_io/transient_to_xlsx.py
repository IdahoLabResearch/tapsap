# transient_to_xlsx
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

import pandas as pd
from tapsap import structures


def transient_to_xlsx(species_data: structures.Transient) -> pd.DataFrame:
    """

    This function takes a Transient class and returns the information flux, concentration, rate information into a data frame.
    The final option (excel_format) includes the temperature as well as the other gas information such as name, mass and gain ect.
    
    Args:
        species_data (class Transient Series): A collection of transient information used to describe a gas species.

        excel_format (bool): Returning a data frame that can be exported to excel including temperature, name, mass, ect.

    Returns:
        gas_df (DataFrame): The species_data as a data frame. 


    Implementor:
        M. Ross Kunz

    Link:
        None
    """
    times = [0] + list(species_data.times)
    len_times = len(times)
    series_dict = {
        'Key': ['name', 'amu', 'gain', 'delay_time'] + ['None'] * (len_times - 4),
        'Value': [species_data.name, species_data.mass, species_data.gain, species_data.delay_time] + ['None'] * (len_times - 4),
        'Time': times
    }
    data_df = species_data.flux
    data_df.loc[0.5] = species_data.df_moments['temperature'].values
    data_df = data_df.sort_index().reset_index(drop=True)
    data_df = pd.concat([pd.DataFrame.from_dict(series_dict), data_df], axis=1)

    return data_df
