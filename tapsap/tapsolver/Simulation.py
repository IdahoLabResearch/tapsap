# Simulation
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved
import pandas as pd
import numpy as np
from tapsap import structures

class Simulation():
    """
    
    This class acts as a container for all of the simulation parameters.
    
    Attributes:
        reaction_matrix (dict): The reaction matrix based on stoichiometery.

        elementary_steps (dict): The elementary steps.

        zone_mesh_sizes (dict): The mesh size per zone.

        advection_amount (float): The advection amount.

        reference_diffusion (float): The reference diffusion in the simulation.
        
    """
    def __init__(self):
        # reactor information
        self.zone_lengths = {'zone0': 2.80718, 'zone1': 0.17364, 'zone2': 2.80718}
        self.zone_void = {'zone0': 0.4, 'zone1': 0.4, 'zone2': 0.4}
        self.reactor_radius = 1
        self.reaction_temperature = 385.65
        self.mesh_size = 200
        self.catalyst_mesh_density = 4
        self.output_folder_name = 'results'
        self.experimental_data_folder = 'none'
        self.reference_diffusion_inert = 16
        self.reference_diffusion_catalyst = 16
        self.reference_temperature = 385.65
        self.reference_mass = 40
        self.advection_value = 0

        # feed and surface Composition
        self.feed_names = {'feed_1': 'A','feed_2': 'B', 'feed_3': 'C'}
        self.feed_intensity = {'feed_1': 1,'feed_2': 0.5, 'feed_3': 0}
        self.feed_time = {'feed_1': 0,'feed_2': 0.1, 'feed_3': 0}
        self.feed_mass = {'feed_1': 28.01,'feed_2': 32, 'feed_3': 44}
        self.surface_names = {'surface_1' : 'A*', 'surface_2':'B*', 'surface_3':'*'}
        self.surface_concentrations = {'surface_1' : 0, 'surface_2':0, 'surface_3':30}

        # reaction information
        self.steps = {'step_1': 'A + * <-> A*','step_2': 'B + * <-> B*','step_3': 'A* + B* <-> C + *'}
        self.left_links = {'step_1': '{a}','step_2': '{a}','step_3': '{c}'}
        self.right_links = {'step_1': '{b}','step_2': '{b}','step_3': '{d}'}
        self.link_names = {'link_1': 'a', 'link_2': 'b', 'link_3': 'c', 'link_4': 'd'}
        self.linked_kinetics = {'link_1': 4, 'link_2': 1, 'link_3': 10, 'link_4': 0.2}

    def set_from_experiment(self, experiment:structures.Experiment, inert_name:str):
        self.zone_lengths = experiment.reactor.zone_lengths
        self.zone_void = experiment.reactor.zone_porosity
        self.reactor_radius = experiment.reactor.reactor_radius
        inert_data = experiment.species_data[inert_name]
        # this may need to be scaled
        self.reference_diffusion_inert = inert_data.diffusion
        self.reference_diffusion_catalyst = inert_data.diffusion
        self.reaction_temperature = np.mean(inert_data.df_moments['temperature'].values)
        self.reference_temperature = np.mean(inert_data.df_moments['temperature'].values)
        self.reference_mass = inert_data.mass

    def reactor_to_df(self) -> pd.DataFrame:
        df = pd.DataFrame()
        first_column = [
            'Zone Length', 'Zone Void', 'Reactor Radius', 
            'Reactor Temperature', 'Mesh Size', 'Catalyst Mesh Density', 
            'Output Folder Name', 'Experimental Data Folder', 'Reference Diffusion Inert', 
            'Reference Diffusion Catalyst', 'Reference Temperature', 'Reference Mass', 
            'Advection Value'
        ]
        first_column += [i for i in list(self.steps.values())] + [np.NaN] + [i for i in list(self.link_names.values())]
        second_column = [
            self.zone_lengths.values()[0], self.zone_void.values()[0], self.reactor_radius,
            self.reaction_temperature, self.mesh_size, self.catalyst_mesh_density,
            self.output_folder_name, self.experimental_data_folder, self.reference_diffusion_inert,
            self.reference_diffusion_catalyst, self.reference_temperature, self.reference_mass,
            self.advection_value
        ]
        third_column = [self.zone_lengths.values()[1], self.zone_void.values()[1]] + [np.NaN] * (len(first_column) - 2)
        fourth_column = [self.zone_lengths.values()[2], self.zone_void.values()[2]] + [np.NaN] * (len(first_column) - 2)
        
        df['Reactor_Information'] = first_column + [np.NaN]
        df['Unnamed: 1'] = second_column + [np.NaN]
        df['Unnamed: 2'] = third_column + [np.NaN]
        df['Unnamed: 3'] = fourth_column + [np.NaN]

        return df

    def feed_to_df(self) -> pd.DataFrame:
        df = pd.DataFrame()
        df['Reactor_Information'] = ['Feed_&_Surface_Composition'] + [np.NaN] + ['Intensity', 'Time', 'Mass'] + [np.NaN]
        for i in range(len(self.feed_names.values())):
            temp_name = 'Unnamed: ' + str(i + 1)
            temp_list = [np.NaN, self.feed_names.values()[i], self.feed_intensity.values()[i], self.feed_time.values()[i], self.feed_mass.values()[i]] + [np.NaN]
            df[temp_name] = temp_list

        return df

    def surface_to_df(self) -> pd.DataFrame:
        df = pd.DataFrame()
        df['Reactor_Information'] = [np.NaN, 'Initial Concentration'] + [np.NaN]
        for i in range(len(self.surface_names.values())):
            temp_name = 'Unnamed: ' + str(i + 1)
            temp_list = [self.surface_names.values()[i], self.surface_concentrations.values()[i]]
            df[temp_name] = temp_list

        return df


    def reaction_to_df(self) -> pd.DataFrame:
        # always setting the values to Reactor_Information from the header
        df = pd.DataFrame()
        first_column = ['Reaction_Information'] + list(self.steps.values()) + [np.NaN, 'Linked Kinetics'] + list(self.link_names.values())
        second_column = [np.NaN] + list(self.left_links.values()) + [np.NaN] * 2 + list(self.linked_kinetics.values())
        third_column = [np.NaN] + list(self.right_links.values()) + [np.NaN] * (2 + len(self.linked_kinetics.values()))

        df['Reactor_Information'] = first_column + [np.NaN]
        df['Unnamed: 1'] = second_column + [np.NaN]
        df['Unnamed: 2'] = third_column + [np.NaN]

        return df

    def save_input(self, save_path:str = 'tapsolver_input.csv') -> None:
        reactor_df = self.reactor_to_df()
        feed_df = self.feed_to_df()
        surface_df = self.surface_to_df()
        reaction_df = self.reaction_to_df()
        result = pd.concat([reactor_df, feed_df, surface_df, reaction_df], axis=1)
        result.to_csv(save_path)



