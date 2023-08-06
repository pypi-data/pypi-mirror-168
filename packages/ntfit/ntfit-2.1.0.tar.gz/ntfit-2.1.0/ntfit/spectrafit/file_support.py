# -*- coding: utf-8 -*-
import numpy as np
import os # or pathlib
from time import strftime, localtime
try:
    from .td_support import bandwidth_select_td
except:
    from td_support import bandwidth_select_td
    
class Transmission():
    def __init__(self, bandwidth=[6800,7100]):
        
        # transmission spectrum information
        self.trans_spectrum = None
        self.x_wvn = None
        self.wvn_start, self.wvn_stop = bandwidth
        self.transmission_path = '' # what file did transmission spectrum come from?
        
        # initialize thermodynamic parameters
        self.p_torr = 640
        self.t_celsius = 23
        self.chi = 0.01
        self.pathlength = 10 
                
    def get_transmission_asc(self, asc_file_path, overwrite_thermo=True):
        """
        Pulls important parameters from transmission file already formatted for Labfit
        
        INPUTS:
            asc_file_path = string name of transmission file (ignore .asc extension)
                            must be in labfit_engine directory else Labfit won't run
            self.wvn_start = fitting range for parameter
            
        OUTPUTS:
            Numpy arrays of frequency-domain transmission spectrum in object
            self.x_wvn = frequency axis (wavenumbers cm-1)
            self.trans_spectrum = intensity transmission (frequency-domain)
            
            Also pulls path-average thermo properties T,P,X,L from file
            self.pathlength
            self.t_celsius
            self.p_torr
            self.chi        
        """
        
        if '.asc' in asc_file_path:
        # Ignore .asc extension
            asc_file_path = asc_file_path[:-4]        
        self.transmission_path = os.path.abspath(asc_file_path) + '.asc'
        
        ## First extract path-average thermodynamic parameters
        if overwrite_thermo:
            with open(asc_file_path + '.asc','r') as f:
                for i in range(3):
                    f.readline()
                therm_line = f.readline()
                path_m, t_celsius, p_torr, chi = therm_line.split()[:4]
                self.pathlength = float(path_m) * 100 # cm
                self.t_celsius = float(t_celsius)
                self.p_torr = float(p_torr)
                self.chi = float(chi)

        ## Then get transmission spectrum
        self.x_wvn, self.trans_spectrum = np.loadtxt(asc_file_path + '.asc',unpack=True, skiprows=18)
        # last update the subset bandwidth
        # Check that transmission spectrum is large enough
        if self.x_wvn[0] > self.wvn_start:
            self.wvn_start = np.ceil(self.x_wvn[0])
            print('Bandwidth too large for transmission file.')
            print('Changing self.wvn_start = ', self.wvn_start)
        if self.x_wvn[-1] < self.wvn_stop:
            self.wvn_stop = np.floor(float(self.x_wvn[-1]))
            print('Bandwidth too large for transmission file.')
            print('Changing self.wvn_stop = ', self.wvn_stop)
        # Adjust array to match fit window with fast FFT for time-domain 
        x_start, x_stop = bandwidth_select_td(self.x_wvn, [self.wvn_start, self.wvn_stop])
        self.x_wvn = self.x_wvn[x_start:x_stop]
        self.trans_spectrum = self.trans_spectrum[x_start:x_stop]
        
    def make_asc(self, file_name = 'Spectrum007',
                 message = 'Data for E"-bin time-domain fitting', save_res = False):
        """
        Make Labfit-formatted transmission text file.
        18 lines of header, then space-delimited array x_wvn, trans
        
        INPUTS:
            self.trans_spectrum = laser transmission spectrum (y-axis numpy array)
            self.x_wvn = (cm-1) wavenumber of each data point (numpy array)
            self.p_torr, self.t_celsius, self.pathlength, self.chi = path-average properties
            file_name = name of output ASC file for Labfit
            save_res: if True, save absorbance residual in 3rd column (from self.spectrum_by_ebin())
            
        OUTPUTS:
            transFile.asc = Labfit-formatted transmission spectrum
            
        ASSUMPTIONS:
            self.wvn_start and self.wvn_stop are where you want them
            Actually Labfit can handle an ASC file larger than the fitting region
        
        """
        
        self.transmission_path = os.path.abspath(file_name) + '.asc' # !! possible bug: remove .txt or other file extension

        ## Format strings for ASC file conventions
        self.wvn_step = (self.x_wvn[-1] - self.x_wvn[0]) / (len(self.x_wvn) - 1) # :31f
        # Change T,P,X,L to formatted strings
        pathlength = self.pathlength/100; T_celsius = self.t_celsius; p_torr = self.p_torr
        if(pathlength < 10):
            pathlength = '{0:.7f}'.format(pathlength)
        elif(pathlength < 100):
            pathlength = '{0:.6f}'.format(pathlength)
        if(T_celsius < 100): # Assume T_celsius > 10c
            T_celsius = '{0:.4f}'.format(T_celsius)
        elif(T_celsius < 1000):
            T_celsius = '{0:.3f}'.format(T_celsius)
        else:
            T_celsius = '{0:.2f}'.format(T_celsius)
        if(p_torr < 10):
            p_torr = '{0:.5f}'.format(p_torr)
        elif(p_torr < 100):
            p_torr = '{0:.4f}'.format(p_torr)
        elif(p_torr < 1000):
            p_torr = '{0:.3f}'.format(p_torr)
        elif(p_torr < 10000):
           p_torr = '{0:.2f}'.format(p_torr)
        else:
            p_torr = '{0:.1f}'.format(p_torr)
        chi = '{0:.6f}'.format(self.chi)
        
        ## Now write to output file
        with open(self.transmission_path,'w') as out_file:
            file_id = '1111'
            out_file.write('******* File ' + file_id + ', ' + message + '\n')
            out_file.write(file_id+'   ')
            out_file.write(f'{self.x_wvn[0]:.10f}' + '  ')
            out_file.write(f'{self.x_wvn[-1]:.8f}'  + '  ')
            out_file.write( f'{self.wvn_step:.31f}' + '\n')
            out_file.write('  00000.00    0.00000     0.00e0     ')
            out_file.write('1   2     3   0        0\n') # Hitran molecule codes
            # Thermo line
            out_file.write(4*' ' + pathlength + 5*' ' + T_celsius + 6*' ' + 
                           p_torr + 4*' ' + chi + '    .0000000 .0000000 0.000\n')
            for i in range(2):
                out_file.write('    0.0000000     23.4486      0.00000    0.000000')
                out_file.write('    .0000000 .0000000 0.000\n')
            for i in range(9):
                out_file.write('1. 1. 1. 1. 1. 1. 1. 1. 1. 1.\n')
        # Other introductory lines
#            out_file.write('DATE ' + date + '; time ' + time + '\n')
            out_file.write(strftime("%m/%d/%Y %H:%M:%S\n", localtime()))
            out_file.write('\n')
            out_file.write('6801.3716254 0.003338200000000000000000000000 15031')
            out_file.write(' 1 1    2  0.9935  0.000   0.000 294.300 295.400')
            out_file.write(' 295.300   7.000  22.000 500.000 START\n')
         # Now write out transmission spectrum
            for count, vals in enumerate(self.x_wvn):
                out_file.write(f'{vals:.5f}' + 6*' ')
                out_file.write(f'{self.trans_spectrum[count]:.5f}')
                if save_res:
                    res_i = self.data_meas[count] - self.absorption_total[count]
                    out_file.write(6*' ' + f'{res_i:.5f}')
                out_file.write('\n')
