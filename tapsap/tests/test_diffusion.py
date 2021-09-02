# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

import unittest
from tapsap import diffusion
import pandas as pd
from numpy import array
import io
import pkgutil
import tapsap


class TestDiffusion(unittest.TestCase):
    def setUp(self):
        self.zone_lengths = {'zone0':0.5, 'zone1':1e-5, 'zone2':0.5}
        self.zone_porosity = {'zone0':0.5, 'zone1':0.5, 'zone2':0.5}
        self.zone_diffusion = {'zone0':0.5, 'zone1':0.5, 'zone2':0.5}
        self.diffusion = 0.5
        self.initial_single_residence_time = 0.1
        self.actual_single_residence_time = 0.5
        self.initial_residence_time = {'zone0':0.1,'zone1': 1e-5,'zone2': 0.1}
        self.actual_residence_time = {'zone0':0.5, 'zone1':1e-5, 'zone2':0.5}
        stream = pkgutil.get_data('tapsap', 'data/irreversible.csv')
        test_data = pd.read_csv(io.BytesIO(stream))
        self.inert_flux = array(test_data['inert_flux'])
        self.times = array(test_data['times'])
        self.allowed_sdc_rmse = 1e-3
        self.graham_less_than_max = 2.594
        self.graham_greater_than_max = 1.513

    def test_calculate_residence_time(self) -> None:
        """
        Test to verify the residence time from reactor parameters.
        """
        test_residence_time = diffusion.calculate_residence_time(
            self.zone_lengths, self.zone_porosity, self.zone_diffusion)
        self.assertListEqual(list(test_residence_time.values()), list(self.actual_residence_time.values()))

    def test_standard_diffusion_curve(self) -> None:
        """
        Test to verify the standard diffusion curve.
        """
        test_sdc = diffusion.standard_diffusion_curve(
            self.actual_single_residence_time, self.times)
        rmse_sdc_difference = tapsap.rmse(test_sdc, self.inert_flux)
        self.assertAlmostEqual(rmse_sdc_difference,
                               self.allowed_sdc_rmse, places=3)

    def test_opt_sdc(self) -> None:
        """
        Test to verify the optimization of the standard diffusion curve.
        """
        test_sdc = diffusion.opt_sdc(
            self.initial_single_residence_time, self.inert_flux, self.times)
        estimated_residence_time = test_sdc['residence_time']
        self.assertAlmostEqual(estimated_residence_time,
                               self.actual_residence_time['zone2'], places=3)

    def test_grahams_law_less_than(self) -> None:
        """
        Test to verify application of Graham's law when the new mass is less than the current mass.
        """
        test_transform = diffusion.grahams_law(
            self.inert_flux, self.times, 40, 20)
        self.assertAlmostEqual(max(test_transform),
                               self.graham_less_than_max, places=2)

    def test_grahams_law_greater_than(self) -> None:
        """
        Test to verify application of Graham's law when the new mass is greater than the current mass.
        """
        test_transform = diffusion.grahams_law(
            self.inert_flux, self.times, 40, 60)
        self.assertAlmostEqual(max(test_transform),
                               self.graham_greater_than_max, places=2)
