# read_xlsx
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

from tapsap.structures import Experiment, Transient
import pandas as pd
from tapsap.utils import filter_xl


def read_xlsx(file_name: str) -> Experiment:
    """

    A function for reading an excel file to a tapsap Experiment object.
    
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

    Link:
        None

    """
    new_experiment = Experiment()
    # reading in the data
    data = pd.ExcelFile(file_name)
    all_sheets = data.sheet_names
    gas_sheets = all_sheets[3:]
    # setting the experiment object
    df = data.parse('experiment')
    df_keys = df['Key']
    for i, key in enumerate(df_keys):
        setattr(new_experiment, str(key), filter_xl(df['Value'][i]))

    # setting the reactor object
    df = data.parse('reactor')
    df_keys = df['Key']
    for i, key in enumerate(df_keys):
        setattr(new_experiment.reactor, key, filter_xl(df['Value'][i]))


    # setting all of the gas information
    for gas in gas_sheets:
        df = data.parse(gas)
        new_transient = Transient()
        # TODO this could be enhanced
        new_transient.name = (df['Value'])[0]
        new_transient.mass = float((df['Value'])[1])
        new_transient.gain = float((df['Value'])[2])
        new_transient.delay_time = float((df['Value'])[3])
        times = (df['Time'])[1:]
        pulse_ids = (df.keys())[3:]
        temperature_values = df.iloc[0, 3:]
        flux = df.iloc[1:, 3:]
        new_transient.flux = flux
        init_moments = {
            'pulse_number': pulse_ids,
            'temperature': temperature_values
        }
        new_transient.df_moments = pd.DataFrame.from_dict(init_moments)
        new_transient.times = times
        new_transient.reactor = new_experiment.reactor
        new_transient.integration_times = [0, max(times)]
        new_transient.num_pulse = flux.shape[1]
        new_experiment.species_data[new_transient.name] = new_transient

    return new_experiment
