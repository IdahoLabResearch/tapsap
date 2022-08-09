# Reactor
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

class Reactor():
    """
    
    This class acts as a container for all of the reactor parameters.
    
    Attributes:
        zone_lengths (dict): The zone lengths for the reactor.

        zone_porosity (dict): The bed porosity within each zone.

        zone_diffusion (dict): The diffusion coefficient for each zone.

        zone_residence_time (dict): The residence time within each zone.

        reactor_radius (float): The radius of the reactor.

        catalyst_weight (float): The catalyst weight.

        mol_per_pulse (float): The mol per pulse.
        
    """
    def __init__(self):
        self.zone_lengths = {'zone0':0.02, 'zone1':0.00075, 'zone2':0.02}
        self.zone_porosity = {'zone0':0.4, 'zone1':0.4, 'zone2':0.4}
        self.zone_diffusion = {'zone0':0.002, 'zone1':0.002, 'zone2':0.002}
        self.zone_residence_time = {'zone0':0.5, 'zone1':0.5, 'zone2':0.5}
        self.reactor_radius = 0.002
        self.catalyst_weight = 1
        self.mol_per_pulse = 1


