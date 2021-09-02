# transient_to_xlsx_summary
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

import pandas as pd
from tapsap import structures


def transient_to_xlsx_summary(species_data: structures.Transient) -> pd.DataFrame:
    """

    This function takes a Transient class dataframe of moment information into a excel style data frame.
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
    series_dict = {
        'Key': ['name', 'amu', 'gain', 'delay_time'] + ['None'] * (species_data.num_pulse - 4),
        'Value': [species_data.name, species_data.mass, species_data.gain, species_data.delay_time] + ['None'] * (species_data.num_pulse - 4)
    }
    gas_df = pd.concat([pd.DataFrame.from_dict(
        series_dict), species_data.df_moments], axis=1)

    return gas_df
