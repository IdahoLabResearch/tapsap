# Experiment
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

from tapsap import structures
import copy
import numpy as np

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
        self.species_class = {'inert':None, 'reactants': None, 'products':None}
       

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


    def calibrate_all_species(self, inert:str = None, reference_index = 10) -> None:
        """
        This method calibrates all other flux to the inert species.

        Args:
            inert (str): The name of the inert species as found in the species_data keys.  If none, then will use species_class contained in the experiment.

            reference_index (optional int): The index in which to calibrate the inert values.  Be sure to examine prior to application in case of outgassing.
        """
        if inert is not None:
            self.species_class['inert'] = inert

        inert_species = self.species_class['inert']

        try:
            inert_check = inert_species not in list(self.species_data.keys())
            if inert_check:
                raise ValueError
        except ValueError:
            print("Please enter a valid inert from the species data keys, i.e., experiment.species_data.keys()")

        self.species_data[inert_species].baseline_correct()
        self.species_data[inert_species].calibrate_flux(reference_index = reference_index)

        all_other_species = [i for i in list(self.species_data.keys()) if i is not inert_species]
        for i in all_other_species:
            current_mass = self.species_data[i].mass
            current_name = self.species_data[i].name.replace('AMU', '')
            inert_name = 'inert_' + current_name
            self.make_copy(inert_species, inert_name)
            # baseline correction and calibration
            self.species_data[inert_name].grahams_law(current_mass)
            self.species_data[i].reference_gas = self.species_data[inert_name]
            self.species_data[i].baseline_correct()
            self.species_data[i].calibrate_flux(huber_loss = True)
            self.species_data[i].set_moments()


    def rate_reactivity_data(self, inert:str = None, reactants:np.ndarray = None, products:np.ndarray = None, calibrate_data:bool = True, reference_index:int = 10) -> None:
        """
        This method calculates the rate, concentration, and the accumulation for each different species.

        Args:
            inert (str): The name of the inert species as found in the species_data keys.  If none, then will use species_class contained in the experiment.

            reactants (ndarray or str): The name(s) of the reactant species.  If none, then will use species_class contained in the experiment.

            products (ndarray or str): The name(s) of the product species.  If none, then will use species_class contained in the experiment.

            calibrate_data (bool): To calibrate the data prior to measuring the rate_reactivity_data.

            reference_index (optional int): The index in which to calibrate the inert values.  Be sure to examine prior to application in case of outgassing.
        """

        if inert is not None:
            self.species_class['inert'] = inert

        if reactants is not None:
            self.species_class['reactants'] = reactants

        if products is not None:
            self.species_class['products'] = products

        inert_species = self.species_class['inert']
        reactant_species = self.species_class['reactants']
        product_species = self.species_class['products']

        try:
            inert_check = inert_species not in list(self.species_data.keys())
            if inert_check:
                raise ValueError
        except ValueError:
            print("Please enter a valid inert from the species data keys, i.e., experiment.species_data.keys()")

        for i in reactant_species:
            try:
                reactant_check = i not in list(self.species_data.keys())
                if reactant_check:
                    raise ValueError
            except ValueError:
                print("Please enter a valid reactant from the species data keys, i.e., experiment.species_data.keys()")

        if product_species is not None:
            for i in product_species:
                try:
                    product_check = i not in list(self.species_data.keys())
                    if product_check:
                        raise ValueError
                except ValueError:
                    print("Please enter a valid product from the species data keys, i.e., experiment.species_data.keys()")

        if calibrate_data:
            self.calibrate_all_species(inert_species, reference_index = reference_index)

        for i in reactant_species:
            current_name = self.species_data[i].name.replace('AMU', '')
            # measure the concentration
            concentration_name = 'concentration_' + current_name
            self.make_copy(i, concentration_name)
            self.species_data[concentration_name].set_concentration()
            self.species_data[concentration_name].set_moments()
            # measure the rate
            rate_name = 'rate_' + current_name
            self.make_copy(i, rate_name)
            self.species_data[rate_name].set_rate(isreactant = True)
            self.species_data[rate_name].set_moments()
            # measure the accumulation
            accumulation_name = 'accumulation_' + current_name
            self.make_copy(rate_name, accumulation_name)
            self.species_data[accumulation_name].set_accumulation()
            self.species_data[accumulation_name].set_moments()

        if product_species is not None:
            for i in product_species:
                current_name = self.species_data[i].name.replace('AMU', '')
                # measure the concentration
                concentration_name = 'concentration_' + current_name
                self.make_copy(i, concentration_name)
                self.species_data[concentration_name].set_concentration()
                self.species_data[concentration_name].set_moments()
                # measure the rate
                rate_name = 'rate_' + current_name
                self.make_copy(i, rate_name)
                self.species_data[rate_name].set_rate()
                self.species_data[rate_name].set_moments()
                # measure the accumulation
                accumulation_name = 'accumulation_' + current_name
                self.make_copy(rate_name, accumulation_name)
                self.species_data[accumulation_name].set_accumulation()
                self.species_data[accumulation_name].set_moments()

