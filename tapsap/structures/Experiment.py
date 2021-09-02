# Experiment
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

from tapsap import structures
import copy

class Experiment():
    """
     
    This class contains all of the experiment information.
    It mainly acts as a container for all of the species data / methods as well as a container for meta data.  
    

    Attributes:
        file_name (str): The name of the read file or experiment.
        
        collection_time (str): The collection time of the experiment.
        
        pulse_spacing (float): The pulse spacing within the experiment.

        time_start (float): The start time of each flux.

        time_end (float): The end time of the experiment.

        num_samples_per_pulse (int): The number of samples per pulse.

        species_data (dict): A collection of Transient objects.

        reactor (class Reactor): The reactor information.
        
    """
    def __init__(self):
        self.file_name = 'no_file_name'
        self.collection_time = 1
        self.pulse_spacing = 1
        self.time_start = 0
        self.time_end = 1
        self.num_samples_per_pulse = 100
        self.species_data = {}
        self.reactor = structures.Reactor()
       

    def set_reactor_params(self) -> None:
        """
        This method sets the reactor parameters for each species in species_data based on the experiments reactor information.
        """
        for i in list(self.species_data.keys()):
            self.species_data[i].reactor = self.reactor

    def remove_delay_time(self) -> None:
        """
        This method removes the delay time ranges from all gas species. This may need to be done if the experiment delays a pulse to determine the baseline at the front of the flux.

        """
        for i in list(self.species_data.keys()):
            self.species_data[i].remove_delay_time()

    def make_copy(self, name_to_copy:str, new_species_name:str) -> None:
        """
        This method makes a deep copy of a species such that it may be transformed without removing the original flux.

        Args:
            name_to_copy (str): A name contained in the species_data attribute

            new_species_name (str): The new name of the copy.
        """
        current_species = copy.deepcopy((self.species_data[name_to_copy]))
        current_species.name = new_species_name
        self.species_data[new_species_name] = current_species


    def set_reference_gas(self, inert_species:str) -> None:
        """
        This method sets the reference gas for all species in species_data

        Args:
            inert_species (str): The name of the inert species.
        """
        # this assumes that all of the baseline correction and calibration have already been performed.
        for i in list(self.species_data.keys()):
            self.species_data[i].reference_gas = self.species_data[inert_species]


