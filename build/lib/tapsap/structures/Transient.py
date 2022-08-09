# Transient
# Copyright 2021, Battelle Energy Alliance, LLC All Rights Reserved

import numpy as np
import pandas as pd
from tapsap import structures, moments_analysis, preprocess, transient_analysis, diffusion
import multiprocessing as mp
import copy


class Transient():
    """
    
    This class contains all of the transient information per pulse for a single gas species.
    Most of the computation for preprocessing and transformations should take place in this class.

    Attributes:
        name (str): The name of the gas species.
        
        pulse_id (str): The pulse index for the parent gas species.
        
        mass (float): The mass of the gas species.

        gain (float): The gain of the mass spectrometer for measuring the gas species.

        delay_time (float): The delay time of the gas species.

        flux (dataframe): The measured flux of the gas species.

        times (float ndarray): An array of time.

        amount_pulsed (float): The amount pulsed for each pulse.

        initial_concentration (float): The initial concentration within the reaction.

        num_pulse (int): The number of pulses injected.

        df_moments (dataframe): A dataframe containing all of the summary information of the experiment.

        reactor (Reactor): A Reactor class containing all of the reactor information.

        reference_gas (Transient): The reference flux (inert flux) when measuring kinetic information.

        integration_times (list): The integration times for the moments.

        num_cores (int): The total number of cores to use in processing the data.  Initially set to the total number of cores available - 1.
        
    """

    def __init__(self):
        self.name = 'AMU_40_1'
        self.mass = 40
        self.gain = 9
        self.delay_time = 0
        self.flux = None
        self.smoothed_flux = None
        self.times = None
        self.smoothing_parameter = 1e-4
        # if surface species, then diffusion = 0
        self.diffusion = 0.5
        self.amount_pulsed = 1
        self.initial_concentration = 0
        self.num_pulse = 1
        self.df_moments = None
        self.reactor = structures.Reactor()
        self.reference_gas = None
        self.integration_times = [0, 3]
        self.num_cores = mp.cpu_count() - 1

    def set_min_mean_max(self) -> None:
        """
        A method for setting the summary information (min, mean, max) for each flux.
        """
        temp_result = moments_analysis.min_mean_max(self.flux)
        for j in temp_result.keys():
            self.df_moments[j] = temp_result[j]

    def set_moments(self, smooth_flux:bool = False, find_integration_times:list = False) -> None:
        """
        A method for setting the moments.

        Args:
            smooth_flux (bool): Smoothing the flux prior to optimization.

        See also:
            tapsap.moments_analysis.moments
        """
        if find_integration_times:
            temp_integration = None
        else:
            temp_integration = self.integration_times

        if smooth_flux:
            if not isinstance(self.smoothed_flux, pd.DataFrame):
                self.smooth_flux()
            
            temp_result = moments_analysis.moments(self.smoothed_flux, self.times, temp_integration)
        else:
            temp_result = moments_analysis.moments(self.flux, self.times, temp_integration)
        for j in temp_result.keys():
            self.df_moments[j] = temp_result[j]

    def set_gas_diffusion(self) -> None:
        """
        A method for setting the gas diffusion based on the inert or reference flux diffusion.
        This method requires a reference gas and that the moments have been calculated.
        """
        moment_check = 'M1' not in list(self.df_moments.keys())
        if moment_check:
            self.set_moments()

        if self.reference_gas is None:
            temp_result = moments_analysis.diffusion_moments(self.df_moments, self.reactor.zone_lengths, self.reactor.zone_porosity)
        else:
            temp_result = moments_analysis.diffusion_moments(self.df_moments, self.reactor.zone_lengths, self.reactor.zone_porosity, self.mass, self.reference_gas.mass)

        for j in temp_result.keys():
            self.df_moments[j] = temp_result[j]

        self.diffusion = np.mean(self.df_moments['diffusion'])

    def set_rtd_parameters(self) -> None:
        """
        A method for setting the residence time distribution parameters.
        This requires calculating the moments.

        See also:
            tapsap.moments_analysis.rtd_parameters
        """        
        moment_check = 'M1' not in list(self.df_moments.keys())    
        if moment_check:
            self.set_moments()

        temp_result = moments_analysis.rtd_parameters(self.df_moments)
        for j in temp_result.keys():
            self.df_moments[j] = temp_result[j]

    def set_reactivities(self, reactant_obj = None) -> None:
        """
        A method for setting the reactivites.
        The method requires that the reference_gas be set to the inert species using moments_analysis.diffusion_moments.

        Args:
            reactant_obj (Transient): If none, then it is assumed that the gas species is a reactant.  If used, then the gas species is a product and the additional moments are the reactant moments.

        See also:
            tapsap.moments_analysis.diffusion_moments

            tapsap.moments_analysis.reactivities_product

            tapsap.moments_analysis.reactivities_reactant
        """        
        moment_check = 'M1' not in list(self.df_moments.keys())    
        if moment_check:
            self.set_moments()
            self.set_gas_diffusion()

        reference_moment_check = 'M1' not in list(self.reference_gas.df_moments.keys())    
        if reference_moment_check:
            self.reference_gas.set_moments()
            self.reference_gas.set_gas_diffusion()

        if reactant_obj is None:
            temp_result = moments_analysis.reactivities_reactant(self.df_moments, self.reference_gas.df_moments, self.reactor.zone_residence_time)
        else:
            reactant_moment_check = 'M1' not in list(reactant_obj.df_moments.keys())    
            if reactant_moment_check:
                reactant_obj.set_moments()
                reactant_obj.set_gas_diffusion()

            reactant_reactivities_check = 'r1' not in list(reactant_obj.df_moments.keys())
            if reactant_reactivities_check:
                if reactant_obj.reference_gas is None:
                    reactant_obj.reference_gas = self.reference_gas

                reactant_obj.set_reactivities()

            temp_diffusions = [self.reference_gas.diffusion, reactant_obj.diffusion, self.diffusion]
            temp_result = moments_analysis.reactivities_product(self.df_moments, reactant_obj.df_moments, self.reference_gas.df_moments, reactant_obj.df_moments, self.reactor.zone_residence_time, temp_diffusions)

        for j in temp_result.keys():
            self.df_moments[j] = temp_result[j]

    def baseline_correct(self, baseline_time_range:list=None, baseline_amount:float=None, smooth_flux:bool=True) -> None:
        """
        A method for traditional baseline correction by either a baseline amount or baseline time range.
        If baseline_time_range and baseline_amount is None, then the baseline_gamma will be used.

        Args:
            baseline_time_range (float list): The points in time in which to take the baseline.

            baseline_amount (float): The amount of baseline correction to apply.

            smooth_flux (bool): Smoothing the flux prior to optimization.

        See also:
            tapsap.preprocess.baseline_correction

            tapsap.preprocess.baseline_gamma

        """
        moments_keys = list(self.df_moments.keys())
        if 'baseline' not in moments_keys:
            self.df_moments['baseline'] = np.zeros(self.num_pulse)

        if smooth_flux:
            if not isinstance(self.smoothed_flux, pd.DataFrame):
                self.smooth_flux()

        temp_baseline = np.zeros(self.num_pulse)
        if (baseline_time_range is None) & (baseline_amount is None):
            if smooth_flux:
                temp_args = [(self.smoothed_flux.iloc[:,i].values, self.times) for i in range(self.num_pulse)]
            else:
                temp_args = [(self.flux.iloc[:,i].values, self.times) for i in range(self.num_pulse)]
            
            pool = mp.Pool(self.num_cores)
            results = pool.starmap(preprocess.baseline_gamma, temp_args)
            pool.close()
            pool.join()
        else:
            results = [preprocess.baseline_correction(self.flux.iloc[:,i].values, self.times, baseline_time_range, baseline_amount) for i in range(self.num_pulse)]
            smooth_flux = False

        for i, result in enumerate(results):
            if smooth_flux:
                self.smoothed_flux.iloc[:,i] = result['flux']
                self.flux.iloc[:,i] -= result['baseline_amount']
            else:
                self.flux.iloc[:,i] = result['flux']
                if isinstance(self.smoothed_flux, pd.DataFrame):
                    self.smoothed_flux.iloc[:,i] -= result['baseline_amount']
            
            temp_baseline[i] = result['baseline_amount']

        self.df_moments['baseline'] = self.df_moments['baseline'] + temp_baseline

    def calibrate_flux(self, calibration_amount: float = None, reference_index:np.ndarray=None, smooth_flux: bool = True, huber_loss: bool = False, constraints:bool = True, fit_intercept:bool = True, enforce_max:bool = False) -> None:
        """
        A method for applying a calibration coefficient to the flux (multiplied).
        This method has the option to do traditional calibration via a calibration amount or if None, then will perform transient calibration.
        When the reference_index is not None, then this will loop over all flux and calibrate to a specific flux. 
        The reference flux is usefull when accounting for drift in the inert flux.

        Args:
            calibration_amount (float): The amount to scale the flux.

            reference_index (int): The index in which to calibrate all other flux.

            smooth_flux (bool): Smoothing the flux prior to optimization.

            huber_loss (bool): Use a robust loss function rather than the standard square error loss.

            constraints (bool): This controls whether contrained regression is performed.

            fit_intercept (bool): Fit the intercept within the convex optimization.

            enforce_max (bool): Enforce the maximum of the X values must be less than y.

        See also:
            tapsap.preprocess.calibration_coef

            tapsap.preprocess.tap_mix

            tapsap.preprocess.calibration_teak

        """
        moments_keys = list(self.df_moments.keys())
        if 'calibration_coef' not in moments_keys:
            self.df_moments['calibration_coef'] = np.ones(self.num_pulse)
            self.df_moments['intercept'] = np.zeros(self.num_pulse)

        if 'baseline' not in moments_keys:
            self.df_moments['baseline'] = np.zeros(self.num_pulse)

        if smooth_flux:
            if not isinstance(self.smoothed_flux, pd.DataFrame):
                self.smooth_flux()

        temp_coef = np.zeros(self.num_pulse)
        temp_intercept = np.zeros(self.num_pulse)
        if calibration_amount is not None:
            results = [preprocess.calibration_coef(self.flux.iloc[:,i].values, calibration_amount=calibration_amount) for i in range(self.num_pulse)]
            smooth_flux = False
        elif reference_index is not None:
            if smooth_flux:
                temp_args = [(self.smoothed_flux.iloc[:,i].values, self.smoothed_flux.iloc[:, reference_index].values, self.times, huber_loss, constraints, fit_intercept, enforce_max) for i in range(self.num_pulse)]
            else:
                temp_args = [(self.flux.iloc[:,i].values, self.flux.iloc[:, reference_index].values, self.times, huber_loss, constraints, fit_intercept, enforce_max) for i in range(self.num_pulse)]
            pool = mp.Pool(self.num_cores)
            results = pool.starmap(preprocess.tap_mix, temp_args)
            pool.close()
            pool.join()
        else:
            if smooth_flux:
                if not isinstance(self.smoothed_flux, pd.DataFrame):
                    self.reference_gas.smooth_flux()

                temp_args = [(self.smoothed_flux.iloc[:,i].values, self.reference_gas.smoothed_flux.iloc[:,i].values, self.times, huber_loss, constraints, fit_intercept, enforce_max) for i in range(self.num_pulse)]
            else:
                temp_args = [(self.flux.iloc[:,i].values, self.reference_gas.flux.iloc[:,i].values, self.times, huber_loss, constraints, fit_intercept, enforce_max) for i in range(self.num_pulse)]
            pool = mp.Pool(self.num_cores)
            results = pool.starmap(preprocess.tap_mix, temp_args)
            pool.close()
            pool.join()

        for i, result in enumerate(results):
            temp_calibration_coef = result['calibration_coef']
            if isinstance(temp_calibration_coef, list):
                temp_calibration_coef = temp_calibration_coef[0]

            temp_coef[i] = temp_calibration_coef
            temp_intercept[i] = result['intercept']
            if smooth_flux:
                self.flux.iloc[:,i] *= temp_calibration_coef
                self.flux.iloc[:,i] += result['intercept']
                self.smoothed_flux.iloc[:,i] = result['flux']
            else:
                self.flux.iloc[:,i] = result['flux']
                if isinstance(self.smoothed_flux, pd.DataFrame):
                    self.smoothed_flux.iloc[:,i] *= temp_calibration_coef  
                    self.smoothed_flux.iloc[:,i] += result['intercept']  


        self.df_moments['calibration_coef'] = self.df_moments['calibration_coef'] * temp_coef
        self.df_moments['intercept'] = temp_intercept
        self.df_moments['baseline'] = self.df_moments['baseline'] - result['intercept']


    def set_concentration(self, y_smoothing:float=None, post_smoothing:bool=True) -> None:
        """
        A method calculates the gas concentration from the available flux.
        Note that by doing this method, the original flux will be overwritten.
        It is preferable to make a deepcopy of the original species information where the concentration will another object.
        If y_smoothing is left as None, then G-Procedure is used.

        Args:
            y_smoothing (float): This value controls the amount of smoothing placed on the gas concentration when the Y-Procedure is used.  If None, then the G-Procedure is used.

            post_smoothing (boolean): Smooth the concentration, placed in smoothed_flux, after calculating the concentration.

        See also:
            tapsap.transient_analysis.concentration_g

            tapsap.transient_analysis.concentration_y

            tapsap.transient_analysis.smooth_flux_gam

        """
        pool = mp.Pool(self.num_cores)
        if y_smoothing is None:
            temp_args = [(self.flux.iloc[:,i].values, self.times, self.reactor.zone_lengths) for i in range(self.num_pulse)]
            results = pool.starmap(transient_analysis.concentration_g, temp_args)
        else:
            temp_args = [(self.flux.iloc[:,i].values, self.times, self.diffusion, self.reactor.zone_lengths, self.reactor.zone_porosity, y_smoothing) for i in range(self.num_pulse)]
            results = pool.starmap(transient_analysis.concentration_y, temp_args)

        pool.close()
        pool.join()
        temp_units = transient_analysis.concentration_units(self.diffusion, self.reactor.zone_lengths, self.reactor.reactor_radius, self.reactor.mol_per_pulse)
        for i, result in enumerate(results):
            self.flux.iloc[:,i] = result * temp_units

        if post_smoothing:
            self.smooth_flux()

    def set_rate(self, y_smoothing:float=None, isreactant:bool = False, post_smoothing:bool=True) -> None:
        """
        A method calculates the rate from the available flux.
        Note that by doing this method, the original flux will be overwritten.
        It is preferable to make a deepcopy of the original species information where the rate will another object.
        If y_smoothing is left as None, then G-Procedure is used.

        Args:
            y_smoothing (float): This value controls the amount of smoothing placed on the gas concentration when the Y-Procedure is used.  If None, then the G-Procedure is used.

            isreactant (bool): This controls whether the difference between the inert and the reactant is used when measuring the rate.

            post_smoothing (boolean): Smooth the rate, placed in smoothed_flux, after calculating the rate.

        See also:
            tapsap.transient_analysis.rate_g

            tapsap.transient_analysis.rate_y

            tapsap.transient_analysis.smooth_flux_gam

        """
        if isreactant:
            pool = mp.Pool(self.num_cores)
            temp_args = [(self.reference_gas.flux.iloc[:,i].values, self.times, self.reference_gas.mass, self.mass) for i in range(self.num_pulse)]
            inert_flux = pool.starmap(diffusion.grahams_law, temp_args)
            pool.close()
            pool.join()
        else:
            inert_flux = [None] * self.num_pulse

        pool = mp.Pool(self.num_cores)
        if y_smoothing is None:
            temp_args = [(self.flux.iloc[:,i].values, self.times, self.reactor.zone_lengths, inert_flux[i]) for i in range(self.num_pulse)]
            results = pool.starmap(transient_analysis.rate_g, temp_args)
        else:
            temp_args = [(self.flux.iloc[:,i].values, self.times, self.diffusion, self.reactor.zone_lengths, self.reactor.zone_porosity, inert_flux[i], y_smoothing) for i in range(self.num_pulse)]
            results = pool.starmap(transient_analysis.rate_y, temp_args)

        pool.close()
        pool.join()

        temp_units = transient_analysis.rate_units(self.reactor.mol_per_pulse, self.reactor.catalyst_weight)
        for i, result in enumerate(results):
            self.flux.iloc[:,i] = result * temp_units

        if post_smoothing:
            self.smooth_flux()


    def set_accumulation(self) -> None:
        """
        This method applies a cumulative intergral to the flux (preferably the rate to get the accumulation).

        """
        for i in range(self.num_pulse):
            self.flux.iloc[:,i] = np.cumsum(self.flux.iloc[:,i].values) * (self.times[1] - self.times[0])

        if self.smoothed_flux is not None:
            for i in range(self.num_pulse):
                self.smoothed_flux.iloc[:,i] = np.cumsum(self.smoothed_flux.iloc[:,i].values) * (self.times[1] - self.times[0])


    def smooth_flux(self) -> None:
        """
        This method applies smooth_flux_gam to each flux.

        See also:
            tapsap.transient_analysis.smooth_flux_gam

        """
        self.smoothed_flux = copy.deepcopy(self.flux)
        pool = mp.Pool(self.num_cores)
        temp_args = [(self.smoothed_flux.iloc[:,i].values, self.smoothing_parameter) for i in range(self.num_pulse)]
        results = pool.starmap(preprocess.smooth_flux_gam, temp_args)
        pool.close()
        pool.join()
        
        for i, result in enumerate(results):
            self.smoothed_flux.iloc[:,i] = result


    def grahams_law(self, new_mass:float) -> None:
        """
        This method applies grahams_law to each flux.

        Args:
            new_mass (float): The mass to scale the flux to.

        See also:
            tapsap.diffusion.grahams_law

        """
        pool = mp.Pool(self.num_cores)
        temp_args = [(self.flux.iloc[:,i].values, self.times, self.mass, new_mass) for i in range(self.num_pulse)]
        results = pool.starmap(diffusion.grahams_law, temp_args)
        pool.close()
        pool.join()
        
        self.mass = new_mass
        for i, result in enumerate(results):
            self.flux.iloc[:,i] = result

        if isinstance(self.smoothed_flux, pd.DataFrame):
            pool = mp.Pool(self.num_cores)
            temp_args = [(self.smoothed_flux.iloc[:,i].values, self.times, self.mass, new_mass) for i in range(self.num_pulse)]
            results = pool.starmap(diffusion.grahams_law, temp_args)
            pool.close()
            pool.join()

            for i, result in enumerate(results):
                self.smoothed_flux.iloc[:,i] = result


    def remove_delay_time(self) -> None:
        """
        This method removes the delay time ranges from the flux. This may need to be done if the experiment delays a pulse to determine the baseline at the front of the flux.

        """
        remove_index_end = abs(self.times - self.delay_time).argmin()
        self.flux.drop(self.flux.index[0:remove_index_end], inplace=True)
        self.times = self.times[0:self.flux.shape[0]]
        self.integration_times = [self.integration_times[0], min(self.integration_times[1], max(self.times))]




    