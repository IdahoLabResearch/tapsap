# write_tapsolver_input
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved


from tapsap import tapsolver
import numpy as np
import pandas as pd

def write_tapsolver_input(tapsolver_simualtion:tapsolver.Simulation, save_path:str = 'tapsolver_input.csv') -> None:
    """

    Takes a tapsolver simulation object and saves an input csv file.
    
    Args:
        tapsolver_simualtion (Simulation): The tapsolver simulation object.

        save_path (str, optional): The path or file name to save the input file.

    Returns:
        None

    Citation:
        Yonge et al, "TAPsolver: A Python package for the simulation and analysis of TAP reactor experiments"

    Implementor:
        M. Ross Kunz

    Link:
        https://doi.org/10.1016/j.cej.2021.129377

        https://arxiv.org/abs/2008.13584

    See also:
        tapsap.tapsolver.Simulation
    """

    # setting the reactor information
    reactor_df = pd.DataFrame()
    first_column = [
        'Zone Length', 'Zone Void', 'Reactor Radius', 
        'Reactor Temperature', 'Mesh Size', 'Catalyst Mesh Density', 
        'Output Folder Name', 'Experimental Data Folder', 'Reference Diffusion Inert', 
        'Reference Diffusion Catalyst', 'Reference Temperature', 'Reference Mass', 
        'Advection Value'
    ]
    first_column += [i for i in list(tapsolver_simualtion.steps.values())] + [np.NaN] + [i for i in list(tapsolver_simualtion.link_names.values())]
    second_column = [
        tapsolver_simualtion.zone_lengths.values()[0], tapsolver_simualtion.zone_void.values()[0], tapsolver_simualtion.reactor_radius,
        tapsolver_simualtion.reaction_temperature, tapsolver_simualtion.mesh_size, tapsolver_simualtion.catalyst_mesh_density,
        tapsolver_simualtion.output_folder_name, tapsolver_simualtion.experimental_data_folder, tapsolver_simualtion.reference_diffusion_inert,
        tapsolver_simualtion.reference_diffusion_catalyst, tapsolver_simualtion.reference_temperature, tapsolver_simualtion.reference_mass,
        tapsolver_simualtion.advection_value
    ]
    third_column = [tapsolver_simualtion.zone_lengths.values()[1], tapsolver_simualtion.zone_void.values()[1]] + [np.NaN] * (len(first_column) - 2)
    fourth_column = [tapsolver_simualtion.zone_lengths.values()[2], tapsolver_simualtion.zone_void.values()[2]] + [np.NaN] * (len(first_column) - 2)
    
    reactor_df['Reactor_Information'] = first_column + [np.NaN]
    reactor_df['Unnamed: 1'] = second_column + [np.NaN]
    reactor_df['Unnamed: 2'] = third_column + [np.NaN]
    reactor_df['Unnamed: 3'] = fourth_column + [np.NaN]

    # setting the feed
    feed_df = pd.DataFrame()
    feed_df['Reactor_Information'] = ['Feed_&_Surface_Composition'] + [np.NaN] + ['Intensity', 'Time', 'Mass'] + [np.NaN]
    for i in range(len(tapsolver_simualtion.feed_names.values())):
        temp_name = 'Unnamed: ' + str(i + 1)
        temp_list = [np.NaN, tapsolver_simualtion.feed_names.values()[i], tapsolver_simualtion.feed_intensity.values()[i], tapsolver_simualtion.feed_time.values()[i], tapsolver_simualtion.feed_mass.values()[i]] + [np.NaN]
        feed_df[temp_name] = temp_list

    # setting the surface composition
    surface_df = pd.DataFrame()
    surface_df['Reactor_Information'] = [np.NaN, 'Initial Concentration'] + [np.NaN]
    for i in range(len(tapsolver_simualtion.surface_names.values())):
        temp_name = 'Unnamed: ' + str(i + 1)
        temp_list = [tapsolver_simualtion.surface_names.values()[i], tapsolver_simualtion.surface_concentrations.values()[i]]
        surface_df[temp_name] = temp_list

    # setting the reaction information
    reaction_df = pd.DataFrame()
    first_column = ['Reaction_Information'] + list(tapsolver_simualtion.steps.values()) + [np.NaN, 'Linked Kinetics'] + list(tapsolver_simualtion.link_names.values())
    second_column = [np.NaN] + list(tapsolver_simualtion.left_links.values()) + [np.NaN] * 2 + list(tapsolver_simualtion.linked_kinetics.values())
    third_column = [np.NaN] + list(tapsolver_simualtion.right_links.values()) + [np.NaN] * (2 + len(tapsolver_simualtion.linked_kinetics.values()))

    reaction_df['Reactor_Information'] = first_column + [np.NaN]
    reaction_df['Unnamed: 1'] = second_column + [np.NaN]
    reaction_df['Unnamed: 2'] = third_column + [np.NaN]

    # combine all of the data frames
    result = pd.concat([reactor_df, feed_df, surface_df, reaction_df], axis=1)
    result.to_csv(save_path)