# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved
import unittest
from tapsap import file_io
import io
import pkgutil
import tapsap
import nptdms
from numpy import unique, array


class TestFileIO(unittest.TestCase):
    def setUp(self):
        self.stream = pkgutil.get_data('tapsap', 'data/argon_100C.tdms')
        #self.stream_xlsx = pkgutil.get_data('tapsap', 'data/argon_100C.xlsx')
        self.base_file = nptdms.TdmsFile(
            io.BytesIO(self.stream)).as_dataframe()
        self.tdms_meta_data = self.base_file.filter(regex='Meta Data')
        self.actual_meta_data_list = [5.1, 5, 0.0, 'AMU_40_1', 8.0, 40]
        self.actual_flux_data_list = [-0.049, 0.1, 21, 100]
        self.actual_all_data_list = [-0.049, 0.1, 21, 2500]
        self.experiment = tapsap.read_tdms(io.BytesIO(self.stream))
        self.experiment_shape = [6, 2]
        self.reactor_shape = [7, 2]
        self.transient_summary_shape = [100, 2]
        self.transient_summary_excel_shape = [100, 4]
        self.transient_excel_shape = [2501, 103]
        self.transient_shape = [2500, 101]
        self.transient_shape = [2500, 2]

    def test_read_tdms(self) -> None:
        """
        Test to verify the read tdms function.
        """
        test_tdms = file_io.read_tdms(io.BytesIO(self.stream))
        self.assertEqual(test_tdms.num_samples_per_pulse, 2500)

    def test_experiment_to_df(self) -> None:
        """
        Test to verify the experiment to data frame function.
        """
        test_df = file_io.experiment_to_df(self.experiment)
        test_shape = list(test_df.shape)
        self.assertListEqual(test_shape, self.experiment_shape)

    def test_reactor_to_df(self) -> None:
        """
        Test to verify the reactor to data frame function.
        """
        test_df = file_io.reactor_to_df(self.experiment.reactor)
        test_shape = list(test_df.shape)
        self.assertListEqual(test_shape, self.reactor_shape)

    def transient_to_xlsx_summary(self) -> None:
        """
        Test to verify the transient_to_df_summary with excel to data frame function.
        """
        temp_keys = list(self.experiment.species_data.keys())
        test_df = file_io.transient_to_xlsx_summary(
            self.experiment.species_data[temp_keys[0]])
        test_shape = list(test_df.shape)
        self.assertListEqual(
            test_shape, self.transient_summary_excel_shape)

    def test_transient_to_xlsx(self) -> None:
        """
        Test to verify the transient_to_df with excel to data frame function.
        """
        temp_keys = list(self.experiment.species_data.keys())
        test_df = file_io.transient_to_xlsx(
            self.experiment.species_data[temp_keys[0]])
        test_shape = list(test_df.shape)
        self.assertListEqual(test_shape, self.transient_excel_shape)

    # def test_write_xlsx(self) -> None:
    #     """
    #     Test to verify the write to excel function.
    #     """
    #     test_tdms = file_io.read_tdms(io.BytesIO(self.stream))
    #     tapsap.write_xlsx(test_tdms, '../data/argon_100C.xlsx')

    # def test_read_xlsx(self) -> None:
    #     """
    #     Test to verify the read to excel function.
    #     """
    #     test_experiment = file_io.read_xlsx(io.BytesIO(self.stream_xlsx))
    #     self.assertEqual(len(test_experiment.data_gas), 1)
