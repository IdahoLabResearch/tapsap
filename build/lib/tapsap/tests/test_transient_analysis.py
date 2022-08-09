# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved
import unittest
import tapsap
import pkgutil
import io
import pandas as pd
import numpy as np


class TestTransientAnalysis(unittest.TestCase):
    def setUp(self):
        stream = pkgutil.get_data('tapsap', 'data/irreversible.csv')
        irreversible_data = pd.read_csv(io.BytesIO(stream))
        self.times = np.array(irreversible_data['times'])
        self.irreversible_inert_flux = np.array(irreversible_data['inert_flux'])
        self.irreversible_reactant_flux = np.array(irreversible_data['A_flux'])
        self.irreversible_rate = np.array(irreversible_data['A_rate'])
        self.irreversible_concentration = np.array(irreversible_data['A_concentration'])
        self.diffusion = 0.002
        self.zone_lengths = {'zone0':0.018, 'zone1':1e-5, 'zone2':0.018}
        self.zone_porosity = {'zone0':0.4, 'zone1':0.4, 'zone2':0.4}
        self.reactor_radius = 0.002
        self.allowed_rmse = 1e1
        self.concentration_units = 716197.2


    def test_concentration_units(self):
        units = round(tapsap.concentration_units(self.diffusion, self.zone_lengths, self.reactor_radius),1)
        self.assertEqual(units, self.concentration_units)

    def test_concentration_g(self):
        test_concentration = tapsap.concentration_g(self.irreversible_reactant_flux, self.times, self.zone_lengths)
        test_concentration *= self.zone_lengths['zone2'] / self.diffusion
        test_rmse = round(tapsap.rmse(test_concentration, self.irreversible_concentration),1)
        self.assertLessEqual(test_rmse, self.allowed_rmse)

    def test_concentration_y(self):
        test_concentration = tapsap.concentration_y(self.irreversible_reactant_flux, self.times, self.diffusion, self.zone_lengths, self.zone_porosity, 5)
        test_concentration *= self.zone_lengths['zone2'] / self.diffusion
        test_rmse = round(tapsap.rmse(test_concentration, self.irreversible_concentration),1)
        self.assertLessEqual(test_rmse, self.allowed_rmse)

    def test_rate_g(self):
        test_rate = tapsap.rate_g(self.irreversible_reactant_flux, self.times, self.zone_lengths, self.irreversible_inert_flux)
        test_rmse = round(tapsap.rmse(test_rate, self.irreversible_rate),1)
        self.assertLessEqual(test_rmse, self.allowed_rmse)


    def test_rate_y(self):
        test_rate = tapsap.rate_y(self.irreversible_reactant_flux, self.times, self.diffusion, self.zone_lengths, self.zone_porosity, self.irreversible_inert_flux, 5)
        test_rmse = round(tapsap.rmse(test_rate, self.irreversible_rate),1)
        self.assertLessEqual(test_rmse, self.allowed_rmse)