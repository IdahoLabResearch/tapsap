# experiment_to_df
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

import pandas as pd
from pandas import DataFrame
from tapsap import structures


def experiment_to_df(experiment_data: structures.Experiment) -> DataFrame:
    """

    This function takes a experiment class and returns a data frame.
    
    Args:
        experiment_data (class Experiment): A Experiment data class.

    Returns:
        experiment_df (DataFrame): The experiment_data as a data frame. 


    Implementor:
        M. Ross Kunz

    Link:
        None
    """
    experiment_keys = ['file_name', 'collection_time', 'pulse_spacing',
                       'time_start', 'time_end', 'num_samples_per_pulse']
    experiment_values = [str(getattr(experiment_data, i))
                         for i in experiment_keys]
    experiment_dict = {
        'Key': experiment_keys,
        'Value': experiment_values
    }
    experiment_df = pd.DataFrame(experiment_dict)

    return experiment_df
