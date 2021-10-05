# read_tapsolver_input
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

import pandas as pd
from tapsap import tapsolver
import numpy as np
from tapsap import utils

def read_tapsolver_input(input_path:str) -> tapsolver.Simulation:
    """

    Takes an input file path and reads the tapsolver input file.
    
    Args:
        
        input_path (str): The path or file name to read the input file.

    Returns:
        tapsolver_simualtion (Simulation): The tapsolver simulation object.

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

    data = pd.read_csv(input_path)
    new_simulation = tapsolver.Simulation()

    start_of_reactor = 0
    start_of_feed = np.where(data.iloc[:,0].values == 'Feed_&_Surface_Composition')[0]
    start_of_surface = start_of_feed + 5
    start_of_reaction = np.where(data.iloc[:,0].values == 'Reaction_Information')[0]
    start_of_linked_kinetics = np.where(data.iloc[:,0].values == 'Linked Kinetics')[0]

    # reading in the reactor information
    for i in np.arange(start_of_reactor, start_of_feed - 1):
        id_name = data.iloc[int(i), 0].lower().replace(' ', '_')
        if 'zone' in id_name:
            temp_attr_values = {'zone0': float(data.iloc[int(i),1]), 'zone1': float(data.iloc[int(i),1]), 'zone2': float(data.iloc[int(i),1])}
        else:
            temp_attr_values = utils.filter_xl(data.iloc[int(i), 1])

        setattr(new_simulation, id_name, temp_attr_values)

    # reading in the feed information
    for i in np.arange(start_of_feed + 1, start_of_surface - 1):
        id_name = 'feed_' + str(data.iloc[int(i), 0]).lower().replace(' ', '_')
        if i == (start_of_feed + 1):
            id_name = 'feed_names'

        temp_attr_values = {}
        for j in np.arange(1, data.shape[1]):
            temp_feed_id = 'feed_' + str(j - 1)
            temp_attr_values[temp_feed_id] = utils.filter_xl(data.iloc[int(i), int(j)])
            
        setattr(new_simulation, id_name, temp_attr_values)

    # reading in the surface information
    for i in np.arange(start_of_surface + 1, start_of_reaction - 1):
        id_name = 'surface_' + str(data.iloc[int(i), 0]).lower().replace(' ', '_')
        if i == (start_of_surface + 1):
            id_name = 'surface_names'

        temp_attr_values = {}
        for j in np.arange(1, data.shape[1]):
            temp_surface_id = 'surface_' + str(j - 1)
            temp_attr_values[temp_surface_id] = utils.filter_xl(data.iloc[int(i), int(j)])
            
        setattr(new_simulation, id_name, temp_attr_values)

    # reading in the reaction information
    temp_steps = {}
    temp_left_links = {}
    temp_right_links = {}
    flag = 0
    for i in np.arange(start_of_reaction + 1, start_of_linked_kinetics - 1):
        id_name = 'step_' + str(flag)
        temp_steps[id_name] = utils.filter_xl(data.iloc[int(i), 0])
        temp_left_links[id_name] = utils.filter_xl(data.iloc[int(i), 1])
        temp_right_links[id_name] = utils.filter_xl(data.iloc[int(i), 2])
        flag += 1
                
    setattr(new_simulation, 'steps', temp_steps)
    setattr(new_simulation, 'left_links', temp_left_links)
    setattr(new_simulation, 'right_links', temp_right_links)

    # reading in the linked kinetics information
    temp_link_names = {}
    temp_linked_kinetics = {}
    flag = 0
    for i in np.arange(start_of_linked_kinetics + 1, data.shape[0]):
        id_name = 'link_' + str(flag)
        temp_link_names[id_name] = utils.filter_xl(data.iloc[int(i), 0])
        temp_linked_kinetics[id_name] = utils.filter_xl(data.iloc[int(i), 1])
        flag += 1
                
    setattr(new_simulation, 'link_names', temp_link_names)
    setattr(new_simulation, 'linked_kinetics', temp_linked_kinetics)

    return new_simulation