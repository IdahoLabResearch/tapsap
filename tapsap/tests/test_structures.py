# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

import unittest
import io
import pkgutil
import tapsap

class TestStructures(unittest.TestCase):
    def setUp(self):
        stream = pkgutil.get_data('tapsap', 'data/argon_100C.tdms')
        self.experiment = tapsap.read_tdms(io.BytesIO(stream))
        self.min_value = -0.071
        self.M1_value = -0.34
        self.mean_residence_time = -1.328
        self.baseline_amount = -0.05
        self.calibration_amount = 0.25
        self.calibration_amount_sequential = 0.859

    def test_transient_set_min_mean_max(self) -> None:
        species_keys = list(self.experiment.species_data.keys())
        temp_transient = self.experiment.species_data[species_keys[0]]
        temp_transient.set_min_mean_max()
        temp_min = round(temp_transient.df_moments['min'][50], 3)
        self.assertEqual(temp_min, self.min_value)

    def test_set_moments(self) -> None:
        species_keys = list(self.experiment.species_data.keys())
        temp_transient = self.experiment.species_data[species_keys[0]]
        temp_transient.set_moments()
        temp_M1 = round(temp_transient.df_moments['M1'][50], 3)
        self.assertEqual(temp_M1, self.M1_value)

    def test_set_rtd_parameters(self) -> None:
        species_keys = list(self.experiment.species_data.keys())
        temp_transient = self.experiment.species_data[species_keys[0]]
        temp_transient.set_rtd_parameters()
        temp_mean_residence_time = round(
            temp_transient.df_moments['mean_residence_time'][50], 3)
        self.assertEqual(temp_mean_residence_time, self.mean_residence_time)

    def test_baseline_correct(self) -> None:
        species_keys = list(self.experiment.species_data.keys())
        temp_transient = self.experiment.species_data[species_keys[0]]
        temp_transient.baseline_correct()
        temp_baseline_amount = round(
            temp_transient.df_moments['baseline'][25], 2)
        self.assertEqual(temp_baseline_amount, self.baseline_amount)

    def test_baseline_correct_amount(self) -> None:
        species_keys = list(self.experiment.species_data.keys())
        temp_transient = self.experiment.species_data[species_keys[0]]
        temp_transient.baseline_correct(baseline_amount = self.baseline_amount)
        temp_baseline_amount = round(
            temp_transient.df_moments['baseline'][25], 2)
        self.assertEqual(temp_baseline_amount, self.baseline_amount)

    def test_calibrate_flux(self) -> None:
        species_keys = list(self.experiment.species_data.keys())
        temp_transient = self.experiment.species_data[species_keys[0]]
        temp_transient.calibrate_flux(0.25)
        temp_calibration_amount = round(
            temp_transient.df_moments['calibration_coef'][25], 3)
        self.assertEqual(temp_calibration_amount, self.calibration_amount)

    def test_calibrate_flux_pulse(self) -> None:
        species_keys = list(self.experiment.species_data.keys())
        temp_transient = self.experiment.species_data[species_keys[0]]
        temp_transient.calibrate_flux(reference_index=0)
        temp_calibration_amount = round(
            temp_transient.df_moments['calibration_coef'][25], 3)
        self.assertEqual(temp_calibration_amount, self.calibration_amount_sequential)

