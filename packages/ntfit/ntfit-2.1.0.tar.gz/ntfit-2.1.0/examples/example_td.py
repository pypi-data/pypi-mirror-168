# -*- coding: utf-8 -*-
"""
Fit a transmission spectrum from some ASC file for temperature nonuniformity.

Produces a discrete normalized linestrength curve with statistical fitting uncertainties.
which can be then be imported into Tikhonov regularization algorithm (Ref 1)
 to solve for the nonuniform temperature distribution.
This E"-binning algorithm (Ref 2) uses time-domain fitting (Ref 3) 
 to extract concentrations at different E"-ranges.

PREREQUISITE:
This fitting code produces model spectra using the external hapi package (Ref 4).
This package includes a modification of hapi, hapi_combustion.py
to produce more accurate high-temperature lineshape models.

This package uses object-oriented programming. 
You can tab-complete in IPython console to see which functions are available.
INPUTS:
    ( see 5-step preparation in script below to see how to implement )
    - transmission spectrum (and corresponding x-axis)
    - absorption linelist (H2O works best)
    - path-average TPXL to calculate absorption lineshapes
    - which bins of lower-state energy to fit as separate concentrations
OUTPUTS:
	- Normalized linestrength curve text file, in this instance named "example_td.txt"
	   For input into TikhonovInversion algorithm (Ref 1)
       Information also stored in object as N.snorm_out and N.t_celsius
	- Plot of scaled concentration fits of all the E"-bins.


References:
1: Malarich, Rieker, "Part I: ..."
2: Malarich, Rieker, "Part II: ..."
3: Makowiecki, Cole, Hoghooghi, Rieker. ""
4: R.V. Kochanov, I.E. Gordon, L.S. Rothman, P. Wcislo, C. Hill, J.S. Wilzewski, 
   HITRAN Application Programming Interface (HAPI): A comprehensive approach to working 
   with spectroscopic data, J. Quant. Spectrosc. Radiat. Transfer 177, 15-30 (2016)
Created on Tue Jul 23 15:15:45 2019

@author: ForAmericanEyesOnly
"""
# built-in modules
import numpy as np
import matplotlib.pyplot as plt
import os

# nonuniform-temperature code
#from sys import path as syspath
#syspath.append(r'../')
from ntfit import spectrafit as ebin
from ntfit.tdist import Snorm2Tx
plt.rcParams.update({'figure.autolayout':True,'lines.linewidth':0.8}) # plot formatting

load_previous = False
new_fit = True
temperature_inversion = False

# Produce file + path name for computation and output files
file_name = os.path.join(os.getcwd(),'data','example_td')

transmission_labfit = r'data\Furnace_Synth.asc'# ASC file with transmission and thermodynamic data
# Other parameters to edit as you choose.
band_fit = [6802, 7000] # fit region (cm-1)
recommended_iteration = False # Get more accurate higher linestrengths for E"<1500 by floating each broadening. 
calc_nonuni_spectrum = True # Calculate transmission spectrum used in this example fit.

if load_previous:
    # previous E"-bin fit from transmission spectrum (in .asc file)
    NOld = ebin.EbinHapi(file_name, bandwidth = band_fit)
    NOld.load_fit(load_transmission=True, load_path_override = r'data\example_td_ebin')

    # previous T(x) fit from S(E")
    LOld = Snorm2Tx()
    LOld.load_previous_fit(r'data\example_td_tx')
    LOld.plot_fit();


if calc_nonuni_spectrum:    
    N = ebin.EbinHapi(r'data/furnace_synth', bandwidth = band_fit)
    # 2) Select linelist to fit
    N.linelist_path = r'linelist/H2O_PaulLF.data' # Hitran-formatted PAR file
                         # must also have .header file of same name to run HAPI
    # Produce synthetic spectrum from known T(x) profile
    # How to calculate the transmission spectrum used in Furnace_Synth.asc
    N.tx_act_kelvin = np.asarray([547, 581, 634, 699, 771, 843, 908, 959, 991, 996, 
                                969, 903, 877, 822, 772, 724, 680, 638, 600, 564, 
                                531, 500, 471, 443, 418, 395, 372, 351, 331, 312])
    N.pathlength = 152.4 #cm
    N.t_celsius = np.round(np.average(N.tx_act_kelvin) - 273.15)
    N.x_wvn = np.arange(6802, 7000,.01) # 
    abs_nonuni, abs_uni = N.simulate_spectra(True)
    plt.figure(); plt.plot(N.x_wvn, abs_nonuni, label = 'nonuniform spectra')
    plt.plot(N.x_wvn, abs_uni, label = 'uniform-spectra approximation')
    plt.xlabel('Frequency (cm-1)'); plt.ylabel('Absorbance'); plt.legend()
    # data[:,1] = 100 * np.exp(-abs_nonuni) # how Furnace_Synth.asc transmission calculated
    
#    # Now load simulated spectrum into E"-bin fit
#    N.x_wvn = np.arange(6802, 7000,.01)
#    N.trans_spectrum = 100 * np.exp(-abs_nonuni)
#    N.print_thermo() # check that TPXL consistent with previous fit
    
    N.__cleanup__()


if new_fit:
    ##############################################################################
    ## Object-oriented time-domain fitting. 3-5 steps of preparation before fitting.
    # 1) Initialize the E"-binning object. 
    N = ebin.EbinHapi(file_name + 'new', bandwidth = band_fit)
    
    # 2) Select linelist to fit
    N.linelist_path = r'linelist/H2O_PaulLF.data' # Hitran-formatted PAR file
                         # must also have .header file of same name to run HAPI
    
    # 3) Pull in transmission spectrum and estimated path-average thermo parameters
    if calc_nonuni_spectrum:
        # standard method, if you don't already have ASC file
        N.x_wvn = np.arange(6802, 7000,.01)
        N.trans_spectrum = 100 * np.exp(-abs_nonuni)  
        # and update the path-average TPXL fits
        N.t_celsius = 380
        N.pathlength = 152.4
    else:
    # Furnace_Synth.asc file contains transmission spectrum in (wavenumber (cm-1), transmission),
    #  as well as estimated path-average thermodynamic parameters:
    #       p_torr, t_celsius, chi, pathlength (cm)
        N.get_transmission_asc(r'data\Furnace_Synth.asc')
    # 4) This function also updates thermodynamic parameters from asc file
    
    # 5) (optional) Update E"-bin selections.
    # The linelist is split into several different "molecules",
    # so each "molecule" has transition lower-state energies within these delineations
    N.Elist = [0,200,500,750,1020,1220,1440,1680,1940,2220,2510,2820,3100,7000]
    
    # 6) (optional) Update baseline and etalon list
    # N.bl = 100; N.etalons = [[100,120],[150,180]]
    
    ##############################################################################
    ## Now the actual fitting and analysis
    # Select any fit_snorm_* function for different amount of fit parameters
    # Fit concentrations of each E"-bin
    N.fit_snorm(); # the fastest fit, only float pathlength of each E"-bin.
    # All fit_ functions run N.spectrum_by_ebin() to make figure plot.
    #  and calculate baseline-removed spectrum N.data_meas
    # If plot is unseemly and slow, can also do N.plot_ebin() after running a fit_*()
    foo = N.fit_temperature() # plot linestrength curve and show nonuniformity evidence
 
    if load_previous:
        match_previous = np.allclose(NOld.snorm_out, N.snorm_out, .02) 
        if match_previous:
            print('Fit matches previous')
        else:
            print('New fit inconsistent with previous file')
    
## Optional re-fit of concentrations, also floating pressure-broadening of each E"-bin.
# This step is often critical to reduce linestrength error for E"<1500.
#  (see Ref 2, section 2.3: reducing lineshape error)
    if recommended_iteration:
        foo = N.fit_snorm_width_shift()
        print('Normalized linestrength (area/width fit)',N.snorm_out)
        print('Fitted P=',N.p_torr)
        
## Keep clean directory
# Save your fit to reload in another session
N.save_fit()
# Remove temporary linelist files from directory.
N.__cleanup__() # Must repeat N.get_linelist_par() to make another fit.

if temperature_inversion:
    # Now get temperature distribution from linestrengths
    L = Snorm2Tx(N)
    L.reg_weight = 10.**(np.arange(2,-5,-1))
    plot_handles = L.length_bin()
    L.save_fit()