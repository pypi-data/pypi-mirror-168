# -*- coding: utf-8 -*-
"""
Helpful functions for time-domain fitting preparation.

td = time-domain

Created on Fri Nov  8 16:46:56 2019

@author: Nate the Average
"""

import numpy as np

def largest_prime_factor(n):
    i = 2
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
    return n


def bandwidth_select_td(x_array, band_fit, max_prime_factor = 500):
    '''
    Tweak bandwidth selection for swift time-domain fitting.
    
    Time-domain fit does inverse FFT for each nonlinear least-squares iteration,
    and speed of FFT goes with maximum prime factor.
    
    INPUTS:
        x_array = x-axis for measurement transmission spectrum
        band_fit = [start_frequency, stop_frequency]
    '''
    x_start = np.argmin(np.abs(x_array - band_fit[0]))
    x_stop = np.argmin(np.abs(x_array - band_fit[1]))
       
    prime_factor = largest_prime_factor(2 * (x_stop - x_start - 1))
    while prime_factor > max_prime_factor:
        x_stop -= 1
        prime_factor = largest_prime_factor(2 * (x_stop - x_start - 1))
    return x_start, x_stop

def weight_func(len_fd, bl, etalons = []):
    '''
    Time-domain weighting function, set to 0 over selected baseline, etalon range
    INPUTS:
        len_fd = length of frequency-domain spectrum
        bl = number of points at beginning to attribute to baseline
        etalons = list of [start_point, stop_point] time-domain points for etalon spikes
    '''
    weight = np.ones(2*(len_fd-1))
    weight[:bl] = 0; weight[-bl:] = 0
    for et in etalons:
        weight[et[0]:et[1]] = 0
        weight[-et[1]:-et[0]] = 0
    return weight