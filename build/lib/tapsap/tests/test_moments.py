# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved
import unittest
import tapsap
import pkgutil
import io
import pandas as pd
from numpy import array


class TestMoments(unittest.TestCase):
    def setUp(self):
        stream = pkgutil.get_data('tapsap', 'data/irreversible.csv')
        irreversible_data = pd.read_csv(io.BytesIO(stream))
        self.irreversible_inert_flux = array(irreversible_data['inert_flux'])
        self.irreversible_reactant_flux = array(irreversible_data['A_flux'])
        stream_2 = pkgutil.get_data('tapsap', 'data/reversible.csv')
        reversible_data = pd.read_csv(io.BytesIO(stream_2))
        self.reversible_inert_flux = array(reversible_data['inert_flux'])
        self.reversible_reactant_flux = array(reversible_data['A_flux'])
        self.times = array(irreversible_data['times'])
        self.actual_moments_clipped = {'M0':0.9,'M1': 0.3,'M2': 0.2}
        self.actual_rtd_values = {'mean_residence_time':0.5, 'variance_residence_time':0.2, 'gamma_shape':1.7, 'gamma_scale':3.3}
        self.inert_moments = {'M0':1, 'M1':0.5, 'M2':0.4}
        self.zone_residence_time = {'zone0':0.5, 'zone1':1, 'zone2':0.5}
        self.zone_lengths = {'zone0':0.5, 'zone1':1e-5, 'zone2':0.5}
        self.zone_porosity = {'zone0':0.5, 'zone1':0.5, 'zone2':0.5}
        self.diffusions = [0.5, 0.5, 0.5]
        self.irreversible_reactant_moments = {'M0':0.46, 'M1':0.15, 'M2':0.073}
        self.reversible_reactant_moments = {'M0':0.9, 'M1':0.46, 'M2':0.384}
        self.actual_irreversible_reactant_reactivites = {'r0':1.17, 'r1':0.01, 'r2':0.01}
        self.actual_reversible_reactant_reactivites = {'r0':0.11, 'r1':0.05, 'r2':0.00}
        self.eley_rideal_reactant_moments = {'M0':0.4, 'M1':0.09, 'M2':0.03}
        self.eley_rideal_product_moments = {'M0':0.3, 'M1':0.26, 'M2':0.28}
        self.actual_eley_rideal_product_reactivities = {'r0':0.75,'r1': -0.23,'r2': -0.82}
    ## testing caclulate_moments

    def test_caclulate_moments_no_options(self) -> None:
        """
        Test to verify the moments of an inert flux using the basic flux and times.
        """
        all_moments = tapsap.moments(self.irreversible_inert_flux, self.times)
        all_moments_rounded = [round(i, 1) for i in all_moments.values()]
        self.assertListEqual(all_moments_rounded, list(self.inert_moments.values()))


    def test_caclulate_moments_with_integration_time(self) -> None:
        """
        Test to verify the moments of an inert flux using the basic flux and times.  Clipping the flux to the first 1000 points.
        """
        all_moments = tapsap.moments(
            self.irreversible_inert_flux, self.times, integration_time_range=[0, 1])
        all_moments_rounded = [round(i, 1) for i in all_moments.values()]
        self.assertListEqual(all_moments_rounded, list(self.actual_moments_clipped.values()))


    ## testing rtd_parameters
    def test_rtd_parameters(self) -> None:
        """
        Test to verify the calculation of the rtd parameters.
        """
        all_rtd = tapsap.rtd_parameters(self.inert_moments)
        all_rtd_rounded = [round(i, 1) for i in all_rtd.values()]
        self.assertListEqual(all_rtd_rounded, list(self.actual_rtd_values.values()))

    def test_reactivities_reactant_irreversible(self) -> None:
        """
        Test to verify the reactivities of the reactant that are derived from data/irreversible.csv.
        """
        reactivities_reactant = tapsap.reactivities_reactant(
            self.irreversible_reactant_moments, self.inert_moments, self.zone_residence_time)
        reactivities_reactant_rounded = [
            round(i, 2) for i in reactivities_reactant.values()]
        self.assertListEqual(reactivities_reactant_rounded,
                             list(self.actual_irreversible_reactant_reactivites.values()))

    def test_reactivities_reactant_reversible(self) -> None:
        """
        Test to verify the reactivities of the reactant that are derived from data/reversible.csv.
        """
        reactivities_reactant = tapsap.reactivities_reactant(
            self.reversible_reactant_moments, self.inert_moments, self.zone_residence_time)
        reactivities_reactant_rounded = [
            round(i, 2) for i in reactivities_reactant.values()]
        self.assertListEqual(reactivities_reactant_rounded,
                             list(self.actual_reversible_reactant_reactivites.values()))

    def test_reactivities_product(self) -> None:
        """
        Test to verify the reactivities of the reactant that are derived from data/reversible.csv.
        """
        reactivities_reactant = tapsap.reactivities_reactant(
            self.eley_rideal_reactant_moments, self.inert_moments, self.zone_residence_time)
        reactivities_product = tapsap.reactivities_product(
            self.eley_rideal_product_moments, self.eley_rideal_reactant_moments, self.inert_moments, reactivities_reactant, self.zone_residence_time, self.diffusions)
        reactivities_product_rounded = [round(i, 2) for i in reactivities_product.values()]
        self.assertListEqual(reactivities_product_rounded,
                             list(self.actual_eley_rideal_product_reactivities.values()))

    def test_isreversible_false(self) -> None:
        """
        Test to verify the use of the normalized moments to determine if a flux is reversible. This is the false case.
        """
        test_reversible = tapsap.isreversible(
            self.irreversible_reactant_flux, self.times, self.irreversible_inert_flux, 40, 40)
        self.assertEqual(test_reversible, False)

    def test_isreversible_true(self) -> None:
        """
        Test to verify the use of the normalized moments to determine if a flux is reversible. This is the false case.
        """
        test_reversible = tapsap.isreversible(
            self.reversible_reactant_flux, self.times, self.reversible_inert_flux, 40, 40)
        self.assertEqual(test_reversible, True)

    def test_diffusion_moments(self) -> None:
        """
        Test to verify the diffusion coefficient.
        """
        test_diffusion = round(tapsap.diffusion_moments(self.inert_moments, self.zone_lengths, self.zone_porosity)['diffusion'],1)
        self.assertEqual(test_diffusion, self.diffusions[0])

    def test_diffusion_moments_new_mass(self) -> None:
        """
        Test to verify the diffusion coefficient.
        """
        test_diffusion = round(tapsap.diffusion_moments(self.inert_moments, self.zone_lengths, self.zone_porosity, 28, 40)['diffusion'],1)
        self.assertEqual(test_diffusion, 0.6)

    def test_min_mean_max(self) -> None:
        """
        Test to verify the min mean and max.
        """
        test_max = round(tapsap.min_mean_max(self.reversible_inert_flux)['max'], 2)
        self.assertEqual(test_max, 1.85)