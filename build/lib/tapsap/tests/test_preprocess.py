# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved
import unittest
import tapsap
import pkgutil
import io
import pandas as pd
from numpy import array


class TestPreprocess(unittest.TestCase):
    def setUp(self):
        stream = pkgutil.get_data('tapsap', 'data/irreversible.csv')
        irreversible_data = pd.read_csv(io.BytesIO(stream))
        self.irreversible_inert_flux = array(irreversible_data['inert_flux'])
        self.irreversible_reactant_flux = array(irreversible_data['A_flux'])
        self.irreversible_reactant_flux_scaled = array(
            irreversible_data['A_flux']) * 2
        self.irreversible_inert_flux_shifted = array(
            irreversible_data['inert_flux']) + 2
        self.irreversible_inert_flux_scaled = array(
            irreversible_data['inert_flux']) * 2
        self.times = array(irreversible_data['times'])
        stream_3 = pkgutil.get_data('tapsap', 'data/argon_100C_subset.csv')
        noisy_data = pd.read_csv(io.BytesIO(stream_3))
        self.noisy_flux_1 = noisy_data['pulse_10']
        self.noisy_flux_2 = noisy_data['pulse_75']
        self.noisy_times = noisy_data['times']
        self.actual_gamma_parameters = [0.5, 0.16]
        self.allowed_rmse = 6e-2
        

    def test_baseline_correction_no_options(self) -> None:
        """
        Test to verify the baseline correction function.
        """
        test_flux = tapsap.baseline_correction(
            self.irreversible_inert_flux_shifted, self.times)['flux']
        test_rmse = tapsap.rmse(test_flux, self.irreversible_inert_flux)
        self.assertLessEqual(test_rmse, self.allowed_rmse)

    def test_baseline_correction_given_value(self) -> None:
        """
        Test to verify the baseline correction function given the baseline amount.
        """
        test_flux = tapsap.baseline_correction(
            self.irreversible_inert_flux_shifted, self.times, baseline_amount=2)['flux']
        test_rmse = tapsap.rmse(test_flux, self.irreversible_inert_flux)
        self.assertLessEqual(test_rmse, self.allowed_rmse)

    def test_baseline_correction_given_range(self) -> None:
        """
        Test to verify the baseline correction function given a baseline time range.
        """
        test_flux = tapsap.baseline_correction(
            self.irreversible_inert_flux_shifted, self.times, baseline_time_range=[2.9, 3.0])['flux']
        test_rmse = tapsap.rmse(test_flux, self.irreversible_inert_flux)
        self.assertLessEqual(test_rmse, self.allowed_rmse)

    def test_calibration_coef(self) -> None:
        """
        Test to verify the application of a calibration coefficient.
        """
        test_flux = tapsap.calibration_coef(
            self.irreversible_reactant_flux_scaled, 0.5)['flux']
        test_rmse = tapsap.rmse(test_flux, self.irreversible_reactant_flux)
        self.assertLessEqual(test_rmse, self.allowed_rmse)

    def test_baseline_gamma(self) -> None:
        """
        Test to verify the automatic baseline correction of a flux.
        """
        test_flux = tapsap.baseline_gamma(
            self.irreversible_inert_flux_shifted, self.times)['flux']
        test_rmse = tapsap.rmse(test_flux, self.irreversible_inert_flux)
        self.assertLessEqual(test_rmse, self.allowed_rmse)

    def test_tap_mix(self) -> None:
        """
        Test to verify the automatic calibration coefficient correction of a flux.
        """
        test_flux = tapsap.tap_mix(
            self.irreversible_reactant_flux_scaled, self.irreversible_inert_flux, self.times)['flux']
        test_rmse = tapsap.rmse(test_flux, self.irreversible_reactant_flux)
        self.assertLessEqual(test_rmse, self.allowed_rmse)

    def test_tap_mix_huber(self) -> None:
        """
        Test to verify the automatic calibration coefficient correction of a flux.
        """
        test_flux = tapsap.tap_mix(self.irreversible_reactant_flux_scaled,
                                   self.irreversible_inert_flux, self.times, huber_loss=True)['flux']
        test_rmse = tapsap.rmse(test_flux, self.irreversible_reactant_flux)
        self.assertLessEqual(test_rmse, self.allowed_rmse)

    def test_tap_mix_opt(self) -> None:
        """
        Test to verify the automatic calibration coefficient correction of a flux.
        """
        test_flux = tapsap.tap_mix_opt(
            self.irreversible_reactant_flux_scaled, self.irreversible_inert_flux)['flux']
        test_rmse = tapsap.rmse(test_flux, self.irreversible_reactant_flux)
        self.assertLessEqual(test_rmse, self.allowed_rmse)

    def test_smooth_flux_gam(self) -> None:
        """
        Test to verify the smoothing of a flux via Generalized Additive Models.
        """
        test_flux = tapsap.smooth_flux_gam(self.irreversible_inert_flux, 0.5)
        test_rmse = tapsap.rmse(test_flux, self.irreversible_inert_flux)
        self.assertLessEqual(test_rmse, self.allowed_rmse)

    def test_calibration_teak(self) -> None:
        """
        Test to verify the calibration teak that takes into account if the flux is reversible or irreversible
        """
        test_flux = tapsap.calibration_teak(
            self.irreversible_reactant_flux_scaled, self.irreversible_inert_flux, self.times, 40, 40)['flux']
        test_rmse = tapsap.rmse(test_flux, self.irreversible_reactant_flux)
        self.assertLessEqual(test_rmse, self.allowed_rmse)

