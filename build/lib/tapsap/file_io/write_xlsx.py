# write_xlsx
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

import pandas as pd
from tapsap import file_io, structures


def write_xlsx(experiment: structures.Experiment, output_file_name: str = 'results.xlsx', data_type: str = 'flux') -> None:
    """

    This function converts a TAP Experiment object to an Excel spread sheet.

    Args:
        experiment (class Experiment): The Experiment class from tapsap holding all of the kinetic information.

        data_type (str): A string containing which type of information you would like to save. Options: flux, summary

        output_file_name (str): The path in which you would like to save the excel document.

    Returns:
        None

    Citation:
        None

    Implementor:
        M. Ross Kunz

    """
    if data_type not in ['flux', 'summary']:
        raise ValueError(
            "data_type must be either flux or summary")
    experiment_df = file_io.experiment_to_df(experiment)
    reactor_df = file_io.reactor_to_df(experiment.reactor)

    with pd.ExcelWriter(output_file_name) as writer:
        experiment_df.to_excel(writer, sheet_name='experiment', index=False)
        reactor_df.to_excel(writer, sheet_name='reactor', index=False)
        for i in experiment.species_data.keys():
            temp_species = experiment.species_data[i]
            if data_type == 'summary':
                species_data_df = file_io.transient_to_xlsx_summary(
                    temp_species, excel_format=True)
            else:
                species_data_df = file_io.transient_to_xlsx(
                    temp_species)

            species_data_df.to_excel(
                writer, sheet_name=temp_species.name, index=False)
