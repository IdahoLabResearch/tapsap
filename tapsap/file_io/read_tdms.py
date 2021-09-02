# read_tdms
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

from tapsap import structures
from nptdms import TdmsFile
from numpy import unique, array
import pandas as pd


def read_tdms(file_name: str) -> structures.Experiment:
    """

    A function for reading a tdms file to a tapsap Experiment object.
    Requires the use of the python package 'nptdms' for use.
    
    Args:
        file_name (str): The path to the TDMS file that is to be read.

    Returns:
        experiment (Experiment): A object containing all of the TDMS information.

    Citation:
        None

    Implementor:
        M. Ross Kunz

    See also:
        tapsap.file_io.Experiment

        tapsap.file_io.Transient

    Link:
        None

    """
    new_experiment = structures.Experiment()
    new_experiment.file_name = file_name
    base_file = TdmsFile(file_name).as_dataframe()

    meta_data = base_file.filter(regex='Meta Data')
    df = meta_data.dropna()
    df_names = list(df.keys())
    amu_values = [i for i, item_name in enumerate(
        df[df_names[0]]) if 'AMU' in item_name]
    pulse_spacing = [i for i, item_name in enumerate(
        df[df_names[0]]) if 'Pulse Spacing' in item_name]
    pulse_spacing = pulse_spacing[0]
    new_experiment.pulse_spacing = float(df[df_names[1]][pulse_spacing])
    collection_time = [i for i, item_name in enumerate(
        df[df_names[0]]) if 'Collection Time' in item_name]
    collection_time = collection_time[0]
    new_experiment.collection_time = float(df[df_names[1]][collection_time])

    # get the group info which corresponds to the names of each individual measured mass
    tdms_names = tdms_names = base_file.keys()
    tdms_names_split = [str(i).replace("'", "") for i in tdms_names]
    tdms_names_split = [str(i).split("/") for i in tdms_names_split]
    group_info = [i[1] for i in tdms_names_split]
    unique_group_info = list(unique(array(group_info)))
    # removing secondary and meta data where the remainder are the individual measured masses
    unique_group_info = unique_group_info[:len(unique_group_info) - 2]

    for i, group_value in enumerate(unique_group_info):
        gas_mass = df[df_names[1]][i]
        gas_name = 'AMU_' + str(gas_mass) + '_1'
        all_gas_names = new_experiment.species_data.keys()
        if gas_name in all_gas_names:
            current_set = [
                temp_val for temp_val in all_gas_names if gas_name in temp_val]
            gas_name = 'AMU_' + str(gas_mass) + '_' + str(len(current_set) + 1)

        group_locs = [j for j, temp_val in enumerate(
            group_info) if temp_val == group_value]
        # subset the data based on the group locations
        group_df = base_file.iloc[:, group_locs]
        num_rows = group_df.shape[0]
        time_values = array(group_df.iloc[:(num_rows - 1), 2]).flatten()
        temperature_values = list(group_df.iloc[0, 3:])
        flux_df = group_df.iloc[1:, 3:]
        pulse_index = [str((i.split('/')[2]).replace("'", ""))
                       for i in flux_df.keys()]
        flux_df.columns = pulse_index
        # set experiment values
        if i == 0:
            new_experiment.num_samples_per_pulse = len(time_values)
            new_experiment.time_start = min(time_values)
            new_experiment.time_end = max(time_values)
        # creation of the transient
        new_species = structures.Transient()
        new_species.name = gas_name
        new_species.mass = float(gas_mass)
        new_species.gain = float(df[df_names[1]][i + len(amu_values)])
        new_species.delay_time = float(df[df_names[1]][2*len(amu_values)])
        new_species.flux = flux_df
        new_species.times = time_values
        new_species.num_pulse = flux_df.shape[1]
        new_species.integration_times = [0, max(time_values)]
        init_moments = {
            'pulse_number': [int(i) for i in pulse_index],
            'temperature': temperature_values
        }
        new_species.df_moments = pd.DataFrame.from_dict(init_moments)
        new_experiment.species_data[gas_name] = new_species

    return new_experiment
