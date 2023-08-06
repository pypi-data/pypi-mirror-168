# -*- coding: utf-8 -*-
"""
E"-binning single-path nonuniform temperature fitting based on time-domain fitting.

Splits H2O linelist into several separate databases for bins of lower-state energy.
Then performs multi-molecule time-domain fit (each E"-bin treated as different molecule)

Syntax warning: uses object-oriented programming with inheritance.

Abbreviations:
    td = time-domain signal. inverse Fourier Transform of frequency spectrum
    wvn = wavenumber (cm-1) of x-axis
    HTP = Hartman-Tran lineshape profile
    bl = laser transmission baseline. number of time-domain points attributed to baseline
    e = lower-state energy (cm-1)
    ebin = subset of linelist for H2O for transitions with similar lower-state energy
    s = linestrength
    rat = ratio, multiplied by some normalization value (reference pressure, reference linestrength) to get actual value
    sh = s_hat = normalized linestrength
    srat = integrated_area / (S(T_ref)P_ref X_ref L_ref)
    TPXL = path-average thermodynamic parameters
            t_celsius (temperature Celsius), 
            p_torr (pressure Torr), 
            chi (molefraction of absorbing molecule (default H2O) (between 0-1)), 
            pathlength (cm)

Created on Tue Jul 23 09:00:06 2019

@author: Nate the Average
"""
# built-in modules
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from time import time
import json
from scipy.optimize import leastsq, nnls # for least-squares fitting
#   use scipy instead of lmfit to handle arbitrary number of linelist inputs

# support modules in the package
try:
    from .Ebin_support import snorm_fit_t_x, s_two_temp, s_t_exact
    from .Ebin_support import calc_cepstrum_td, calc_spectrum_fd
    from .td_support import weight_func
    from .file_support import Transmission
    from ..hapi import db_begin, HITRAN_DEFAULT_HEADER
except:
    from Ebin_support import snorm_fit_t_x, s_two_temp, s_t_exact
    from Ebin_support import calc_cepstrum_td, calc_spectrum_fd
    from td_support import weight_func
    from file_support import Transmission
    from hapi import db_begin, HITRAN_DEFAULT_HEADER


## external module for calculating model absorption spectra.
#from packfind import find_package
#find_package('pldspectrapy')
#import pldspectrapy.pldhapi as hapi

class EbinHapi(Transmission):
    """
    Object-oriented script for time-domain E"-binning. 
    Designed for H2O-in-air
    
    INPUTS:
        output_path  = output directory + name of output files.
           eg 'C:\\Users\\Nate\\Documents\\fits\\H2O_5Feb' will make Labfit files called 'H2O_5Feb.inp'
           in the directory 'C:\\Users\\Nate\\Documents\\fits
        bandwidth     = (cm-1) fitting window--should be contained within transmission spectrum.
        
    OUTPUTS:
        self.snorm_out (nonuniform linestrength curve calculated against reference TPXL)
        (information also saved in output_path.txt for export to TikhonovInversion)
        
        Other optional outputs:
        - other spectral fit plots available through spectrum_by_ebin(), plot_ebin()
        - coarse temperature fits available through fit_temperature() and temperature_bin()
        - absorption spectrum for nonuniform path calculated through simulate_spectrum()

        
    Created on Wed Oct 31 15:52:38 2018    
    @author: Nate the Average
    """
    
    def __init__(self, output_path, bandwidth = [6800,7100], Labfit_HTP = False):
        # Load generic Labfit variables
        if bandwidth[0] > bandwidth[1]:
            foo = bandwidth[1]
            bandwidth[1] = bandwidth[0]
            bandwidth[0] = foo
        Transmission.__init__(self, bandwidth)
        # And initialize E"-binning-specific variables
        self.Elist = [0,500,1000,2000,7000]#[0,50,100,200,300,400,500,600,750,1020,1220,1440,1680,1940,2220,2510,2820,3100,4000,7000]
            # A list to hit all of the J" = 5-16 family of high-E" lines. vib = (101<-000)
            # E"=1000-3000 bins split along middle between each strong-line J" family.
            # Any lines with E" > max(self.Elist) will not be included in the fit
        self.bl = 0.002 # baseline weighting portion
        self.etalons = []
        self.weight = None
        self.snorm_out = []
        self.p_rat = None # If model features narrower than measurement, increase p_rat
        self.shift = None # If v_model < v_meas, then reduce shift (more negative)
        self.sdvoigt = False
        
        # Initialize the spectral variables
        self.bkgd_mod_fd = None
        self.flip_spectrum = False # for DCS if reverse Nyquist window

        # optional true discretized T(x) profile
        self.tx_act_kelvin = None
        
        # Initialize linelist variables
        if os.path.isabs(output_path) is True:
            self.full_output_name = output_path
        else:
            self.full_output_name = os.path.join(os.getcwd(), output_path)
        self.path, self.output_name = os.path.split(output_path)
        self.path = os.path.join(self.path, 'hood')
        if os.path.exists(self.path) is False:
            os.makedirs(self.path)
        self.linelist_path = ''
        self.wvn_start = bandwidth[0]
        self.wvn_stop  = bandwidth[1] 
        self.n_lines = 0
        self.molec_id = 1
        self.local_iso_id = 1
        
    def calc_bkgd(self, p_atm = 0, molefraction = 0, t_kelvin = 296,
                  pathlength_cm = 0, shift_wvn = 0, db_override=''):
        '''
        Calculate time-domain background-subtraction model from P,x,T,L
        '''
        assert self.x_wvn is not None, "Need absorption spectrum first"
        
        # Set up linelist file
        if len(db_override) == 0:
            db_override = self.linelist_path
        db_name = os.path.basename(db_override).split('.')[0]
        dir_db = os.path.dirname(db_override)
        if len(dir_db) == 0:
            db_begin(os.getcwd())
        else:
            db_begin(dir_db)
            
        # Setup T,P,x,L parameters
        self.bkgd_pars = {'p_atm':p_atm}
        self.bkgd_pars['chi'] = molefraction
        self.bkgd_pars['t_kelvin'] = t_kelvin
        self.bkgd_pars['pathlength_cm'] = pathlength_cm
        self.bkgd_pars['shift_wvn'] = shift_wvn

        # Simulate bkgd
        self.bkgd_mod_fd = calc_spectrum_fd(self.x_wvn, 1, 1, molefraction,
                                           p_atm, t_kelvin,
                                           pathlength_cm, shift_wvn, 
                                           db_name, self.sdvoigt)

###############################################
# Nest functions used in fit_snorm_* functions #
###############################################           
    def ebin(self,x):
        '''
        Determine which E"-bin a line with E" = x is in. Returns index of Elist. 
        
        Nested function of make_srat()
        '''
#        for i in range(1,len(self.Elist)):
#            if(x < self.Elist[i] and x >= self.Elist[i-1]):
#                return i-1
        try:
            ebin_i = next(index for index, e_val in enumerate(self.Elist) if e_val > x)
        except StopIteration:
            ebin_i = len(self.Elist)
        return ebin_i - 1
            
    def prep_ebins(self):
        '''
        Make different hapi file for each ebin
        '''
        msg = "Provide a valid linelist file path for self.linelist_path"
        assert os.path.exists(self.linelist_path), msg
        header = get_linelist_header(self.linelist_path)

        nE = len(self.Elist)-1 # first row never assigned.
        Ecount_weight = np.zeros(nE)
        Esum = np.zeros(nE)
        self.par_name = []
        par_bin = []
        if len(self.snorm_out) != nE:
            # Initialize normalized linestrengths if changed E"-bins,
            #  otherwise keep the output from the previous fit (or file load)
            self.snorm_out = np.ones(nE)
            self.n_lines = 0
        try:
            [os.remove(os.path.join(self.path,f)) for f in os.listdir(self.path) 
                                       if self.output_name+'_' in f and '.data' in f]
            [os.remove(os.path.join(self.path,f)) for f in os.listdir(self.path) 
                               if self.output_name+'_' in f and '.header' in f]
        except FileNotFoundError:
            pass
        for i in range(nE):
            e_i = int(1/2 * (self.Elist[i] + self.Elist[i+1]))
            self.par_name.append(self.output_name + '_' + repr(e_i))
#            self.par_name.append(self.full_output_name + '_' + repr(e_i) + '.data')
            par_bin.append(open(os.path.join(self.path,self.par_name[-1]+'.data'),'w'))
            # and write out the header file
            with open(os.path.join(self.path, self.par_name[-1] + '.header'),'w') as f:
                f.write(json.dumps(header, indent=2))
        
        # Now sort each line into different E"-bin data file
        with open(self.linelist_path, 'r') as lines:
            for line in lines:
                self.molec_id = int(line[:2])
                self.local_iso_id = int(line[2])
                nu = float(line[3:15])
                if nu > self.wvn_stop:
                    break
                if nu > self.wvn_start:
                    elower = float(line[45:55])
                    ebin_i = self.ebin(elower)
                    s_i = float(line[15:25])* s_t_exact(self.t_celsius+273, 296, elower)
                    if ebin_i < nE and ebin_i >= 0:
                        Ecount_weight[ebin_i] += s_i**2
                        Esum[ebin_i] += s_i**2 * elower 
                        par_bin[ebin_i].write(line)
                        self.n_lines += 1
        for ebin in par_bin:
            ebin.close()
        par_bin = []
        # Weighted-average E" for each bin for future temperature inversion
        self.ebin_xVals = np.round(Esum / Ecount_weight)
        # Check on E"-selections
        self.bin_size = Ecount_weight # bigger number is better for fit uncertainty
        if min(self.bin_size) == 0:
            print('WARNING: certain E"-bins have no absorption features')
            bad = 0
            bads = []
            for i, b in enumerate(self.bin_size):
                if b == 0:
                    print('E" = ' + repr(self.Elist[i]) + '-' + repr(self.Elist[i+1]))
                    # Delete empty E"-bins from Elist and linelist files
                    bad_file = os.path.join(self.path, self.par_name[i])
                    os.remove(bad_file + '.data')
                    os.remove(bad_file + '.header')
                    bad += 1
                    bads.append(i)
            # Delete empty E"-bins from all relevant files
            self.ebin_xVals = np.delete(self.ebin_xVals, bads)
            self.Elist = np.delete(self.Elist, np.array(bads)+1)
            self.par_name = np.delete(self.par_name, bads)
            if isinstance(self.shift, np.ndarray): # also check size of self.shift!
                self.shift = np.ones(len(self.par_name) - bad) * np.average(self.shift)
                
        return Ecount_weight
    
    def get_td(self):
        warning = "Import arrays for self.trans_spectrum and self.x_wvn, and "
        warning += "check whether self.print_thermo() is making decent average-PxTL."
        assert self.trans_spectrum is not None, warning
        
        self.absorption_td = np.fft.irfft(-np.log(self.trans_spectrum))
        self.absorption_td[0] = 0; self.absorption_td[-1] = 0 # remove dc
        if self.bl < 1: # only have fraction of time-domain to unweight
            self.bl = int(self.bl*len(self.absorption_td))
        self.weight = weight_func(len(self.trans_spectrum), self.bl, self.etalons)
        if self.bkgd_mod_fd is not None:
            self.absorption_td -= np.fft.irfft(self.bkgd_mod_fd)
            
    def shift_setup(self):
        '''
        Rescale dimension of width and shift arrays.
        Avoids runtime error with E"-bin model calculations
        '''
        nbins = len(self.Elist) - 1
        if self.p_rat is None:
            self.p_rat = np.ones(nbins)
        elif len(self.p_rat) != nbins:
            self.p_rat = np.average(self.p_rat) * np.ones(nbins)
        if self.shift is None:
            self.shift = np.zeros(nbins)
        if isinstance(self.shift, float) or isinstance(self.shift, int):
            self.shift = self.shift * np.ones(nbins)
        if len(self.shift) != nbins:
            self.shift = np.average(self.shift) * np.ones(nbins)
            
    def spectrum_by_ebin(self):
        '''
        Given fit results, plot absorbance for each spectrum.
        Must run some fit_snorm_* first
        '''
        if self.x_wvn is None:
            print('WARNING: no loaded transmission spectrum exists')
            print('Setting nominal transmission = 1, 0.01cm-1 resolution')
            self.x_wvn = np.arange(self.wvn_start, self.wvn_stop, 0.01)
            self.trans_spectrum = np.ones(len(self.x_wvn))
        self.absorption_models = []
        self.absorption_total = np.zeros(len(self.x_wvn))
        self.shift_setup()
        for ix, ebin in enumerate(self.par_name):
            p_atm = self.p_torr / 760 * self.p_rat[ix]
            absorption_ebin = calc_spectrum_fd(self.x_wvn, self.molec_id, 
                                               self.local_iso_id, self.chi,
                                               p_atm, self.t_celsius+273,
                                               self.pathlength, self.shift[ix], 
                                               ebin, self.sdvoigt)
            absorption_ebin *= self.snorm_out[ix] / self.p_rat[ix]
            self.absorption_total += absorption_ebin
            self.absorption_models.append(absorption_ebin)
        fig, axs = plt.subplots(2,1, sharex='col', figsize=(9,4))
        for index, ebin in enumerate(self.absorption_models):
            axs[0].plot(self.x_wvn, ebin, label = 'E" = ' + repr(self.ebin_xVals[index]))
        axs[1].set_xlabel('Wavenumber (cm$^{-1}$)'); axs[0].set_ylabel('Absorbance'); 
#        axs[0].legend(loc='upper left')
        try:
            res = self.absorption_td - np.fft.irfft(self.absorption_total)
        except: # AttributeError or ValueError
            self.get_td()
            res = self.absorption_td - np.fft.irfft(self.absorption_total)
        self.bl_mod = np.real(np.fft.rfft((1-self.weight)*res))
        self.data_meas = np.real(np.fft.rfft(self.absorption_td) - self.bl_mod)
        axs[0].plot(self.x_wvn, self.data_meas, 'k:', label = 'Data')
        axs[1].plot(self.x_wvn, self.data_meas - self.absorption_total,'r', linewidth=0.8)
        axs[1].set_xlim(self.wvn_start, self.wvn_stop)
        axs[0].set_title(os.path.basename(self.full_output_name))

###############################################################################
# Analysis functions you might call directly after running fit_snorm_* functions
###############################################################################
    def plot_ebin(self, ebin_index, tight_plot=False, plot_trans = False):
        '''
        After running spectrum_by_ebin, compare fit for single bin of features.
        Show srat uncertainty in shaded error bars,
        show all other absorption contributions in blue
        '''
        absorption_ebin = self.absorption_models[ebin_index]
        absorption_other = self.absorption_total - absorption_ebin
        uc_rat = self.snorm_uc[ebin_index] / self.snorm_out[ebin_index]
        colors = {'ebin':'r','others':'xkcd:bright blue'}
        if ebin_index >= 0:
            elabel='%d<E"<%d bin' % (self.Elist[ebin_index], self.Elist[ebin_index+1])
        else:
            elabel='%d<E"<%d bin' % (self.Elist[ebin_index-1], self.Elist[ebin_index])
#        # plot linestrength curve
#        plt.figure()
#        plt.plot(self.ebin_xVals, self.snorm_out,'.',color=colors['others'])
#        plt.errorbar(self.ebin_xVals, self.snorm_out, self.snorm_uc, color=colors['others'], ls='none')
#        plt.plot(self.ebin_xVals[ebin_index], self.snorm_out[ebin_index],'.',color=colors['ebin'])
#        plt.errorbar(self.ebin_xVals[ebin_index], self.snorm_out[ebin_index], 
#                     self.snorm_uc[ebin_index], color=colors['ebin'], ls='none')
#        plt.xlabel('E"'); plt.ylabel('Normalized linestrength')
        if tight_plot:
            # Plot without horizontal space between axes,
            #  tough for zooming but good for output plots
            plt.rcParams.update({'xtick.direction':'in','xtick.top':True})
            gs1 = gridspec.GridSpec(3,1)
            gs1.update(hspace=0)
            fig = plt.figure();
            # transmission spectrum
            if plot_trans:
                ax1 = plt.subplot(gs1[0])
                ax1.plot(self.x_wvn, self.trans_spectrum, 'k', linewidth=0.8)
                ax1.set_xlim(self.wvn_start, self.wvn_stop)
                ax1.set_xticklabels([])
                ax1.set_ylabel('Transmission')
                ax1.set_title('Time-domain fit %d < E" < %d' % (self.Elist[ebin_index], self.Elist[ebin_index+1]))
            else:
                ax1 = plt.subplot(3,1,1)
                ax1.plot(self.ebin_xVals, self.snorm_out,'.',
                         markersize=3, color=colors['others'])
                ax1.errorbar(self.ebin_xVals, self.snorm_out, self.snorm_uc,
                             color=colors['others'], ls='none')
                ax1.plot(self.ebin_xVals[ebin_index], self.snorm_out[ebin_index],
                         '+',markersize = 7, color=colors['ebin'])
                ax1.errorbar(self.ebin_xVals[ebin_index], self.snorm_out[ebin_index], 
                             self.snorm_uc[ebin_index], color=colors['ebin'], ls='none')      
                ax1.set_xlabel('E"'); ax1.set_ylabel('S')
            # absorbance spectrum
            ax2 = plt.subplot(gs1[1])
            other, = ax2.plot(self.x_wvn, absorption_other, color=colors['others'], linewidth=0.5, label = 'All other E"-bins')
            meas, = ax2.plot(self.x_wvn, self.data_meas, 'k:', linewidth=1.1, label='Measurement')
            ax2.fill_between(self.x_wvn, (1-uc_rat) * absorption_ebin,
                         (1+uc_rat) * absorption_ebin, color='r', alpha=0.6)
            main, = ax2.plot(self.x_wvn, absorption_ebin,color=colors['ebin'], label = elabel) 
            handles = [meas, main, other]
            ax2.legend(handles,['Measurement',elabel,'All other E"-bins'],frameon=False)
            ax2.set_xlim(self.wvn_start, self.wvn_stop)
            ax2.set_xticklabels([])
            ax2.set_ylabel('Absorbance')
            # residual spectrum
            ax3 = plt.subplot(gs1[2])
            ax3.plot(self.x_wvn, self.data_meas - self.absorption_total,'k', linewidth=0.8)
            ax3.set_xlim(self.wvn_start, self.wvn_stop)
            ax3.set_xlabel('Wavenumber (cm$^{-1}$)')
            ax3.set_ylabel('Residual')
            return fig, ax1, ax2, ax3
        else:
            fig, axs = plt.subplots(2,1, sharex='col')
            other, = axs[0].plot(self.x_wvn, absorption_other,color=colors['others'], 
                        linewidth=.5, label = 'All other E"-bins')
            meas, = axs[0].plot(self.x_wvn, self.data_meas,'k:', linewidth=1.1, label = 'Measurement')
            # and plot uncertainty of E"-bin
            axs[0].fill_between(self.x_wvn, (1-uc_rat) * absorption_ebin,
                             (1+uc_rat) * absorption_ebin, color='r', alpha=0.6) 
            main, = axs[0].plot(self.x_wvn, absorption_ebin,color=colors['ebin'], label = elabel)       
            handles = [meas, main, other]
            # residual plot and formatting
            axs[1].plot(self.x_wvn, self.data_meas - self.absorption_total,'k', linewidth=0.8)
            axs[1].plot(self.x_wvn, np.zeros(len(self.x_wvn)), 'b:')
            axs[1].set_xlabel('Wavenumber (cm$^{-1}$)')
            axs[1].set_ylabel('Absorbance residual')
            axs[0].set_ylabel('Absorbance')
            axs[0].legend(handles,['Measurement',elabel,'All other E"-bins'])
            axs[0].set_title(self.par_name[ebin_index])
            axs[1].set_xlim(self.wvn_start, self.wvn_stop)
    
    def plot_td(self):
        '''
        See time-domain fit residual and weighting window.
        Must run spectrum_by_ebin() first
        '''
        plt.figure()
        plt.plot(self.absorption_td, label = 'data')
        res_td = self.absorption_td - np.fft.irfft(self.absorption_total)
        plt.plot(res_td, label = 'residual')
        plt.plot(self.weight, 'k', label = 'weighting window')
        plt.ylim(-.01, .01)
        plt.xlabel('Time')
        plt.ylabel('Absorbance')
    
    def fit_temperature(self, change_temperature = False, two_t_fit = False):
        '''
        Quick fits to S(E") curves (with plots)
        Scatter plot of individual S(E") and regression for path-average T,X fit
        
        INPUTS:
            change_temperature = can update T,X estimate from regression
                                 then iterate on fit_snorm()
                                 to fit with improved lineshape model
            two_t_fit = Calculate second trendline for 2-zone path
                        with T1, X1, T2, X2
                        If this fits data better, then evidence for nonuniformity
                        WARNING: finicky, unstable nonlinear fitting routine
        '''
        plt.figure(); 
        plt.plot(self.ebin_xVals, self.snorm_out, 'b.')
        plt.errorbar(self.ebin_xVals, self.snorm_out, self.snorm_uc,
                  label = 'spectral data fit', ls='none', color='b')
        t0 = self.t_celsius + 273
        elower = np.linspace(self.ebin_xVals[0], self.ebin_xVals[-1])
        self.ebin_output = np.zeros((len(self.snorm_out),3))
        self.ebin_output[:,0] = self.ebin_xVals
        self.ebin_output[:,1] = self.snorm_out
        self.ebin_output[:,2] = self.snorm_uc
        # single-temperature fit
        t_fit, x_fit = leastsq(snorm_fit_t_x, [self.t_celsius, self.chi], 
                         args = (self.ebin_output, [self.t_celsius, self.chi]))[0]
        print('Path-average temperature ~ %d Celsius (%d K)' % (t_fit, (273+t_fit)))
        print('Path-average molefraction ~ %.3f' % x_fit)
        s_mod = s_t_exact(t_fit+273, t0, elower) * (x_fit / self.chi)
        plt.plot(elower, s_mod, label = 'single-T fit')
        plt.xlabel('E"'); plt.ylabel('Normalized linestrength');
        plt.legend()
        if change_temperature:
            self.t_celsius = int(t_fit)
            self.chi = x_fit
            self.p_rat = None # overwrite default pressures
            
            if self.chi > 1:
                self.chi = 1
                print('Warning: Molefraction too strong.')
                print('Double-check pressure and pathlength.')
        if two_t_fit:
            # two-temperature fit
            t1, t2, x1, x2 = leastsq(s_two_temp, [300, self.t_celsius, .1, self.chi],
                                     args = (self.ebin_output, self.t_celsius, self.chi))[0]
            s_mod = 1 / self.chi * (x1 * s_t_exact(t1+273, t0+273, elower)
                                                + x2 * s_t_exact(t2+273, t0+273, elower))
            plt.plot(elower, s_mod, label = 'two-T fit')
            plt.legend()
            return t1, t2, x1, x2
    
    def temperature_bin(self, t_min = 300, t_max = 1300):
        '''
        Non-negative least-squares inversion solution
         for Temperature Distribution Function (See Part 1 paper, section 4.1)
        
        If you don't want to do full TikhonovInversion, this will give you 
         a coarse estimate of the distribution of H2O across temperature.

        Same algorithm as MATLAB's lsqnonneg(A,b) from Lawson, Hanson        
        '''
        n_t = (t_max - t_min) + 1
        t_i = np.arange(t_min, t_max+1)
        matrix = np.zeros((len(self.ebin_xVals), n_t))
        for t in range(n_t):
            matrix[:,t] = s_t_exact(t_min + t, self.t_celsius + 273, self.ebin_xVals)
        tdf_t = nnls(matrix, self.snorm_out)[0]
        plt.figure(); plt.errorbar(self.ebin_xVals, self.snorm_out, self.snorm_uc)
        plt.plot(self.ebin_xVals, matrix @ tdf_t)
        plt.xlabel('E"'); plt.ylabel('Normalized linestrength');
        plt.legend('data','fit')
        plt.figure(); plt.plot(t_i, tdf_t);
        t_avg = np.sum(t_i * tdf_t) / np.sum(tdf_t)
        print('Fit temperature', t_avg, 'K')
        plt.xlabel('Temperature (K)'); plt.ylabel('TDF')
        return tdf_t

    def ebin_select(self, low_e = 0, high_e = 4000, de = 100, uc_thrsh = 5):
        '''
        Iterative algorithm for selecting optimal E"-bins.
        
        Run fit_snorm() with a dense linear-spaced selection of E",
        then combine the E"-bins above some statistical uncertainty threshold.
        
        INPUTS:
            low_e = lowest included E" (cm-1)
            high_e = highest included E" (cm-1)
            de = width of each E"-bin (cm-1)
            uc_thrsh = aggregate E"-bins with uncertainty above this relative
                       snorm_uc threshold
       OUTPUT:
           no explicit outputs
           optimized self.Elist
           accompanying normalized linestrengths from area-fit only
        '''
        self.Elist = np.arange(low_e, high_e, de)
        self.fit_snorm(False);
        uc_thrsh *= min(self.snorm_uc) # scale threshold to lowest-UC E"-bin
        bads = np.where(self.snorm_uc > uc_thrsh)
#        bads = np.floor(self.snorm_uc / uc_thrsh).nonzero() # alternate method
        self.Elist = np.delete(self.Elist, np.array(bads)+1)
        self.fit_snorm();
        
    def ebin_select2(self, s_thrsh=1e-22, de_thrsh = 100):
        '''
        Select E"-bins based on two principles:
            1) Merge bins if there are stronger features at lower-E" AND higher-E"
            2) Extend total E" range as long as there are features above noise.
                
        This method works best if good self.t_celsius estimate.
        Can iterate on fit_snorm and fit_temperature 
        to determine t_celsius and noise floor threshold from snorm_uc
        TODO:
            figure out noise floor
            Account for nearby strong features
            Center the E" bins around strong features
            Figure out different rules of thumb for high-model error cases
            
        BUG: make sure si2 is not resized
        '''
        Elist = np.arange(0,7000,10)
        self.Elist = Elist.copy() # start with arbitrarily high # bins
        si2 = self.prep_ebins() # linestrength sum-of-squares in each E"-bin
        # si2 estimate 
        # 1) Check for stronger E"-bins at lower and higher E"
        strongest = np.argmax(si2)
        m = strongest
        ebins = [m]
        # 2) 
        while m > 0 and np.sqrt(sum(si2[:m])) > s_thrsh:
            # check if sandwiched between lower E"-bins
            low = np.argmax(si2[:m-1])
            if low < (m-1): # there are stronger E"-bins below
                de = Elist[m] - Elist[low]
                if de > de_thrsh:
                    # 2) Check for strength of E"-bins
                    s_bin = np.sqrt(sum(si2[low:m]))
                    if s_bin > s_thrsh:
                        # Add the E"-bin
                        ebins.append(low) # actually average around low
                        m = low
                else:
                    # Buggy algorithm here.
                    low2 = np.argmax(si2[:low-1])
                    ebins.append(low2)
                    m = low2
                    pass # reduce low
            else:
                m -= 1
                pass # I don't understand this case
        m = strongest
        while m < len(si2)-1 and np.sqrt(sum(si2[m:])) > s_thrsh:
            # check if sandwiched between lower E"-bins
            hi = m-1 + np.argmax(si2[m+1:])
            if hi > (m+1): # there are stronger E"-bins below
                try:
                    de = Elist[hi] - Elist[m]
                except IndexError:
                    print(ebins)
                    print('Trying to set %d out of %d' % (hi, len(self.Elist)))
                if de > de_thrsh:
                    # 2) Check for strength of E"-bins
                    s_bin = np.sqrt(sum(si2[m:hi]))
                    if s_bin > s_thrsh:
                        # Add the E"-bin
                        ebins.append(hi) # actually average around low
                        m = hi
                else:
                    # Buggy algorithm here.
                    hi2 = hi-1+np.argmax(si2[hi+1:])
                    ebins.append(hi2)
                    m = hi2
                    pass # reduce low
            else:
                m += 1
                pass # I don't understand this case
        ebins = np.sort(np.asarray(ebins))
        # Now pick the E"-bin boundaries halfway between the strong features
        evals = Elist[ebins]
        ebounds = np.zeros(len(evals))
        ebounds[1:] = .5 * evals[:-1] + .5 * evals[1:]
        
        self.Elist = ebounds            

################################################################
## Random function to calculate nonuniform absorption spectra ##
################################################################
    def simulate_spectra(self, calc_uniform = False):
        '''
        Simulate nonuniform frequency-domain absorption spectrum.
        '''
        assert self.tx_act_kelvin is not None, "Populate self.tx_act_kelvin with temperature profile array"
        msg = "Provide a valid linelist file path for self.linelist_path"
        assert os.path.exists(self.linelist_path), msg
        if self.x_wvn is None:
            print('WARNING: no loaded frequency axis exists')
            print('Setting nominal 0.01cm-1 resolution')
            self.x_wvn = np.arange(self.wvn_start, self.wvn_stop, 0.01)
        # Set up the source file database
        source_file_path = os.path.dirname(os.path.abspath(self.linelist_path))
        db_name = os.path.basename(self.linelist_path).split('.')[0]
        switch_paths = False
        if source_file_path != os.path.abspath(self.path):
            switch_paths = True
            db_begin(source_file_path)
        
        # add together each quasi-uniform chunk
        nchunks = len(self.tx_act_kelvin)
        t_avg = 0
        alpha_nonuni = np.zeros(len(self.x_wvn))
        for t in self.tx_act_kelvin:
            t_avg += t / nchunks
            alpha_nonuni += calc_spectrum_fd(self.x_wvn, self.molec_id, self.local_iso_id,
                                             self.chi, self.p_torr/760, t,
                                             self.pathlength/nchunks, 0, db_name, self.sdvoigt)
        plt.figure()
        plt.plot(self.x_wvn, alpha_nonuni, 'r', label = 'nonuniform T(x)')
        plt.xlabel('Wavenumber (cm$^{-1}$)')
        plt.ylabel('Absorbance')
        plt.title('Simulated spectra for tx_act_kelvin')
        alpha_uni = None
        if calc_uniform:
            alpha_uni = calc_spectrum_fd(self.x_wvn, self.molec_id, self.local_iso_id,
                                         self.chi, self.p_torr/760, t_avg,
                                         self.pathlength, 0, db_name, self.sdvoigt)
            plt.plot(self.x_wvn, alpha_uni, 'k--', label = 'uniform path-average T')
            plt.legend(frameon = False)
        # return to old linelist path
        if switch_paths:
            db_begin(self.path)
        return alpha_nonuni, alpha_uni

############################################################
## Spectral-fitting functions with different constraints. ##
############################################################     
    def fit_snorm(self, plot_fit = True, ebin_correlations = False):
        '''
        Swiftest, least-accurate normalized linestrength fit routine.
        Solves some linear scaling factor (self.snorm_out)
         for the absorption spectra of each E"-bin,
         holding lineshapes fixed at estimated path-average TPXL values.
         
        If path is not too nonuniform, and estimated TPXL come from previous 
         uniform-path fit, then this approximation often works well,
         especially for E" = 1500-3000 (cm-1)
        
        Uses linear-regression fitting of m-FID signal (time-domain)
        
        INPUT:
            plot_fit = plots all E"-bins, but increases run time
                        set to False for iterated fit_snorm(); fit_temperature()
        '''
        tic = time()
        self.prep_ebins()
        db_begin(self.path)
        self.get_td()
        # lineshape scaling
#        self.p_rat = None # scale by p_torr
        self.shift_setup()
        
        # calculate the spectra for each E"-bin
        #  (assume no shift) !!
        dalpha_ds = np.zeros(((len(self.x_wvn)-1) * 2,len(self.par_name)))
        for i, db_name in enumerate(self.par_name):
            a_td = calc_cepstrum_td(self.x_wvn, self.molec_id, self.local_iso_id,
                                    self.chi, self.p_torr / 760,
                                    self.t_celsius + 273, self.pathlength, 
                                    self.shift[i], db_name, self.sdvoigt)
            dalpha_ds[:,i] = a_td * self.weight

        # Now linear regression with chi2 uncertainty
        meas_w = self.absorption_td * self.weight
        cov_s = np.linalg.inv(np.transpose(dalpha_ds) @ dalpha_ds)
        self.snorm_out = cov_s @ np.transpose(dalpha_ds) @ (meas_w)
        res_w = meas_w - dalpha_ds @ self.snorm_out
        chi2 = np.sum(res_w**2) / (len(res_w) - len(self.snorm_out))
        self.snorm_uc = np.sqrt(np.diag(cov_s) * chi2)
        
        if ebin_correlations:
            # normalize covariance matrix to show correlations between E"-bins
            rho_s = cov_s.copy()
            for i in range(np.shape(cov_s)[0]):
                rho_s[:,i] /= np.sqrt(cov_s[i,i])
                rho_s[i,:] /= np.sqrt(cov_s[i,i])
                rho_s[i,i] = 0 # should be 1, but set to 0 to emphaize GUI color-code
            return rho_s

        # wrap-up operations
        self.ebin_output = np.transpose(np.asfarray([self.ebin_xVals, self.snorm_out, self.snorm_uc]))
        if plot_fit:
            self.spectrum_by_ebin()
            self.save_to_tikhonov()
        print('Spectral fit in %d seconds' % (time() - tic))
        return self.snorm_out

    def fit_snorm_width(self):
        '''
        Floats Lorentz width and column density for each E"-bin.
        Updates path-average pressure according to broadening.
        
        Fit takes longer than for fit_snorm, (it's nonlinear least-squares)
        but is more likely to converge than is fit_snorm_width_shift

        Uses scipy.optimize.leastsq for time-domain fitting.
            first input (spectra_float_width) is time-domain measurement
            second input (self.snorm_out) is fit parameters
            third input (args) are all other parameters to calculate time-domain absorption model
              which are held constant throughout the fit.
        
        '''
        tic = time()
        self.prep_ebins()
        db_begin(self.path)
        self.get_td()
        # lineshape scaling
        vars = list(self.snorm_out)
        nbins = len(self.par_name)
        p_torr_before = self.p_torr # Do I want to just pass this to shift_setup?
        self.shift_setup()
        vars.extend(list(p_torr_before/760 * self.p_rat))
        
        out = leastsq(spectra_float_width, vars, args=(self.x_wvn,
                                                            self.molec_id,
                                                            self.local_iso_id,
                                                            self.t_celsius+273,
                                                            self.chi,
                                                            self.pathlength,
                                                            self.absorption_td,
                                                            self.weight,
                                                            self.shift,
                                                            self.par_name, self.sdvoigt),
                                                        full_output = True)
        if out[1] is None:
            print("Fit did not converge")
        else:
            res = out[2]['fvec']
            cov_x = out[1] * np.sum(res**2) / (len(res) - len(out[0]))
            length_out = out[0][:nbins]
            p_out_atm = out[0][-nbins:]
            self.p_torr = np.average(p_out_atm) * 760
            self.p_rat =  p_out_atm / (self.p_torr/760)
            self.snorm_out = length_out * self.p_rat
            self.snorm_uc = np.sqrt(np.diag(cov_x))[:nbins]
            self.ebin_output = np.transpose(np.asfarray([self.ebin_xVals, self.snorm_out, self.snorm_uc]))
            self.spectrum_by_ebin()
            self.save_to_tikhonov()
            print('Spectral fit in %d seconds' % (time() - tic))
        return out
    
    def fit_snorm_width_shift(self, fix_bins = []):
        '''
        Floats Lorentz width, lineshift and column density for each E"-bin.
        
        CAUTION: shift-fits are very unstable with this LM fitting.
        This fit will probably not converge unless you already have good
        snorm estimates from fit_snorm().
        
        Pressure-shift and -broadening follow a (296/T) power law,
        so the low-E" lines can have different linewidths and linecenters
        than those calculated for path-average temperature.
        
        INPUT:
            fix_bins = indices of any E"-bins to not fit for width and shift
        '''
        tic = time()
        self.prep_ebins()
        db_begin(self.path)
        self.get_td()
        vars = list(self.snorm_out)
        # Setup lineshape fits
        self.shift_setup()
        nbins = len(self.par_name)
        n_fix = len(fix_bins)
        float_bins = np.delete(np.arange(len(self.shift)), fix_bins)
        p_atm = self.p_torr/760 * self.p_rat
        vars.extend(list(p_atm[float_bins]))
        vars.extend(list(self.shift[float_bins]))        
        # Scipy fit engine
        out = leastsq(spectra_float_width_shift, vars, args=(self.x_wvn,
                                                            self.molec_id,
                                                            self.local_iso_id,
                                                            self.t_celsius+273,
                                                            self.chi,
                                                            self.pathlength,
                                                            self.absorption_td,
                                                            self.weight,
                                                            self.par_name, self.sdvoigt,
                                                            fix_bins,
                                                            p_atm[fix_bins],
                                                            self.shift[fix_bins]),
                                                        full_output = True)
        if out[1] is None:
            print("Fit did not converge")
        else:
            res = out[2]['fvec']
            cov_x = out[1] * np.sum(res**2) / (len(res) - len(out[0]))
            length_out = out[0][:nbins]
            self.p_rat[float_bins] = out[0][nbins:2*nbins-n_fix] / (self.p_torr/760)
            self.shift[float_bins] = out[0][-(nbins-n_fix):]
            self.snorm_out = length_out * self.p_rat
            self.snorm_uc = np.sqrt(np.diag(cov_x))[:nbins]
            self.ebin_output = np.transpose(np.asfarray([self.ebin_xVals, self.snorm_out, self.snorm_uc]))
            self.spectrum_by_ebin()
            self.save_to_tikhonov()
#            self.p_torr = np.average(self.p_rat) * 760 
            print('Spectral fit in %d seconds' % (time() - tic))
        return out
        
#####################################
##  Data/file management functions ##
#####################################
    def print_thermo(self):
        print("Uniform-path approximations")
        print("Temperature = ", self.t_celsius, "Celsius")
        print("Pressure = ", self.p_torr, "Torr")
        print("Molefraction = ", self.chi)
        print("Pathlength = ", self.pathlength, "cm")
        print('\n')
        print('\n')
        print('To change these properties for spectral fitting, ')
        print('update self.t_celsius, self.p_torr, self.chi, self.pathlength.')
        print('eg. >> N.t_celsius = 500   # (if working with Example_td.py)')

    def save_fit(self, suffix = '', full_path = True):
        '''
        Save dictionary of relevant fit conditions for future Python load.
        Can then access from new Python command line using EbinHapi.load_fit()
        
        INPUTS:
            suffix = append to file name (so you can save multiple fits,
                    for instance one of fit_snorm, and another of fit_snorm_width)
            full_path = if True, save full file location of transmission + linelist files
                        set False if exporting fit to another computer,
                        to use relative file path within zipped directories
            
        '''
        
        # External file handling (linelist and transmission spectrum)

        if len(self.transmission_path) == 0:
            print('Do not know file location of transmission spectrum')
            print('Saving current trans_spectrum and x_wvn')
            self.make_asc(self.full_output_name)
        if full_path:
            fit = {'linelist_path':os.path.abspath(self.linelist_path)}
            fit['transmission_path'] = os.path.abspath(self.transmission_path)
        else:
            fit = {'linelist_path':os.path.relpath(self.linelist_path)}
            fit['transmission_path'] = os.path.relpath(self.transmission_path)
        
        # Variable and array handling
        fit['wvn_start'] = self.wvn_start
        fit['wvn_stop'] = self.wvn_stop
        fit['t_celsius'] = self.t_celsius
        fit['pressure'] = self.p_torr
        fit['molefraction'] = self.chi
        fit['pathlength'] = self.pathlength
        if isinstance(self.Elist, np.ndarray):
            self.Elist = self.Elist.astype('float')
        fit['Elist'] = list(self.Elist)
        fit['sdvoigt'] = self.sdvoigt
        fit['snorm_out'] = list(self.snorm_out)
        fit['snorm_uc'] = list(self.snorm_uc)
        fit['bl'] = self.bl
        fit['etalons'] = self.etalons
        try:
            fit['p_rat'] = list(self.p_rat)
        except:
            pass
        try:
            fit['shift'] = list(self.shift)
        except:
            pass

#        return fit
    
        with open(self.full_output_name + '_ebin' + suffix,'w') as f:
            f.write(json.dumps(fit, indent=2))
            
    def load_fit(self, suffix='_ebin',load_transmission = False, load_path_override = None):
        '''
        Load conditions from previous fit, saved under save_fit with self.full_output_name
        Should just initialize EbinHapi, run load_fit, and then be able to run plot_ebin()
        INPUTS:
            load_transmission = flag to also load transmission spectrum from .asc file
            load_path_override = file path of previous fit 
                                 (defaults to EbinHapi.full_output_name)
        '''
        message = 'Fitting '
        if load_path_override is None:
            with open(self.full_output_name + suffix,'r') as f:
                fit = json.loads(f.read())
        else:
            with open(load_path_override,'r') as f:
                fit = json.loads(f.read())
        self.wvn_start = fit['wvn_start']
        self.wvn_stop = fit['wvn_stop']
        try:
            self.t_celsius = fit['t_celsius']
        except: # old notation
            self.t_celsius = fit['temp_c']
        self.p_torr = fit['pressure']
        self.chi = fit['molefraction']
        self.pathlength = fit['pathlength']
        self.Elist = fit['Elist']
        self.snorm_out = np.asarray(fit['snorm_out'])
        self.snorm_uc = np.asarray(fit['snorm_uc'])
        message += repr(len(self.snorm_out)) + ' areas'
        self.bl = fit['bl']
        try:
            self.etalons = fit['etalons']
        except KeyError:
            pass
        try:
            self.p_rat = np.asarray(fit['p_rat'])
            message += ', broadening'
        except KeyError:
            pass     
        try:
            self.shift = np.asarray(fit['shift'])
            message += ', shifts'
        except KeyError:
            pass
        # and prepare linelist from previous time for plotting
        self.linelist_path = fit['linelist_path']
        try:
            self.sdvoigt = fit['sdvoigt']
        except:
            pass
        self.prep_ebins()
        db_begin(self.path)
        if 'bkgd_pars' in fit.keys():
            self.bkgd_pars = fit['bkgd_pars']
                
        message += '.'
        print(message)
        if load_transmission:
            asc_file_path = fit['transmission_path']
            self.get_transmission_asc(asc_file_path, overwrite_thermo=False)
            if 'bkgd_pars' in fit.keys():
                self.calc_bkgd(self.bkgd_pars['p_atm'],
                               self.bkgd_pars['chi'],
                               self.bkgd_pars['t_kelvin'],
                               self.bkgd_pars['pathlength_cm'],
                               self.bkgd_pars['shift_wvn'])
            self.spectrum_by_ebin()
        else:
            print('Load transmission spectrum, ')
            print('Then run EbinHapi.spectrum_by_ebin() to calculate previous spectra.')
	
    def save_to_tikhonov(self, suffix=''):
        '''
        Push relevant E"-binning terms to text file for nonuniform inversion.
        Send T_DB and normalized linestrength curve to MATLAB for Tikhonov regularization.
        '''
        self.ebin_output = np.transpose(np.asfarray([self.ebin_xVals, 
                                                     self.snorm_out, 
                                                     self.snorm_uc]))
        # set up the string-formatted array
        np.savetxt('temp.txt', self.ebin_output)
        with open('temp.txt','r') as out:
            ebin_str = out.readlines()
        with open(self.full_output_name + suffix + '.txt','w') as out:
            out.write('T_DB (Celsius) = %d\n' % self.t_celsius)
            out.write('lower_state_energy normalized_linestrength uncertainty\n')
            out.writelines(ebin_str)
        os.remove('temp.txt')
        
    def __cleanup__(self):
        '''
        Remove linelist files created just for this object.
        '''
#        os.remove(self.path)
#        if self.n_lines > 0:
#            os.remove(self.output_name + 'lineList.dat')
#            os.remove(self.output_name + 'lineList.dir')
#            os.remove(self.output_name + 'lineList.bak')
#            self.n_lines = 0
        try:
            [os.remove(os.path.join(self.path,f)) for f in os.listdir(self.path) 
                                       if self.output_name+'_' in f and '.data' in f]
            [os.remove(os.path.join(self.path,f)) for f in os.listdir(self.path) 
                               if self.output_name+'_' in f and '.header' in f]
        except:
            pass

###############################################################################
# Time-domain fit functions used in fit_snorm_* functions inside Ebin_Hapi class
###############################################################################
def spectra_float_width(vars, xx, molec_id, iso, temperature_kelvin, 
                             molefraction, pathlength, data, weight, 
                             shift, databases, sdvoigt):
    absorption_all = np.zeros(len(xx))
    n_bins = len(databases)
    for i, db_name in enumerate(databases):
        p_atm = vars[n_bins + i]
        alpha_ebin = calc_spectrum_fd(xx, molec_id, iso, molefraction,
                                      p_atm, temperature_kelvin,
                                      pathlength, shift[i], db_name, sdvoigt)
        absorption_all += vars[i] * alpha_ebin
    absorp_td = np.fft.irfft(absorption_all)
    return weight * (data - absorp_td)

def spectra_float_width_shift(vars, xx, molec_id, iso, temperature_kelvin,
                                   molefraction, pathlength, data, weight, 
                                   databases, sdvoigt, fix_bins, p_fix, shift_fix):
    absorption_all = np.zeros(len(xx))
    n_bins = len(databases)
    # Lineshape fit arrays
    float_bins = np.delete(np.arange(n_bins), fix_bins)
    p_atm = np.zeros(n_bins)
    p_atm[float_bins] = vars[n_bins:2*n_bins-len(fix_bins)]
    p_atm[fix_bins] = p_fix
    shift = np.zeros(n_bins)
    shift[float_bins] = vars[2*n_bins-len(fix_bins):]
    shift[fix_bins] = shift_fix
    # Simulate spectral signatures for each E"-bin
    for i, db_name in enumerate(databases):
        alpha_ebin = calc_spectrum_fd(xx, molec_id, iso, molefraction,
                                      p_atm[i], temperature_kelvin,
                                      pathlength, shift[i], db_name, sdvoigt)
        absorption_all += vars[i] * alpha_ebin
    absorp_td = np.fft.irfft(absorption_all)
    return weight * (data - absorp_td)

# nested functions for fitting
def shift_scale(y0_fd, shift, dx):
    '''
    Estimate spectral shift by interpolating from nominal cross-section.
    
    INPUTS:
        y0_fd = original frequency-domain cross-section
        shift_by_dx = desired frequency shift divided by frequency resolution
                      of original cross-section
    '''
    # avoid changing the edge-points of the spectrum
    rem = (shift % dx) / dx # is this wrong with certain shift sign?
    offset = int(shift // dx)
    # calculate xi and hwo many points to remove based on offset
    n = len(y0_fd)
    y_fd = y0_fd.copy()
    if offset < 0:
        xi = np.arange(n + offset - 1)
        y_fd[xi - offset] = y0_fd[xi] * (1 - rem) + y0_fd[xi + 1] * rem
    else:
        xi = np.arange(offset, n-1)
        y_fd[xi - offset] = y0_fd[xi] * (1 - rem) + y0_fd[xi + 1] * rem
    
    return y_fd

def pressure_scale(y0_td, gamma):
    '''
    Scale Lorentz-width of absorption cross-section.
    Using simplified method of Makowiecki et al JQSRT 2020
    '''
    # assume symmetric cepstrum y0_td
    # only scale ~ 50% of the cepstrum
    # assume the rest is below noise floor and should stay that way
    nt = len(y0_td) // 4
    y0_td[:nt] *= np.exp(gamma * np.arange(nt))
    y0_td[:-nt-1:-1] = np.exp(gamma * np.arange(nt))
    
    return y0_td

'''
Hapi support file
'''
def get_linelist_header(linelist_file):
    header_file = linelist_file.split('.')[0] + '.header'
    if os.path.exists(header_file):
        with open(header_file, 'r') as h:
            header = eval(h.read()) # load file into dictionary
        if 'extra' in header:
            print("Using non-standard HITRAN parameters for:")
            print(header['extra'])
            
        return header
    else:
        print("Assuming standard par file without .header file or extra parameters")
        
        return HITRAN_DEFAULT_HEADER

#######
# Fin #
#######
