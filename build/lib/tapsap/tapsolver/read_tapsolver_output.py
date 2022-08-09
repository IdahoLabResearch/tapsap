# read_tapsolver_output
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

import pandas as pd
from tapsap import structures
from tapsap import tapsolver
import glob
import numpy as np

def read_tapsolver_output(simulation:tapsolver.Simulation) -> list:
    """

    Takes an input directory path and reads the tapsolver output file.  This function then coverts the output to a list of transient objects.
    
    Args:
        
        input_path (str): The path or file name to read the input file.

    Returns:
        species_data (list): A list of transient objects.

    Citation:
        Yonge et al, "TAPsolver: A Python package for the simulation and analysis of TAP reactor experiments"

    Implementor:
        M. Ross Kunz

    Link:
        https://doi.org/10.1016/j.cej.2021.129377

        https://arxiv.org/abs/2008.13584

    See also:
        tapsap.tapsolver.Simulation

        tapsap.structures.Transient
    """ 
    species_data = []

    flux_dir = simulation.output_folder_name + '_folder/flux_data/*.csv'
    thin_dir = simulation.output_folder_name + '_folder/thin_data/*.csv'
    flux_files = glob.glob(flux_dir)
    thin_files = glob.glob(thin_dir)

    feed_names = list(simulation.feed_names.values())
    surface_names = list(simulation.surface_names.values())
    surface_times = None

    for i in flux_files:
        data = pd.read_csv(i, header=None)        
        temp_species = structures.Transient()

        temp_name = i.split('/')
        temp_name = (temp_name[len(temp_name) - 1]).split('.')[0]
        feed_index = 'feed_' + str(np.where(feed_names == temp_name)[0])
        num_pulses = data.shape[1] - 1
        init_moments = {
            'pulse_number': list(range(num_pulses)),
            'temperature': [simulation.reaction_temperature] * num_pulses
        }
        if surface_times is None:
            surface_times = data.iloc[:,0].values

        temp_species.name = temp_name
        temp_species.mass = simulation.feed_mass[feed_index]
        temp_species.delay_time = simulation.feed_time[feed_index]
        temp_species.flux = data.iloc[:,1:num_pulses]
        temp_species.times = data.iloc[:,0].values
        temp_species.diffusion = simulation.reference_diffusion_inert * np.sqrt(temp_species.mass / simulation.reference_mass)
        temp_species.amount_pulsed = simulation.feed_intensity[feed_index]
        temp_species.initial_concentration = 0
        temp_species.num_pulse = num_pulses
        temp_species.df_moments = init_moments
        temp_species.reactor = simulation.to_reactor()
        temp_species.reference_gas = None
        temp_species.integration_times = [min(temp_species.times), max(temp_species.times)]

        species_data.append(temp_species)

    for i in thin_files:
        data = pd.read_csv(i, header=None)        
        temp_species = structures.Transient()

        temp_name = i.split('/')
        temp_name = (temp_name[len(temp_name) - 1]).split('.')[0]

        # The name in the thin data can either be the surface concentration, gas concentration, or rate.
        # A csv name that matches any of the surface names will be a surface concentration.
        # A csv name without any active site indicators, e.g., '*', is going to be the gas concentration.
        # A csv name with r_ will be the rate of a species.

        species_indicator = 'concentration_'
        is_feed = True
        if 'r_' not in temp_name:
            if temp_name in surface_names:
                # surface concentration
                temp_index = 'surface_' + str(np.where(surface_names == temp_name)[0])
                is_feed = False
            else:
                # gas concentration
                temp_index = 'feed_' + str(np.where(feed_names == temp_name)[0])
        else:
            species_indicator = 'rate_'
            sub_temp_name = temp_name.split('_')[1]
            if temp_name in surface_names:
                # surface concentration
                temp_index = 'surface_' + str(np.where(surface_names == sub_temp_name)[0])
                is_feed = False
            else:
                # gas concentration
                temp_index = 'feed_' + str(np.where(feed_names == sub_temp_name)[0])

        full_name = species_indicator + temp_name

        num_pulses = data.shape[1]
        init_moments = {
            'pulse_number': list(range(num_pulses)),
            'temperature': [simulation.reaction_temperature] * num_pulses
        }

        temp_species.name = full_name
        if is_feed:
            temp_species.amount_pulsed = simulation.feed_intensity[temp_index]
            temp_species.mass = simulation.feed_mass[temp_index]
            temp_species.delay_time = simulation.feed_time[temp_index]
            temp_species.diffusion = simulation.reference_diffusion_inert * np.sqrt(temp_species.mass / simulation.reference_mass)
        else:
            temp_species.initial_concentration = simulation.surface_initial_concentration[temp_index]
        
        temp_species.flux = data
        temp_species.times = surface_times        
        temp_species.num_pulse = num_pulses
        temp_species.df_moments = init_moments
        temp_species.reactor = simulation.to_reactor()
        temp_species.reference_gas = None
        temp_species.integration_times = [min(surface_times), max(surface_times)]

        species_data.append(temp_species)

    new_experiment = structures.Experiment()

    new_experiment.file_name = 'TAPsolver_simulation'
    new_experiment.collection_time = max(surface_times)
    new_experiment.pulse_spacing = 0
    new_experiment.time_start = min(surface_times)
    new_experiment.time_end = max(surface_times)
    new_experiment.num_samples_per_pulse = 1
    new_experiment.species_data = species_data
    new_experiment.reactor = simulation.to_reactor()
    new_experiment.species_class = {'inert':None, 'reactants': None, 'products':None}

    return species_data    