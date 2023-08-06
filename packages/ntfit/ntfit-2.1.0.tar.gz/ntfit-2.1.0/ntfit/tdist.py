# -*- coding: utf-8 -*-
"""
Simulated annealing algorithm for Tikhonov regularization.
Get discretized temperature distribution from set of normalized linestrengths.

To use, write
tx_, res_, pxl_, reg_, corner = lbin_sa(meas, model)

Or object-oriented version:
L = Snorm2Tx(Ebin_Object)
plot_handles = L.length_bin()
L.save_fit()

MATH abbreviations:
sa = simulated annealing
reg = Tikhonov regularization
l2 = L2-norm matrix for 2nd-order Tikhonov regularization, ||d2f / dx2||
lsq = least-squares
n_ = number of thing
fx = f(x) objective function to minimize
uc = uncertainty

SPECTROSCOPY abbreviations
e, elower = lower-state energy E" (cm-1)
snorm = normalized linestrength
t = temperature (Kelvin)
db = database (aka reference). 
     t_db is reference temperature for linestrength-fitting
tx = T(x) temperature vs position profile, a length-bin discretization
pdf = Probability Density Function of pxl at each temperature
lbin = length-bin, where temperature profile split into several equal lengths.
uni = uniform-path, single-temperature fit
pxl = pressure*molefraction*pathlength product, (cm * atm)
      some count of number absorbing molecules

Development notes:
The central fitting code, tikhonov_sa comes from Corana et al[1].
My implementation for temperature nonuniformity is based on Cai et al [2]
I haven't seen that code, but the 2 ways this might be different is stability
for a single-path absorption measurement (rather than tomography),
with (1) the w_ub term in simulated annealing to encourage parabolic profiles,
and also (2) the L-curve as a lever between uniform and least-square profiles,
giving some uncertainty estimates in profile. These details in [3].

References:
[1] A Corana, M Marchesi, C Martini, S Ridella, "Minimizing multimodal functions
    of continuous variables with the 'simulated annealing' algorithm," 
ACM Trans. Math. Softw. 13 (3) 1987
[2] W Cai, D Ewing, L Ma, "Application of simulated annealing for multispectral
    tomography," Comp. Phys. Comm. 179 (4) 2008
[3] NA Malarich, GB Rieker, "Resolving nonuniform temperature distributions with
 single-beam absorption spectroscopy I) Theoretical capabilities and limitations,"
    JQSRT
    
Created on Sun Dec 22 10:41:41 2019

@author: Nathan Malarich
"""

import os
import numpy as np
from numpy.linalg import norm
#from numpy.matlib import repmat
from time import time
import matplotlib.pyplot as plt
import json
#from multiprocessing import Pool
from scipy.optimize import nnls

# partition function TIPS2017 from hapi (available HitranOnline)
from .hapi import partitionSum
FOUND_HAPI = True
HC_K = 1.4388028496642257

class Snorm2Tx():
    
    def __init__(self, EbinHapi=None):
        '''
        INPUT:
            EbinHapi spectral fitting object
            will pull all necessary variables from spectral fit object,
            and save to same directory with same basename.
            
            If you don't have an object handy in your IPython console, you can
            1) populate the 5 values manually
            2) Load a previous spectral fit from your hard drive
               >> N = ebin.EbinHapi(full_save_path)
               >> N.load_fit()
               >> L = Snorm2Tx(N)
        '''
        # E"-binning fit results
        if EbinHapi is not None:
            self.t_db = EbinHapi.t_celsius + 273
            self.elower = EbinHapi.ebin_xVals
            self.snorm = EbinHapi.snorm_out
            self.snorm_uc = EbinHapi.snorm_uc
            self.save_name = EbinHapi.full_output_name
            # and variables for Q(T)
            self.molec_id = EbinHapi.molec_id
            self.local_iso_id = EbinHapi.local_iso_id
        else:
            self.t_db = 0
            self.elower = None
            self.snorm = None
            self.snorm_uc = None
            self.save_name = None
            self.molec_id = 1
            self.local_iso_id = 1            
            print('Calculating linestrengths with H2O partition function')
            print('Use load_ebin() or load_previous_fit() before running other functions')
        
        self.model = None
        
        # length-binning parameters
        self.nbins = 16
        self.start_condition = 'uniform'
        self.tmin = 300
        self.tmax = max(1300, self.t_db + 400)
        self.reg_weight = 10.**-np.arange(5)
        self.corner_thrsh = 0.07
        
        # extreme-fit outputs
        self.tx_uni = None
        self.tx_lsq = None
        
        # length-binning outputs
        self.tx = None
        self.res = None
        self.pxl = None
        self.reg = None
        self.corner = None
    
    def length_bin(self, tmax_override = None):
        '''
        Run length-bin simulated annealing code.
        
        Same algorithm as lbin_sa(), 
        except outputs stay in Snorm_2Tx object instance
        '''
        ## For minimize ||Ax - b||, calculate matrix A and solution b
        # calculate weighted inversion matrix self.model_w
        model = self.get_model(tmax_override)
        meas_w = self.snorm / self.snorm_uc # solution vector
        
        # Calculate extreme-condition inversions
        self.tx_uni, self.res_uni, self.pxl_uni = uniform_fit(meas_w, self.model_w,
                                                              self.tmin, self.nbins)
        self.tx_lsq, self.res_lsq, self.pxl_lsq = lsq_fit(meas_w, self.model_w,
                                                          self.tmin, self.nbins)
        l2 = self.get_l2()
        self.reg_lsq = norm(l2 @ self.tx_lsq)
        if self.start_condition == 'uniform':
            tx0 = self.tx_uni
            pxl0 = self.pxl_uni
        else:
            tx0 = self.tx_lsq
            pxl0 = self.pxl_lsq
        
        # Now calculate Tikhonov inversion at several regularization weights
        self.tx = np.zeros((self.nbins, len(self.reg_weight)))
        self.pxl = np.zeros(len(self.reg_weight))
        self.res = np.zeros(len(self.reg_weight))
        self.reg = np.zeros(len(self.reg_weight))
        self.s_fit = np.zeros((len(self.elower), len(self.reg_weight)))
        tic = time()
        for i, reg in enumerate(self.reg_weight):
            self.tx[:,i], self.pxl[i], self.res[i] = tikhonov_sa(tx0, pxl0, meas_w, 
                   self.model_w, reg, nbins = self.nbins, tmin = self.tmin)
            self.s_fit[:,i] = res(self.tx[:,i], self.pxl[i], model)
            self.reg[i] = norm(l2 @ self.tx[:,i])
        print('Tikhonov regularization in %d seconds' % (time() - tic))
        fig, axs = self.plot_fit()
        
        return fig, axs
    
    '''
    Nest functions called within length_bin()
    '''    
    def plot_fit(self, plot_limits = False, vstack = False):
        '''
        Plots output of self.length_bin() and self.lcurve()
        INPUTS (optional):
            plot_limits = plot uniform and least-squares solutions as well
            vstack = stack subplots vertically (default horizontal)
        '''
        # edge cases
        if self.model is None:
            self.get_model()
        self.s_uni = res(self.tx_uni, self.pxl_uni, self.model)
        self.s_lsq = res(self.tx_lsq, self.pxl_lsq, self.model)
        
        bad_fits = self.lcurve()
        if vstack:
            fig, axs = plt.subplots(3,1)
            title_plot = 0
        else:
            fig, axs = plt.subplots(1,3)
            title_plot = 1
        # plot linestrengths
#        axs[0].set_title('Spectroscopy data')
        if plot_limits:
            axs[0].plot(self.elower, self.s_uni, 'k--', label='uniform')
            axs[0].plot(self.elower, self.s_lsq, 'k:', label='least-squares')
        if len(bad_fits) > 0:
            axs[0].plot(self.elower, self.s_fit[:, bad_fits], linewidth=0.5)
        axs[0].plot(self.elower, self.s_fit[:, self.corner_all], linewidth=2)
        axs[0].errorbar(self.elower, self.snorm, self.snorm_uc, color='k', ls='none')
        axs[0].plot(self.elower, self.snorm, 'k.', label = 'Data')
        axs[0].set_xlabel('Lower-state energy E"')
        axs[0].set_ylabel('Normalized linestrength')    
        
        # plot temperature distributions
#        axs[1].set_title('Temperature distribution')
        x = np.linspace(0,1, self.nbins)
        if plot_limits:
            axs[1].plot(x, self.tx_uni,'k--')
            axs[1].plot(x, np.sort(self.tx_lsq),'k:')
        for b in bad_fits:
            axs[1].plot(x, np.sort(self.tx[:,b]), linewidth=0.5)
        for c in self.corner_all:
            axs[1].plot(x, np.sort(self.tx[:, c]), linewidth=2)
        axs[1].set_xlabel('Column density fraction')
        axs[1].set_ylabel('Temperature (K)')
        axs[1].set_ylim(self.tmin, self.tmax)
        axs[1].set_xlim(0, 1)
        try:
            axs[title_plot].set_title(os.path.basename(self.save_name))
        except:
            pass
        
        # plot L-curve
#        axs[2].set_title('Tikhonov L-curve')
        for b in bad_fits:
            axs[2].plot(self.res[b], self.reg[b], '+')
        for c in self.corner_all:
            axs[2].plot(self.res[c], self.reg[c], '*')
        axs[2].set_xlabel('Linestrength residual')
        axs[2].set_ylabel('Temperature curvature')
        # Add uniform and leastsquare bounds to L-curve
        axs[2].plot(self.res_uni, 0, 'kx')
        axs[2].plot(min(self.res_lsq, min(self.res)), self.reg_lsq, 'kx')
        
        return fig, axs
                   
    def lcurve(self, thrsh_change = None):
        '''
        Calculates L-curve and decides which T(x) solutions within uncertainty.
        
        See Appendix 1 of Ref [3]        
        '''
        # Set up L-curve rectangle equation (Eq. A1 in ref [3])
        reg_uni = 0
        # bug fix: by discretizing tx_lsq, self.res_lsq could be higher residual
        res_lsq = min(self.res_lsq, min(self.res))
        y_reg = (self.reg - reg_uni) / self.reg_lsq
        x_res = (self.res - res_lsq) / self.res_uni
        reg_rectangle = np.sqrt( y_reg**2 + x_res**2 )
        self.corner = int(np.argmin(reg_rectangle))
        # corner_all are all solutions close enough to true L-curve corner.
        self.corner_all = []
        not_corner = []
        if thrsh_change is not None:
            self.corner_thrsh = thrsh_change
        for index, r in enumerate(reg_rectangle):
            if r < self.corner_thrsh:
                self.corner_all.append(index)
            else:
                not_corner.append(index)
        if len(self.corner_all) == 0:
            self.corner_all.append(self.corner)
        self.corner_all = np.asarray(self.corner_all).astype(int)
        not_corner = np.asarray(not_corner).astype(int)
        # Residual improvement from allowing nonuniformity
        res_corner = self.res[self.corner]
        nonuni_improvement = (self.res_uni - res_corner) / self.res_uni * 100
        print(int(nonuni_improvement), '% fit improvement from uniform-fit')
        
        return np.asarray(not_corner)

    def get_l2(self):
        '''
        Nested function to calculate matrix for 2nd-order Tikhonov regularization.
        
        Minimizes finite-difference d2T/dx2
        '''
        l2 = 2 * np.diag(np.ones(self.nbins))
        l2 -= np.diag(np.ones(self.nbins-1),1) + np.diag(np.ones(self.nbins-1),-1)
        l2[0,:] = 0; l2[-1,:] = 0 # ignore edges
        l2[-1,-1] = 2; l2[-1,-2] = -2 # add 2nd-derivative to high-temperature edge
        
        return l2
    
    def calc_hessian(self):
        '''
        Calculate nonlinear-least-squares Hessian matrix for length-bin result.
        
        H = A'A + gamma * L2'L2
        Weighted model matrix derivative A' = (1/snorm_uc_i) * d(snorm(Tj))/d(Tj)
        '''
        assert self.corner is not None, "run self.length_bin() first to get tx result."
        
        a = np.zeros((len(self.snorm), self.nbins))
        tx_best = self.tx[:,self.corner]
        for j, tj in enumerate(tx_best):
            j2 = int(min(tj - self.tmin, np.shape(self.model_w)[1] - 1))
            a[:,j] = self.model_w[:,j2+1] - self.model_w[:,j2]
        ata = np.transpose(a) @ a
        l = self.get_l2()
        ltl = np.transpose(l) @ l
        gamma = self.reg_weight[self.corner] # No rescaling
        
        return ata + gamma**2 * ltl
        # uc = np.sqrt(np.diag(np.linalg.inv(hessian))) ? 
        
    
    def get_model(self, tmax_override=None):
        '''
        Nested function to get normalized linestrength matrix
        INPUTS:
            tmax_override = maximum temperature-column of matrix (int/float)
            q_exact = use exact partition function from TIPS 
                       instead of power-law (Boolean)
        
        model_ij = integrated_area(E"_i) / (S_i(T_j) PXL)
        '''
        help_statement = "Load linestrengths with some load_*() function"
        help_statement += "before calling this function again."
        assert self.t_db != 0, help_statement
        # Set up absorption model
        
        # and model matrix
        if tmax_override is not None:
            self.tmax = tmax_override
        t = np.arange(self.tmin, self.tmax + 1)
        self.model_w = np.zeros((len(self.elower), len(t)))
        self.model = self.model_w.copy()
        for index, e in enumerate(self.elower):
            self.model[index,:] = s_t_exact(t, self.t_db, e, 
                                           self.molec_id, self.local_iso_id)
            self.model_w[index,:] = self.model[index,:] / self.snorm_uc[index]
#        snorm_repmat = np.transpose(repmat(self.snorm_uc, len(t),1))
#        model = self.model_w * snorm_repmat       
            
        return self.model
    
    def calc_uc(self, reg_index = None):
        '''
        Estimate statistical fitting uncertainty from Tikhonov result
        INPUT:
            reg_index = (int) which column of self.tx to calculate uncertainty.
                        default self.corner
                        
        TODO:
            Figure out why singular matrix for uniform retrieval.
            Is this invalidation of the Hessian derivation or method?
        '''
        assert self.tx is not None, "run self.length_bin() first to get tx result."
        
        if reg_index is None:
            reg_index = self.corner
        
        a = np.zeros((len(self.snorm), self.nbins + 1))
        tx_best = self.tx[:,reg_index]
        for j, tj in enumerate(tx_best):
            j2 = int(min(tj - self.tmin, np.shape(self.model_w)[1] - 2))
            a[:,j] = self.model_w[:,j2+1] - self.model_w[:,j2]
            a[:,-1] += self.model_w[:,j2] # d(snorm) / d(pxl)
        ata = np.transpose(a) @ a
        
        l = self.get_l2()
        l2 = np.zeros((self.nbins, self.nbins + 1)) # with extra pxl column
        l2[:,:-1] = l
        ltl = np.transpose(l2) @ l2
        gamma = self.reg_weight[reg_index] # No rescaling
        
        hessian = ata + gamma**2 * ltl
        uc = np.sqrt(np.diag(np.linalg.inv(hessian)))
        
#        # Uniform retrieval case, ignore possibility of nonuniformity
#        if max(tx_best) == min(tx_best):
#            a = np.zeros((len(self.snorm),2))
#            tj = tx_best[0]
#            j2 = int(min(tj - self.tmin, np.shape(self.model_w)[1] - 2))
#            a[:,0] = self.model_w[:,j2+1] - self.model_w[:,j2] # d(snorm) / dT
#            a[:,1] = self.model_w[:,j2] # d(snorm) / d(pxl)
#            ata = np.transpose(a) @ a
#            uc = np.sqrt(np.diag(np.linalg.inv(ata)))

        return uc
    
    def plot_uc(self, accepted_only = False):
        '''
        Plot temperature distribution (CDF) with statistical uncertainty.
        '''
        colors ='bgrcmyk'
        plt.figure('CDF_uc')
        if accepted_only:
            cdf_min = np.zeros((self.nbins, len(self.corner_all)))
            cdf_max = np.zeros((self.nbins, len(self.corner_all)))
            for i, r in enumerate(self.corner_all):
                tx = self.tx[:,r]
                uc = self.calc_uc(r)
                cdf = np.sort(tx)
                cdf_uc = uc[cdf.argsort()]
                plt.plot(cdf,'-',color=colors[r])
                plt.plot(cdf + cdf_uc,'--',color=colors[r])
                plt.plot(cdf - cdf_uc,'k--',color=colors[r])
                cdf_min[:,i] = cdf - cdf_uc
                cdf_max[:,i] = cdf + cdf_uc
            # Take total uncertainty to be span of each length-bin retrieval
            cdf_min = np.min(cdf_min, axis=1)
            cdf_max = np.max(cdf_max, axis=1)
            return cdf_min, cdf_max
        else:
            for r in range(len(self.reg_weight)):
                tx = self.tx[:,r]
                uc = self.calc_uc(r)
                cdf = np.sort(tx)
                cdf_uc = uc[cdf.argsort()]
                plt.plot(cdf,'-',color=colors[r])
                plt.plot(cdf + cdf_uc,'--',color=colors[r])
                plt.plot(cdf - cdf_uc,'k--',color=colors[r])
    
    '''
    Data-handling functions
    '''
    def save_fit(self, suffix = ''):
        '''
        Save fit result as dictionary to text file. 
        Can reload this information using load_previous_fit()
        
        INPUTS:
            suffix = addition to text file name, 
                     to indicate multiple fits to same data.
        '''
        # setup parameters
        fit = {'t_db':self.t_db}
        fit['elower'] = self.elower.tolist()
        fit['snorm'] = self.snorm.tolist()
        fit['snorm_uc'] = self.snorm_uc.tolist()
        fit['molec_id'] = self.molec_id
        fit['local_iso_id'] = self.local_iso_id
        fit['tmin'] = self.tmin
        fit['tmax'] = self.tmax
        if type(self.reg_weight) is not list:
            fit['reg_weight'] = self.reg_weight.tolist()
        else:
            fit['reg_weight'] = self.reg_weight
        # Tikhonov inversions
        fit['tx'] = np.transpose(self.tx).tolist()
        fit['pxl'] = self.pxl.tolist()
        fit['res'] = self.res.tolist()
        fit['reg'] = self.reg.tolist()
        fit['corner'] = int(self.corner)
        # edge cases
        fit['tx_uni'] = self.tx_uni.tolist()
        fit['pxl_uni'] = self.pxl_uni
        fit['res_uni'] = self.res_uni
        fit['tx_lsq'] = self.tx_lsq.tolist()
        fit['pxl_lsq'] = self.pxl_lsq
        fit['res_lsq'] = self.res_lsq
        fit['reg_lsq'] = self.reg_lsq
        with open(self.save_name + '_tx' + suffix,'w') as f:
            f.write(json.dumps(fit, indent=2))
            
        # Also save accepted length-bin fits to separate text file
        np.savetxt(self.save_name + '_tx' + suffix + '.txt', self.tx[:,self.corner_all])
        
    def load_previous_fit(self, file_name):
        '''
        Load length-binning fit from text file (from previous Snorm2Tx.save_fit())
        
        Can then run Snorm2Tx.lcurve() or Snorm2Tx.plot_fit()
        INPUTS:
            file_name = string name of file produced with earlier length-bin fit.
        '''
        with open(file_name,'r') as f:
            fit = json.loads(f.read())
        self.save_name = file_name
        self.t_db = fit['t_db']
        self.elower = np.asarray(fit['elower'])
        self.snorm = np.asarray(fit['snorm'])
        self.snorm_uc = np.asarray(fit['snorm_uc'])
        self.tmin = fit['tmin']
        self.tmax = fit['tmax']
        self.reg_weight = np.asarray(fit['reg_weight'])
        # Tikhonov inversions
        self.tx = np.transpose(np.asarray(fit['tx']))
        self.nbins = np.shape(self.tx)[0]
        self.pxl = np.asarray(fit['pxl'])
        self.res = np.asarray(fit['res'])
        self.reg = np.asarray(fit['reg'])
        self.corner = fit['corner']
        # edge cases
        self.tx_uni = np.asarray(fit['tx_uni'])
        self.pxl_uni = fit['pxl_uni']
        self.res_uni = fit['res_uni']
        self.tx_lsq = np.asarray(fit['tx_lsq'])
        self.pxl_lsq = fit['pxl_lsq']
        self.res_lsq = fit['res_lsq']
        self.reg_lsq = fit['reg_lsq']
        # Partition function
        try:
            self.molec_id = fit['molec_id']
            self.local_iso_id = fit['local_iso_id']
        except:
            self.molec_id = 1
            self.local_iso_id = 1
        
        # and calculate previous fit residuals
        model = self.get_model()
        self.s_fit = np.zeros((len(self.elower), len(self.reg_weight)))
        for i, reg in enumerate(self.reg_weight):
            self.s_fit[:,i] = res(self.tx[:,i], self.pxl[i], model)  
     
    def load_ebin(self, Ebin):
        '''
        Load EbinHapi object to later fit with self.length_bin()
        In case you forgot when you initialized this object.
        '''
        try:
            self.t_db = Ebin.t_celsius + 273
        except AttributeError:
            self.t_db = Ebin.temp_c + 273
        self.elower = Ebin.ebin_xVals
        self.snorm = Ebin.snorm_out
        self.snorm_uc = Ebin.snorm_uc
        self.save_name = Ebin.full_output_name        


'''
Nested codes in the setup of Snorm2Tx.length_bin
'''
def s_t(t_new, t0, elower, power=-2.77):
    '''
    Returns linestrengths at s(t_new) given array E"
    
    Used in Snorm2Tx.get_model
    '''
    return (t_new / t0)**power * np.exp(-HC_K * elower * (1/t_new - 1/t0))

def s_t_exact(t_new, t0, elower, molec_id = 1, iso = 1):
    '''
    Returns linestrengths at s(t_new) given array elower and partition function q
    '''
    q_t0 = partitionSum(molec_id, iso, t0)
    q_tnew = np.asarray(partitionSum(molec_id, iso, list(t_new)))
    boltz_t0 = np.exp(-HC_K * elower / t0) / (q_t0 * t0)
    boltz_t_new = np.exp(-HC_K * elower / t_new) / (q_tnew  * t_new)
    return boltz_t_new / boltz_t0

def uniform_fit(meas, model, tmin = 300, nbins = 30):
    '''
    What is single best T,X to fit normalized linestrengths?
    '''
    n_t = np.size(model,1)
    pxl_t = np.zeros(n_t)
    res_t = np.zeros(n_t)
    for t in range(n_t):
        pxl_t[t], res_t[t] = nnls(model[:,t:t+1], meas)
    t_uni = np.argmin(res_t) + tmin
    pxl_uni = pxl_t[t_uni - tmin]
    res_uni = res_t[t_uni - tmin] # 2-norm residual
    t_uni = t_uni * np.ones(nbins)
    
    return t_uni, res_uni, pxl_uni

def lsq_fit(meas, model, tmin = 300, nbins = 30):
    '''
    Get PDF(T) least-squares solution and turn into symmetric discrete profile.
    INPUTS:
        meas = normalized linestrengths vector
        model = inversion matrix (E" vs T)
        temp_array = (Kelvin) temperatures used for columns of model
        nbins = number of spots to split temperature
    TODO:
        lower temperature resolution 5 Kelvin?
    '''
    tx = np.zeros(nbins) # length-bin
    
    pdf, res_lsq = nnls(model, meas)
    pxl_lsq = sum(pdf)
    pdf *= nbins / pxl_lsq
#    cdf = np.zeros(len(pdf))
    
    # now round the continuous-numbered PDF into length bins
    lbin = 0; # length-bin index
    res_bin = 1
    # keep a weighted average of pdf until you hit next discretization point
    for ti in range(np.size(model,1)):
#        cdf[ti] = np.sum(pdf[:ti])
        if pdf[ti] > 0:
            li = pdf[ti]
            while li >= res_bin:
                tx[lbin] += res_bin * (ti + tmin)
                li -= res_bin
                lbin += 1; res_bin = 1
                lbin = min(lbin, nbins-1)
            # and save the leftovers
            res_bin -= li
            tx[lbin] += li * (ti + tmin)
       
#    # Last sort into symmetric profile with tmax in middle
#    tx_profile = np.zeros(nbins)
#    tx_profile[:nbins//2] = tx[range(0, nbins-1,2)]
#    tx_profile[:nbins//2-1:-1] = tx[range(1, nbins, 2)]
    tx_profile = tx
    
    # iterate on least-squares residual for discretization
    fit = res(tx_profile, pxl_lsq, model)
    res_lsq = norm(fit - meas)
    
    return tx_profile, res_lsq, pxl_lsq

def res(tx, pxl, model, tmin=300):
    '''
    Calculate linestrength fit model
    '''
    fit = np.zeros(np.shape(model)[0])
    nbins = np.shape(tx)[0]
    for t in tx:
        fit += pxl / nbins * model[:,int(t-tmin)]
    return fit

# The workhorse function
def tikhonov_sa(tx, pxl, meas, model, reg, eps = 1e-5, tmin = 300, nbins = 30):
    '''
    Simulated annealing algorithm based on Corana
    
    Minimize  ||     residual         || + || regularization ||
              ||meas - pxl * model(tx)|| + reg ||d2(tx) / dx2||
    
    Minimization function is nonlinear, so rather than separate objective function,
    just update the relevant portion for each search step.
    pxl * || meas/pxl - model(tx) ||
    
    Tends to produce uniform or parabolic profiles.    
    
    INPUS:
        tx = initial guess T(x) temperatures
        pxl = column density scaling factor, initial guess
        tmin = temperature of first
        meas = normalized linestrengths
        model = inversion matrix. Each column is temperature, 
                 starting at tmin and incrementing in 1 Kelvin
        AND simulated annealing parameters
        reg = regularization parameter
        t_sa = simulated annealing temperature
    TODO:
        lever-rule for Metropolis-Hastings search
        debugging
    '''
    ## Initialize Tikhonov fit residual
    tmin = int(tmin)
    tx = tx.astype(int)
    tx_best = tx.copy()
    pxl_best = pxl
    # Make L2 norm matrix
    l2 = 2 * np.diag(np.ones(nbins))
    l2 -= np.diag(np.ones(nbins-1),1) + np.diag(np.ones(nbins-1),-1)
    l2[0,:] = 0; l2[-1,:] = 0 # ignore edges
    l2[-1,-1] = 2; l2[-1,-2] = -2
    # evaluate vector of fit residual = measurement - model
    res = meas / pxl
    for ti in tx:
        res -= model[:, ti - tmin] / nbins
    fx_i = norm(res) * pxl + reg * norm(l2 @ tx)
    fx_best = fx_i
    
    ## initialize simulated annealing parameters from Corana
    # simulaed annealing steps
    t_sa = 10 # simulated annealing temperature
    cool_rate = 0.85
    n_t = min(100, 5 * nbins)
    return_flag = 0
    cooling_steps = 0 # number of times cooled
    max_steps = 100
    # metropolis-hastings solution search parameters
    lb = tmin * np.ones(nbins+1)
    ub = lb + np.size(model,1) - 1
    tstep = 50 * np.random.rand(nbins+1)
    minstep = 2 * np.ones(nbins+1)
    maxstep =  200 * np.ones(nbins+1)
    dilate = 1.8 * np.ones(nbins + 1) # how much to change the step size
    n_s = 20
    n_accept = np.zeros(nbins + 1)
    # Added Malarich parameters for tweaking Metropolis-Hastings search
    lever = 0.2
    w_ub = 0.01
    # special search parameters for pxl_factor
    lb[-1] = pxl / 1.5
    ub[-1] = pxl * 1.5
    tstep[-1] = .05
    minstep[-1] = .005
    maxstep[-1] = (ub[-1] - lb[-1]) / 5
    
    # Begin iterative optimization algorithm
    while return_flag < 1 and cooling_steps < max_steps:
        fx_start = fx_best
        for m in range(n_t):
            # update step size n_t times at each annealing temperature
            for j in range(n_s):
                # run n_s times at each search step size
                for h in range(nbins):
    # Step 1: generate a new test point
                    keep_searching = True; n_search = 0
                    tx_old = tx[h]
                    while keep_searching:
                        tshift = int(tstep[h] * np.random.randn()) # Gaussian search
                        # and add non-Gaussian search
                        if h == 0:
                            tx_reg = .5 * (lb[h] + tx[h + 1])
                        elif h == (nbins-1):
#                            tx_reg = 0.5 * (lb[h] + tx[h - 1])
                            tx_reg = w_ub * ub[h] + (1 - w_ub) * tx[h-1]
#                        elif h == nbins // 2:
#                        # If you set tx_reg = -100, then result will be M-shape profile
#                            tx_reg = w_ub * ub[h] + (1 - w_ub)/2 * (tx[h+1] + tx[h-1])
                        else:
                            tx_reg = .5 * (tx[h+1] + tx[h-1])
                        tx_test = tx_old + tshift + int(lever * (tx_reg - tx_old))
    # Step 2: is x in a priori domain?                        
                        if tx_test >= lb[h] and tx_test <= ub[h]:
                            keep_searching = False
                        n_search += 1
                        if n_search > 20:
                            tstep[h] = min(tstep[h] + 10, maxstep[h])   
    # Step 3: evaluate x_test, accept test point?
                    tx[h] = tx_test
                    res -= (model[:,tx_test-tmin] - model[:,tx_old - tmin])/nbins
                    ftest = norm(res) * pxl + reg * norm(l2 @ tx)
                    if ftest <= fx_i: # automatically accept new point
                        fx_i = ftest
                        n_accept[h] += 1
                        if ftest < fx_best:
                            tx_best = tx.copy()
                            fx_best = ftest
                            pxl_best = pxl
                    else: # possibly accept new point using annealing algorithm
                        probability_accept = np.exp((fx_i - ftest) / t_sa)
                        if probability_accept > np.random.rand():
                            fx_i = ftest
                            n_accept[h] += 1
                        else: # reject test point
                            tx[h] = tx_old
                            res += (model[:,tx_test-tmin] - model[:,tx_old - tmin])/nbins
    # Repeat steps 1-3 for pxl scaling parameter
                h = nbins
                keep_searching = True; n_search = 0
                while keep_searching:
                    pxl_test = pxl + (-1 + 2 * np.random.randn()) * tstep[-1]
                    n_search += 1
                    if pxl_test >= lb[h] and pxl_test <= ub[h]:
                        keep_searching = False
                    if n_search > 20:
                        tstep[h] = min(tstep[h] * 2, maxstep[h])   
                res += meas * (1/pxl_test - 1/pxl)
                ftest = norm(res) * pxl_test + reg * norm(l2 @ tx)
                if ftest <= fx_i: # automatically accept new point
                    fx_i = ftest
                    n_accept[h] += 1
                    pxl = pxl_test
                    if ftest < fx_best:
                        tx_best = tx.copy()
                        fx_best = ftest
                        pxl_best = pxl_test
                else: # possibly accept new point using annealing algorithm
                    probability_accept = np.exp((fx_i - ftest) / t_sa)
                    if probability_accept > np.random.rand():
                        fx_i = ftest
                        n_accept[h] += 1
                        pxl = pxl_test
                    else: # reject test point
                        res -= meas * (1/pxl_test - 1/pxl)
    # Step 5: update simulated annealing search parameters
            for u in range(nbins + 1):
                if n_accept[u] > 0.6 * n_s: # accepted >60% test points
                    step_new = tstep[u] * (1 + dilate[u] * (n_accept[u]/n_s - .6)/.4)
                    tstep[u] = min(maxstep[u], step_new)
                elif n_accept[u] < 0.4 * n_s: # didn't accept enough points
                    step_new = tstep[u] / (1 + dilate[u] * (.4 - n_accept[u]/n_s)/.4)
                    tstep[u] = max(minstep[u], step_new)
            n_accept[:] = 0 # reset count
    # Step 6: reduce simulated annealing "temperature"
        cooling_steps += 1
        t_sa *= cool_rate    
    # Step 7: does latest step 1-6 loop satisfy exit conditions?
        # exit conditions here: two cooling steps of miniscule residual improvement
        if fx_start - fx_best < eps:
            return_flag += 0.5
            # extra tweak: don't want to exit if t_sa too high and can't find minima
            if np.average(tstep[:-1]) > .99 * maxstep[0]:
                t_sa *= .2
                return_flag = 0
        else:
            return_flag = 0
        tx = tx_best.copy()
        pxl = pxl_best
        fx_i = fx_best
        # Last calcualte linestrength fit residual
        res = meas / pxl
        for t in tx:
            res -= model[:, t - tmin] / nbins
        res_best = pxl * norm(res)
                    
    return tx_best, pxl_best, res_best

'''
Other duplicated functions if you don't want object-oriented framework
'''
def lbin_sa(meas, model, start = 'uniform', nbins = 30, 
            reg_weight = 10.**np.asarray([-2,-1,0,1,2])):
    '''
    Length-bin simulated annealing master code.
    
    The non-object-oriented version of Snorm2Tx.length_bin()
    
    INPUTS:
        meas = normalized linestrengths vector
        model = PDF vs normalized linestrengths
        nbins = number of length-bins in temperature profile solution
        reg_weight = array of 
    '''
    
    tic = time()
    # Make L2 norm matrix
    l2 = 2 * np.diag(np.ones(nbins))
    l2 -= np.diag(np.ones(nbins-1),1) + np.diag(np.ones(nbins-1),-1)
    l2[0,:] = 0; l2[-1,:] = 0 # ignore edges
    # calculate the uniform and least-squares cases
    t_uni, res_uni, pxl_uni = uniform_fit(meas, model)
    reg_uni = 0 # by definition
    t_lsq, res_lsq, pxl_lsq = lsq_fit(meas, model)
    reg_lsq = norm(l2 @ t_lsq)
    reg_weight = np.asarray(reg_weight) * res_lsq
    if start == 'uniform':
        tx0 = t_uni
        pxl0 = pxl_uni
    else:
        tx0 = t_lsq
        pxl0 = pxl_lsq
    # run the Tikhonov
    tx_ = np.ones((nbins, len(reg_weight)))
    pxl_ = np.ones(len(reg_weight))
    res_ = np.ones(len(reg_weight))
    reg_ = np.ones(len(reg_weight))
    for i, reg in enumerate(reg_weight):
        tx_[:,i], pxl_[i], res_[i] = tikhonov_sa(tx0, pxl0, meas, model, reg,
              eps = res_lsq / 100, nbins = nbins)
        reg_ = norm(l2 @ tx_[:,i])
    # Now calculate the L-curve
    res_lsq = min(res_lsq, min(res_)) # mitigate discretization error
    reg_rectangle = np.sqrt( ((reg_ - reg_uni) / reg_lsq)**2 + 
                            ((res_ - res_lsq) / res_uni)**2)
    corner = np.argmin(reg_rectangle)
    print('Regularization in %d seconds' % (time() - tic))
    
    return tx_, res_, pxl_, reg_, corner

def objective(meas, tx, pxl, model, tmin=300):
    '''
    Calculate components of the objective function that tikhonov_sa() minimizes.
    '''
    # linestrength residual
    res = meas / pxl
    nbins = len(tx)
    for t in tx:
        res -= model[:, t - tmin] / nbins
    res_norm = norm(res) * pxl
    
    # and regularization
    l2 = 2 * np.diag(np.ones(nbins))
    l2 -= np.diag(np.ones(nbins-1),1) + np.diag(np.ones(nbins-1),-1)
    l2[0,:] = 0; l2[-1,:] = 0 # ignore edges
    reg_norm = norm(l2 @ tx)
    
    return res_norm, reg_norm