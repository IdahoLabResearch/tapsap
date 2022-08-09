# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

import unittest
import tapsap
import pkgutil
import io
from numpy import array
import pandas as pd


class TestUtils(unittest.TestCase):
    def setUp(self):
        stream = pkgutil.get_data('tapsap', 'data/reversible.csv')
        reversible_data = pd.read_csv(io.BytesIO(stream))
        self.times = reversible_data['times'].values
        self.inert_flux = reversible_data['inert_flux'].values
        stream = pkgutil.get_data('tapsap', 'data/irreversible.csv')
        irreversible_data = pd.read_csv(io.BytesIO(stream))
        self.irreversible_inert_flux = array(irreversible_data['inert_flux'])
        self.test_x = array([1, 2, 3, 4, 5])
        self.test_y = array([2, 3, 4, 5, 6])
        self.test_float = '0.1'
        self.test_int = '1'
        self.test_list = '[1,2,3,4]'
        self.test_json = '{"cat":["tap"]}'
        self.actual_gamma_parameters = [0.5, 0.16]
        self.inert_moments = {'M0':1, 'M1':0.5, 'M2':0.4}
        self.mad = 0.0676
        self.integration_times = [0.0, 2.999]

    def test_isfloat_true(self) -> None:
        test_response = tapsap.isfloat(self.test_float)
        self.assertEqual(test_response, True)

    def test_isfloat_false(self) -> None:
        test_response = tapsap.isfloat(self.test_list)
        self.assertEqual(test_response, False)

    def test_islist_true(self) -> None:
        test_response = tapsap.islist(self.test_list)
        self.assertEqual(test_response, True)

    def test_islist_false(self) -> None:
        test_response = tapsap.islist(self.test_float)
        self.assertEqual(test_response, False)

    def test_isint_true(self) -> None:
        test_response = tapsap.isint(self.test_int)
        self.assertEqual(test_response, True)

    def test_isint_false(self) -> None:
        test_response = tapsap.isint(self.test_float)
        self.assertEqual(test_response, False)

    def test_isjson_true(self) -> None:
        test_response = tapsap.isjson(self.test_json)
        self.assertEqual(test_response, True)           

    def test_rmse(self) -> None:
        test_response = tapsap.rmse(self.test_x, self.test_y)
        self.assertEqual(test_response, 1)

    def test_gamma_pdf(self) -> None:
        """
        Test to verify the creation of the gamma probability distribution function.
        """
        test_gamma_dist = tapsap.gamma_pdf(self.times, shape=1.5, scale=1/3)
        m1 = tapsap.trapz(test_gamma_dist * self.times, self.times)
        m2 = tapsap.trapz(test_gamma_dist * self.times**2, self.times)
        test_variance = m2 - m1**2
        test_gamma_parameters = [round(m1, 1), round(test_variance, 2)]
        self.assertListEqual(test_gamma_parameters,
                             self.actual_gamma_parameters)

    def test_filter_xl(self) -> None:
        test_response = tapsap.filter_xl('5.1')
        self.assertEqual(test_response, 5.1)

    def test_filter_xl(self) -> None:
        test_response = tapsap.filter_xl('5')
        self.assertEqual(test_response, 5)


    def test_trapz_full_time(self) -> None:
        """
        Test to verify the zeroth moment using the trapezoidal rule of the area of a flux.
        """
        zeroth_moment = tapsap.trapz(self.inert_flux, self.times)
        self.assertAlmostEqual(zeroth_moment, self.inert_moments['M0'], places=1)

    def test_trapz_full_time_first_moment(self) -> None:
        """
        Test to verify the first moment using the trapezoidal rule of the area of a flux.
        """
        zeroth_moment = tapsap.trapz(
            self.inert_flux * self.times, self.times)
        self.assertAlmostEqual(zeroth_moment, self.inert_moments['M1'], places=1)

    def test_trapz_full_time_second_moment(self) -> None:
        """
        Test to verify the second moment using the trapezoidal rule of the area of a flux.
        """
        zeroth_moment = tapsap.trapz(
            self.inert_flux * self.times**2, self.times)
        self.assertAlmostEqual(zeroth_moment, self.inert_moments['M2'], places=1)

    def test_mad(self) -> None:
        """
        Test to verify the median absolute deviation.
        """
        temp_mad = tapsap.mad(self.inert_flux)
        self.assertAlmostEqual(temp_mad, self.mad, places=1)

    def test_find_integration_time(self) -> None:
        """
        Test to verify the find_integration_time function.
        """
        test_integration_times = tapsap.find_integration_time(self.irreversible_inert_flux, self.times)
        self.assertListEqual(test_integration_times, self.integration_times)

