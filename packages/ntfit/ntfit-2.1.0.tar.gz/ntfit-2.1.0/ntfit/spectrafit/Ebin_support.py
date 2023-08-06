# -*- coding: utf-8 -*-
"""
Support scripts for Ebinning

Created on Mon Jul 22 12:18:12 2019

@author: Nate the Average
"""
import numpy as np

# hapi

try:
    from ..hapi import HITRAN_DEFAULT_HEADER, partitionSum 
    from ..hapi import absorptionCoefficient_Voigt, absorptionCoefficient_SDVoigt
except:
    from hapi_combustion import HITRAN_DEFAULT_HEADER, partitionSum, absorptionCoefficient_Voigt
    from hapi_combustion import absorptionCoefficient_SDVoigt
#find_package('pldspectrapy')
#from pldspectrapy.pldhapi import absorptionCoefficient_Voigt
HITRAN_DEFAULT_HEADER['default']['line_mixing_flag'] = 'E'
HITRAN_DEFAULT_HEADER['default']['gp'] = 0
HITRAN_DEFAULT_HEADER['default']['gpp'] = 0
HC_K = 1.4388028496642257 # physical constants for linestrength equation

###################
# S calculations
##################
def calc_smax(S0, elower, Tmax_gas):
    """
    Calculates S(T) where dS/dT = 0.
    
    Nest function for makeSrat() ReThrsh, where want to know if line should float or is too weak.
    
    TODO:
        Think about where I need this function.
        Maybe I should set up Smax just once when I initialize lineDict.
        And then think about precisely which parameters I need in lineDict vs sticking straight in .ref file.
    
    """
    S0 = float(S0); elower = float(elower) # make sure any strings converted to float.
    powerLaw = 2.77 # Power-law fit to T*Q(T) for H2O
    Tmax_S = min(HC_K * elower / powerLaw,Tmax_gas) #Cut off super highT lines if don't expect any temperature above 1300K
    if(Tmax_S > 296): #Don't expect sub-room temperature lines
        Smax = S0 * (Tmax_S / 296.)**(-powerLaw) * np.exp(-HC_K*elower*(1/Tmax_S - 1/296.))
    else:
        Smax = S0 # for all those lines with small E"
        
    return Smax


def snorm_fit_t_x(vars, s_e_array, thermo_old):#T_out, x_out, S0, elower, t_celsius, chi):
    """
    Calculates integrated area.
    Function to be called into scipy.optimize for updating T,X from initial guess

    find t_new, x_new to minimize integrated area residual
    min || int_alpha - S(T_new) P x_new L ||
    knowing snorm_meas = int_alpha / (S(T_0) P x_0 L)
    and assuming you can ignore scaling factors in front of equation
    which might be okay when already weighting each E"-bin by snorm_uc, yields
    
    min || snorm_meas (S(T_0) x_0 ) / (S(t_new) x_new) - 1 ||
    
    Uses power-law approximation for partition function Q_H2O(T)
    
    INPUTS:
        s_e_array: 3-column numpy float, with [E", S_norm, UC]
                 S_norm = (integrated area) / (S(T_old) P X_old L)
         thermo_old: [T_old (Celsius), x_old (molefraction)]
    """
    t_old = thermo_old[0] + 273 # initial guess temperature (Kelvin)
    x_old = thermo_old[1]
    
    thermo_old = vars.copy()
    
    # Fitted variables
    t_new = vars[0] + 273 # temperature (Kelvin)
    x_new = vars[1] # molefraction
    
    elower = s_e_array[:,0]
    snorm = s_e_array[:,1]
    uc = s_e_array[:,2]
    
    powerLaw = 2.77
    st_new_old = (t_new / t_old)**(-powerLaw) * np.exp(-HC_K * elower * (1/t_new - 1/t_old)) # S(T)_new / S(T)_old
    xt_old_over_new = (x_old / x_new) / st_new_old
    
    return (snorm * xt_old_over_new - 1) / uc # (nE x 1) array to minimize

def s_bkgd(vars, s_e_array, t_celsius, chi):
    '''
    Fits one temperature and roomT column density
    '''
    temp_old = t_celsius + 273
    t_new = vars[0]
    x_new = vars[1]
    x_bkgd = vars[2]
    
    elower = s_e_array[:,0]
    s_norm = s_e_array[:,1]
    uc = s_e_array[:,2]

    power = -2.77
    s_meas = s_norm * chi * temp_old**power * np.exp(-HC_K * elower / temp_old)
    s_t = t_new**power * np.exp(-HC_K * elower / t_new) * x_new
    s_bkgd = 296**power * np.exp(-HC_K * elower / 296) * x_bkgd
    
    return (s_meas - s_t - s_bkgd) / uc

def s_two_temp(vars, s_e_array, t_celsius, chi):
    '''
    Fits (T1, x1, T2, x2) from linestrength curve.
    Output temperatures in Kelvin
    '''
    temp_old = t_celsius + 273
    t1 = vars[0]
    t2 = vars[1]
    x1 = vars[2]
    x2 = vars[3]
    elower = s_e_array[:,0]
    s_norm = s_e_array[:,1]
    uc = s_e_array[:,2]
    
    power = -2.77
    s_meas = s_norm * chi * temp_old**power * np.exp(-HC_K * elower / temp_old)
    s_t1 = t1**power * np.exp(-HC_K * elower / t1) * x1
    s_t2 = t2**power * np.exp(-HC_K * elower / t2) * x2    
    return (s_meas - s_t1 - s_t2) / uc

def s_t(t_new, t0, elower, power=-2.77):
    '''
    Returns linestrengths at s(t_new) given array elower
    '''
    return (t_new / t0)**power * np.exp(-HC_K * elower * (1/t_new - 1/t0))

def s_t_exact(t_new, t0, elower, molec_id = 1, iso = 1):
    '''
    Returns linestrengths at s(t_new) given array elower and partition function q
    INPUTS:
        t_new = output evaluated temperature (Kelvin)
        t0 = reference temperature, 296 for HITRAN (Kelvin)
        elower = E" at which to calculate S(E") (int, float, numpy array)
        molec_id, iso = HITRAN molecule reference codes for partition function
    '''
    q_t0 = partitionSum(molec_id, iso, t0)
    if type(t_new) is np.ndarray:
        q_tnew = np.asarray(partitionSum(molec_id, iso, list(t_new)))
    else:
        q_tnew = np.asarray(partitionSum(molec_id, iso, t_new))
    boltz_t0 = np.exp(-HC_K * elower / t0) / (q_t0 * t0)
    boltz_t_new = np.exp(-HC_K * elower / t_new) / (q_tnew  * t_new)
    return boltz_t_new / boltz_t0

#####################
# Write par file ####
#####################
    
def write_par_line(line_dict, out_file):
    '''
    Write 160-char Hitran format transition in line_dict to out_file. 
    '''
    added_quanta = False
    for name in HITRAN_DEFAULT_HEADER['order']:
        try:
            value = line_dict[name]
        except KeyError:
            value = HITRAN_DEFAULT_HEADER['default'][name]
        if 'quanta' in name:
            # only count the quanta once
            if added_quanta is False:
                out_file.write('%60s' % line_dict['quanta'][:60])
                added_quanta = True
        else:
            name_format = HITRAN_DEFAULT_HEADER['format'][name]
            try:
                str_len = int(name_format.split('.')[0][1:])
            except ValueError:
                str_len = int(name_format[1:-1])
            if 's' not in name_format:
                value = float(value)
            value_str = name_format % value
            # Fix leading-zero bug on air-broadening parameters
            if len(value_str) > str_len:
                if value >= 0:
                    out_file.write(value_str[1:])
                else:
                    out_file.write('-.' + value_str.split('.')[1])
            else:
                out_file.write(value_str)
    out_file.write('\n')

############################
## Simulate absorption spectra (TD for time-domain, FD for frequency-domain)
############################
def calc_spectrum_fd(xx, mol_id, iso, molefraction, pressure, temperature, 
                     pathlength, shift, db_file_name='H2O', sdvoigt = False):
    '''
    Spectrum calculation for adding multiple models with composite model.
    
    See lmfit model page on prefix, parameter hints, composite models.
    
    INPUTS:
        xx -> wavenumber array (cm-1)
        name -> name of file (no extension) to pull linelist
        mol_id -> Hitran integer for molecule
        iso -> Hitran integer for isotope
        molefraction
        pressure -> (atmospheres)
        temperature -> kelvin
        pathlength (centimeters)
        shift -> (cm-1) calculation relative to Hitran
        db_file_name -> string name (no extension) of Hitran linelist file
    
    TODO: how to pull molecule name from prefix of call?
    '''
    if sdvoigt:
        nu, coef = absorptionCoefficient_SDVoigt(((int(mol_id), int(iso), molefraction),),
                db_file_name, HITRAN_units=False,
                OmegaGrid = xx + shift,
                Environment={'p':pressure,'T':temperature},
                Diluent={'self':molefraction,'air':(1-molefraction)}) 
    else:
        nu, coef = absorptionCoefficient_Voigt(((int(mol_id), int(iso), molefraction),),
                db_file_name, HITRAN_units=False,
                OmegaGrid = xx + shift,
                Environment={'p':pressure,'T':temperature},
                Diluent={'self':molefraction,'air':(1-molefraction)})
    absorp = coef * pathlength
    return absorp       
            
def calc_cepstrum_td(xx, mol_id, iso, molefraction, pressure, temperature, 
                     pathlength, shift, db_file_name='H2O', sdvoigt = False):
    '''
    Spectrum calculation for adding multiple models with composite model.
    
    See lmfit model page on prefix, parameter hints, composite models.
    
    INPUTS:
        xx -> wavenumber array (cm-1)
        name -> name of file (no extension) to pull linelist
        mol_id -> Hitran integer for molecule
        iso -> Hitran integer for isotope
        molefraction
        pressure -> (atmospheres)
        temperature -> kelvin
        pathlength (centimeters)
        shift -> (cm-1) calculation relative to Hitran
        db_file_name -> string name (no extension) of Hitran linelist file
    
    TODO: how to pull molecule name from prefix of call?
    '''
    absorp_fd = calc_spectrum_fd(xx, mol_id, iso, molefraction, pressure,
                                 temperature, pathlength, shift, db_file_name,
                                 sdvoigt)
    absorp_time_domain = np.fft.irfft(absorp_fd)
    return absorp_time_domain        

def spectra_allTD(vars, xx, data):
    molec_id = vars[0]
    local_iso_id = vars[1]
    pressure_atm = vars[2]
    temperature_kelvin = vars[3]
    molefraction = vars[4]
    pathlengths = vars[5]
    shift = vars[6]
    linelists = vars[7]
    absorption_all = np.zeros(len(xx))
    for i in range(len(pathlengths)):
        nu, coef = absorptionCoefficient_Voigt(((int(molec_id), int(local_iso_id), molefraction),),
                linelists[i], HITRAN_units=False,
                OmegaGrid = xx + shift,
                Environment={'p':pressure_atm,'T':temperature_kelvin},
                Diluent={'self':molefraction,'air':(1-molefraction)})
        absorption_all += pathlengths[i] * coef
    absorp_td = np.fft.irfft(absorption_all)
    return data - absorp_td

###############################
# Simulate nonuniform-path absorption spectra (frequency-domain)
###############################
