# Simulation
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

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

    Citation:
        Yonge et al, "TAPsolver: A Python package for the simulation and analysis of TAP reactor experiments"

    Implementor:
        M. Ross Kunz

    Link:
        https://doi.org/10.1016/j.cej.2021.129377

        https://arxiv.org/abs/2008.13584
        
    """
    def __init__(self, experiment:structures.Experiment=None):
        # reactor information
        self.zone_length = {'zone0': 2.80718, 'zone1': 0.17364, 'zone2': 2.80718}
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
        # this could be better off as an object per feed name
        self.feed_names = {'feed_0': 'A','feed_1': 'B', 'feed_2': 'C'}
        self.feed_intensity = {'feed_0': 1,'feed_1': 0.5, 'feed_2': 0}
        self.feed_time = {'feed_0': 0,'feed_1': 0.1, 'feed_2': 0}
        self.feed_mass = {'feed_0': 28.01,'feed_1': 32, 'feed_2': 44}
        self.surface_names = {'surface_0' : 'A*', 'surface_1':'B*', 'surface_2':'*'}
        self.surface_initial_concentration = {'surface_0' : 0, 'surface_1':0, 'surface_2':30}

        # reaction information
        self.steps = {'step_0': 'A + * <-> A*','step_1': 'B + * <-> B*','step_2': 'A* + B* <-> C + *'}
        self.left_links = {'step_0': '{a}','step_1': '{a}','step_2': '{c}'}
        self.right_links = {'step_0': '{b}','step_1': '{b}','step_2': '{d}'}
        self.link_names = {'link_0': 'a', 'link_1': 'b', 'link_2': 'c', 'link_3': 'd'}
        self.linked_kinetics = {'link_0': 4, 'link_1': 1, 'link_2': 10, 'link_3': 0.2}

        if experiment is not None:
            self.zone_length = experiment.reactor.zone_lengths
            self.zone_void = experiment.reactor.zone_porosity
            self.reactor_radius = experiment.reactor.reactor_radius
            inert_species = experiment.species_class['inert']
            if inert_species is None:
                inert_data = experiment.species_data[list(experiment.species_data.keys())[0]]
            else:
                inert_data = experiment.species_data[inert_species]

            # this may need to be scaled
            self.reference_diffusion_inert = inert_data.diffusion
            self.reference_diffusion_catalyst = inert_data.diffusion
            self.reaction_temperature = inert_data.df_moments['temperature'].values.mean()
            self.reference_temperature = inert_data.df_moments['temperature'].values.mean()
            self.reference_mass = inert_data.mass

    def to_reactor(self) -> structures.Reactor:
        new_reactor = structures.Reactor()
        new_reactor.zone_lengths = self.zone_length
        new_reactor.zone_porosity = self.zone_void
        new_reactor.reactor_radius = self.reactor_radius

