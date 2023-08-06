# -*- coding: utf-8 -*-

'''
This module provides an access to the HITRAN data.
Data is downloaded and cached.

This module serves as a simple database manager front end.

!!!!!!!!!!!!!!!!!!!
Changes to absorptionCoefficient_Voigt() and absorptionCoefficient_SDVoigt()
!!!!!!!!!!!!!!!!!!!
Rieker group group calculation updates labelled by 'pld_update' with contributor and date.
Update lineshape parameter-handling to be consistent with our in-house high-temperature databases.
-Added lineshift temperature-dependence exponent n_delta_air=1 to absorptionCoefficient_
 (Voigt and SDVoigt).
 Hapi assumes linear pressure-shift model parameter deltap_air, 
 except HitranOnline doesn't have many of those.
 In this version, hapi looks for deltap_, 
 and if it doesn't find it it uses a power-law model, looks for n_delta_,
 and if it can't find that assumes n_delta_ = 1
-Lorentz-broadening note: hapi looks for n_self, 
 and if it doesn't find that in the database, assumes n_self = n_air for the line.
 If you want to hard-code a particular n_self = 0.694 or similar, 
  must add comma-separated value to Hitran database file.
- SDVoigt has same temperature dependence in Gamma0 as Gamma0
'''

import sys
import json
import os, os.path
import re
from os import listdir
import numpy as np
from numpy import zeros,array,setdiff1d,ndarray,arange
from numpy import place,where,real,polyval
from numpy import complex128,int64,float64,float32
from numpy import sqrt,abs,exp,pi,log,sin,cos,tan
from numpy import convolve
from numpy import flipud
from numpy.fft import fft,fftshift
from numpy import linspace,floor
from numpy import any,minimum,maximum
from numpy import sort as npsort
from bisect import bisect
from warnings import warn,simplefilter
import pydoc
from .tips2017 import partitionSum, PYTIPS, PYTIPS2017

# Enable warning repetitions
simplefilter('always', UserWarning)

# Python 3 compatibility
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
if 'io' in sys.modules: # define open using Linux-style line endings
    import io
    def open_(*args,**argv):
        argv.update(dict(newline='\n'))
        return io.open(*args,**argv)
else:
    open_ = open

HAPI_VERSION = '1.1.0.9.6'; __version__ = HAPI_VERSION
HAPI_HISTORY = [
'FIXED GRID BUG (ver. 1.1.0.1)',
'FIXED OUTPUT FORMAT FOR CROSS-SECTIONS (ver. 1.1.0.1)',
'ADDED CPF BY SCHREIER (JQSRT_112_2011) (ver. 1.1.0.2)',
'OPTIMIZED EXPRESSION EVALUATIONS FOR SELECT (ver. 1.1.0.3)',
'ADDED SUPPORT FOR MIXTURES (ver. 1.1.0.4)',
'ADDED SUPPORT FOR USER-DEFINED ENV DEPENDENCES (ver. 1.1.0.5)',
'ADDED PROFILE SELECTION (ALPHA) (ver. 1.1.0.6)',
'ADDED METADATA FOR HTP, FIXED NORMALIZATION IN CONVOLVESPECTRUMSAME (ver. 1.1.0.7)',
'FIXED A "LONELY HEADER" BUG IN CACHE2STORAGE (ver. 1.1.0.7.1)',
'ADDED SUPPORT FOR PHOSGENE AND CYANOGEN (ver. 1.1.0.7.2)',
'OPTIMIZED STORAGE2CACHE (by Nils-Holger Loeber) (ver. 1.1.0.7.3)',
'ADDED SKIPABLE PARAMETERS IN HEADERS (ver. 1.1.0.7.4)',
'ADDED SUPPORT FOR FORTRAN D-NOTATION (ver. 1.1.0.7.5)',
'ADDED SUPPORT FOR WEIRD-FORMATTED INTENSITY VALUES E.G. "2.700-164" (ver. 1.1.0.7.6)',
'ADDED TIPS-2017 (ver. 1.1.0.8)',
'ADDED SUPPORT FOR CUSTOM EXTENSIONS OF THE DATA FILES (ver. 1.1.0.8.1)',
'FIXED LINK TO (2,0) ISOTOPOLOGUE IN TIPS-2017 (ver. 1.1.0.8.2)',
'ADDED SAVEHEADER FUNCTION (ver. 1.1.0.8.3)',
'ADDED METADATA FOR SF6 (ver. 1.1.0.8.4)',
'ADDED D2O ISOTOPOLOGUE OF WATER TO DESCRIPTION (ver. 1.1.0.8.5)',
'FIXED LINE ENDINGS IN STORAGE2CACHE AND QUERYHITRAN (ver. 1.1.0.8.6)',
'ADDED SUPPORT FOR NON-INTEGER LOCAL ISO IDS (ver. 1.1.0.8.7)',
'FIXED PARAMETER NAME CASE BUG (by Robert J. Hargreaves) (ver. 1.1.0.8.8)',
'CAST LOCAL_ISO_ID=0 TO 10 FOR CARBON DIOXIDE (ver. 1.1.0.8.9)',
'USING NUMPY.ARRAYS FOR NUMERIC COLUMNS OF LOCAL_TABLE_CACHE (ver. 1.1.0.9.0)',
'ADDED DESCRIPTIONS FOR BROADENING BY H2O (ver. 1.1.0.9.1)',
'ADDED PROXY SUPPORT IN FETCH AND FETCH_BY_IDS (ver. 1.1.0.9.2)',
'ADDED LIMIT FOR NUMBER OF LINES DURING TABLE READ (ver. 1.1.0.9.3)',
'FIXED ABSOLUTE PATH BUG IN TABLE NAMES (ver. 1.1.0.9.4)',
'CORRECTED ABUNDANCE OF THE HD ISOTOPOLOGUE (ver. 1.1.0.9.5)',
'ADDED UNIFIED INTERFACES FOR ABSCOEF AND XSC CALCULATIONS (ver. 1.1.0.9.6)',
]

# version header
print('HAPI version: 1.1.0.9.6 with power-law lineshape changes')
#print('To get the most up-to-date version please check http://hitran.org/hapi')
#print('ATTENTION: Python versions of partition sums from TIPS-2017 are now available in HAPI code')
##print('ATTENTION: Python versions of partition sums from TIPS-2017 are available at http://hitran.org/suppl/TIPS/')
##print('           To use them in HAPI ver. 1.1.0.7, use partitionFunction parameter of the absorptionCoefficient_ routine.')
#print('')
#print('           It is free to use HAPI. If you use HAPI in your research or software development,')
#print('           please cite it using the following reference:')
#print('           R.V. Kochanov, I.E. Gordon, L.S. Rothman, P. Wcislo, C. Hill, J.S. Wilzewski,')
#print('           HITRAN Application Programming Interface (HAPI): A comprehensive approach')
#print('           to working with spectroscopic data, J. Quant. Spectrosc. Radiat. Transfer 177, 15-30 (2016)')
#print('           DOI: 10.1016/j.jqsrt.2016.03.005')

# define precision
__ComplexType__ = complex128
__IntegerType__ = int64
__FloatType__ = float64

# define zero
cZero = __FloatType__(0.)

# physical constants
cBolts = 1.380648813E-16 # erg/K, CGS
cc = 2.99792458e10 # cm/s, CGS
hh = 6.626196e-27 # erg*s, CGS

# computational constants
cSqrtLn2divSqrtPi = 0.469718639319144059835
cLn2 = 0.6931471805599
cSqrtLn2 = 0.8325546111577
cSqrt2Ln2 = 1.1774100225

# initialize global variables
VARIABLES = {}

VARIABLES['DEBUG'] = False
if VARIABLES['DEBUG']: warn('DEBUG is set to True!')

GLOBAL_DEBUG = False
if GLOBAL_DEBUG: warn('GLOBAL_DEBUG is set to True!')

LOCAL_HOST = 'http://localhost'

# DEBUG switch
if GLOBAL_DEBUG:
   GLOBAL_HOST = LOCAL_HOST+':8000' # localhost
else:
   GLOBAL_HOST = 'http://hitran.org'

VARIABLES['PROXY'] = {}
# EXAMPLE OF PROXY:
# VARIABLES['PROXY'] = {'http': '127.0.0.1:80'}
   
# make it changeable
VARIABLES['GLOBAL_HOST'] = GLOBAL_HOST

# display the fetch URL (debug)
VARIABLES['DISPLAY_FETCH_URL'] = False

# In this "robust" version of arange the grid doesn't suffer 
# from the shift of the nodes due to error accumulation.
# This effect is pronounced only if the step is sufficiently small.
def arange_(lower,upper,step):
    npnt = floor((upper-lower)/step)+1
    upper_new = lower + step*(npnt-1)
    if abs((upper-upper_new)-step) < 1e-10:
        upper_new += step
        npnt += 1    
    return linspace(lower,upper_new,npnt)

# ---------------------------------------------------------------
# ---------------------------------------------------------------
# LOCAL DATABASE MANAGEMENT SYSTEM
# ---------------------------------------------------------------
# ---------------------------------------------------------------

# ---------------------------------------------------------------
# DATABASE BACKEND: simple text files, parsed into a python lists
# Use a directory as a database. Each table is stored in a 
# separate text file. Parameters in text are position-fixed.

BACKEND_DATABASE_NAME_DEFAULT = '.'

VARIABLES['BACKEND_DATABASE_NAME'] = BACKEND_DATABASE_NAME_DEFAULT

# For this node local DB is schema-dependent!
LOCAL_TABLE_CACHE = {
   'sampletab' : { # table
      'header' : { # header
         'order' : ('column1','column2','column3'),
         'format' : {
            'column1' : '%10d',
            'column2' : '%20f',
            'column3' : '%30s' 
         },
         'default' : {
            'column1' : 0,
            'column2' : 0.0,
            'column3' : ''
         },
         'number_of_rows' : 3,
         'size_in_bytes' : None,
         'table_name' : 'sampletab',
         'table_type' : 'strict'
      }, # /header
      'data' : {
         'column1' : [1,2,3],
         'column2' : [10.5,11.5,12.5],
         'column3' : ['one','two','three']
      }, # /data
   } # /table
} # hash-map of tables

# FORMAT CONVERSION LAYER

# converts between TRANSPORT_FORMAT and OBJECT_FORMAT
HITRAN_FORMAT_160 = {
   'M'          : {'pos' :   1,   'len' :  2,   'format' : '%2d' },
   'I'          : {'pos' :   3,   'len' :  1,   'format' : '%1d' },
   'nu'         : {'pos' :   4,   'len' : 12,   'format' : '%12f'},
   'S'          : {'pos' :  16,   'len' : 10,   'format' : '%10f'},
   'R'          : {'pos' :  26,   'len' :  0,   'format' : '%0f' },
   'A'          : {'pos' :  26,   'len' : 10,   'format' : '%10f'},
   'gamma_air'  : {'pos' :  36,   'len' :  5,   'format' : '%5f' },
   'gamma_self' : {'pos' :  41,   'len' :  5,   'format' : '%5f' },
   'E_'         : {'pos' :  46,   'len' : 10,   'format' : '%10f'},
   'n_air'      : {'pos' :  56,   'len' :  4,   'format' : '%4f' },
   'delta_air'  : {'pos' :  60,   'len' :  8,   'format' : '%8f' },
   'V'          : {'pos' :  68,   'len' : 15,   'format' : '%15s'},
   'V_'         : {'pos' :  83,   'len' : 15,   'format' : '%15s'},
   'Q'          : {'pos' :  98,   'len' : 15,   'format' : '%15s'},
   'Q_'         : {'pos' : 113,   'len' : 15,   'format' : '%15s'},
   'Ierr'       : {'pos' : 128,   'len' :  6,   'format' : '%6s' },
   'Iref'       : {'pos' : 134,   'len' : 12,   'format' : '%12s'},
   'flag'       : {'pos' : 146,   'len' :  1,   'format' : '%1s' },
   'g'          : {'pos' : 147,   'len' :  7,   'format' : '%7f' },
   'g_'         : {'pos' : 154,   'len' :  7,   'format' : '%7f' }
}

# This should be generating from the server's response
HITRAN_DEFAULT_HEADER = {
  "table_type": "column-fixed", 
  "size_in_bytes": -1, 
  "table_name": "###", 
  "number_of_rows": -1, 
  "order": [
    "molec_id", 
    "local_iso_id", 
    "nu", 
    "sw", 
    "a", 
    "gamma_air", 
    "gamma_self", 
    "elower", 
    "n_air", 
    "delta_air", 
    "global_upper_quanta", 
    "global_lower_quanta", 
    "local_upper_quanta", 
    "local_lower_quanta", 
    "ierr", 
    "iref", 
    "line_mixing_flag", 
    "gp", 
    "gpp"
  ],
  "format": {
    "a": "%10.3E", 
    "gamma_air": "%5.4f", 
    "gp": "%7.1f", 
    "local_iso_id": "%1d", 
    "molec_id": "%2d", 
    "sw": "%10.3E", 
    "local_lower_quanta": "%15s", 
    "local_upper_quanta": "%15s", 
    "gpp": "%7.1f", 
    "elower": "%10.4f", 
    "n_air": "%4.2f", 
    "delta_air": "%8.6f", 
    "global_upper_quanta": "%15s", 
    "iref": "%12s", 
    "line_mixing_flag": "%1s", 
    "ierr": "%6s", 
    "nu": "%12.6f", 
    "gamma_self": "%5.3f", 
    "global_lower_quanta": "%15s"
  }, 
  "default": {
    "a": 0.0, 
    "gamma_air": 0.0, 
    "gp": "FFF", 
    "local_iso_id": 0, 
    "molec_id": 0, 
    "sw": 0.0, 
    "local_lower_quanta": "000", 
    "local_upper_quanta": "000", 
    "gpp": "FFF", 
    "elower": 0.0, 
    "n_air": 0.0, 
    "delta_air": 0.0, 
    "global_upper_quanta": "000", 
    "iref": "EEE", 
    "line_mixing_flag": "EEE", 
    "ierr": "EEE", 
    "nu": 0.0, 
    "gamma_self": 0.0, 
    "global_lower_quanta": "000"
  },
  "description": {
    "a": "Einstein A-coefficient in s-1", 
    "gamma_air": "Air-broadened Lorentzian half-width at half-maximum at p = 1 atm and T = 296 K", 
    "gp": "Upper state degeneracy", 
    "local_iso_id": "Integer ID of a particular Isotopologue, unique only to a given molecule, in order or abundance (1 = most abundant)", 
    "molec_id": "The HITRAN integer ID for this molecule in all its isotopologue forms", 
    "sw": "Line intensity, multiplied by isotopologue abundance, at T = 296 K", 
    "local_lower_quanta": "Rotational, hyperfine and other quantum numbers and labels for the lower state of a transition", 
    "local_upper_quanta": "Rotational, hyperfine and other quantum numbers and labels for the upper state of a transition", 
    "gpp": "Lower state degeneracy", 
    "elower": "Lower-state energy", 
    "n_air": "Temperature exponent for the air-broadened HWHM", 
    "delta_air": "Pressure shift induced by air, referred to p=1 atm", 
    "global_upper_quanta": "Electronic and vibrational quantum numbers and labels for the upper state of a transition", 
    "iref": "Ordered list of reference identifiers for transition parameters", 
    "line_mixing_flag": "A flag indicating the presence of additional data and code relating to line-mixing", 
    "ierr": "Ordered list of indices corresponding to uncertainty estimates of transition parameters", 
    "nu": "Transition wavenumber", 
    "gamma_self": "Self-broadened HWHM at 1 atm pressure and 296 K", 
    "global_lower_quanta": "Electronic and vibrational quantum numbers and labels for the lower state of a transition"
  },
  "position": {
    "molec_id": 0,
    "local_iso_id": 2,
    "nu": 3,
    "sw": 15,
    "a": 25,
    "gamma_air": 35,
    "gamma_self": 40,
    "elower": 45,
    "n_air": 55,
    "delta_air": 59,
    "global_upper_quanta": 67,
    "global_lower_quanta": 82,
    "local_upper_quanta": 97,
    "local_lower_quanta": 112,
    "ierr": 127,
    "iref": 133,
    "line_mixing_flag": 145,
    "gp": 146,
    "gpp": 153,
  },
  'cast': {
    "molec_id": "uint8",
    "local_iso_id": "uint8",
    "nu": "float32",
    "sw": "float62",
    "a": "float62",
    "gamma_air": "float16",
    "gamma_self": "float16",
    "elower": "float32",
    "n_air": "float16",
    "delta_air": "float16",
    "global_upper_quanta": "str",
    "global_lower_quanta": "str",
    "local_upper_quanta": "str",
    "local_upper_quanta": "str",
    "ierr": "str",
    "iref": "str",
    "line_mixing_flag": "str",
    "gp": "int16",
    "gpp": "int16",  
  }
}

PARAMETER_META_ = \
{
  "global_iso_id" : {
    "id" : 1,
    "name" : "global_iso_id",
    "name_html" : "Global isotopologue ID",
    "table_name" : "",
    "description" : "Unique integer ID of a particular isotopologue: every global isotopologue ID is unique to a particular species, even between different molecules. The number itself is, however arbitrary.",
    "description_html" : "Unique integer ID of a particular isotopologue: every global isotopologue ID is unique to a particular species, even between different molecules. The number itself is, however arbitrary.",
    "default_fmt" : "%5d",
    "default_units" : "",
    "data_type" : "int",
    "selectable" : 1,
    "has_reference" : 0,
    "has_error" : 0
  },
  "molec_id" : {
    "id" : 2,
    "name" : "molec_id",
    "name_html" : "Molecule ID",
    "table_name" : "",
    "description" : "The HITRAN integer ID for this molecule in all its isotopologue forms",
    "description_html" : "The HITRAN integer ID for this molecule in all its isotopologue forms",
    "default_fmt" : "%2d",
    "default_units" : None,
    "data_type" : "int",
    "selectable" : 1,
    "has_reference" : 0,
    "has_error" : 0
  },
  "local_iso_id" : {
    "id" : 3,
    "name" : "local_iso_id",
    "name_html" : "Isotopologue ID",
    "table_name" : "",
    "description" : "Integer ID of a particular Isotopologue, unique only to a given molecule, in order or abundance (1 = most abundant)",
    "description_html" : "Integer ID of a particular Isotopologue, unique only to a given molecule, in order or abundance (1 = most abundant)",
    "default_fmt" : "%1d",
    "default_units" : "",
    "data_type" : "int",
    "selectable" : 1,
    "has_reference" : 0,
    "has_error" : 0
  },
  "nu" : {
    "id" : 4,
    "name" : "nu",
    "name_html" : "<em>&nu;</em>",
    "table_name" : "prm_nu",
    "description" : "Transition wavenumber",
    "description_html" : "Transition wavenumber",
    "default_fmt" : "%12.6f",
    "default_units" : "cm-1",
    "data_type" : "float",
    "selectable" : 1,
    "has_reference" : 1,
    "has_error" : 1
  },
  "sw" : {
    "id" : 5,
    "name" : "sw",
    "name_html" : "<em>S</em>",
    "table_name" : "prm_sw",
    "description" : "Line intensity, multiplied by isotopologue abundance, at T = 296 K",
    "description_html" : "Line intensity, multiplied by isotopologue abundance, at T&nbsp;=&nbsp;296&nbsp;K",
    "default_fmt" : "%10.3e",
    "default_units" : "cm-1/(molec.cm-2)",
    "data_type" : "float",
    "selectable" : 1,
    "has_reference" : 1,
    "has_error" : 1
  },
  "a" : {
    "id" : 6,
    "name" : "a",
    "name_html" : "<em>A</em>",
    "table_name" : "prm_a",
    "description" : "Einstein A-coefficient in s-1",
    "description_html" : "Einstein <em>A</em>-coefficient",
    "default_fmt" : "%10.3e",
    "default_units" : "s-1",
    "data_type" : "float",
    "selectable" : 1,
    "has_reference" : 0,
    "has_error" : 0
  },
  "gamma_air" : {
    "id" : 7,
    "name" : "gamma_air",
    "name_html" : "<em>&gamma;</em><sub>air</sub>",
    "table_name" : "prm_gamma_air",
    "description" : "Air-broadened Lorentzian half-width at half-maximum at p = 1 atm and T = 296 K",
    "description_html" : "Air-broadened Lorentzian half-width at half-maximum at p&nbsp;=&nbsp;1&nbsp;atm and T&nbsp;=&nbsp;296&nbsp;K",
    "default_fmt" : "%6.4f",
    "default_units" : "cm-1.atm-1",
    "data_type" : "float",
    "selectable" : 1,
    "has_reference" : 1,
    "has_error" : 1
  },
  "gamma_self" : {
    "id" : 8,
    "name" : "gamma_self",
    "name_html" : "<em>&gamma;</em><sub>self</sub>",
    "table_name" : "prm_gamma_self",
    "description" : "Self-broadened HWHM at 1 atm pressure and 296 K",
    "description_html" : "Self-broadened HWHM at 1&nbsp;atm pressure and 296&nbsp;K",
    "default_fmt" : "%5.3f",
    "default_units" : "cm-1.atm-1",
    "data_type" : "float",
    "selectable" : 1,
    "has_reference" : 1,
    "has_error" : 1
  },
  "n_air" : {
    "id" : 9,
    "name" : "n_air",
    "name_html" : "<em>n</em><sub>air</sub>",
    "table_name" : "prm_n_air",
    "description" : "Temperature exponent for the air-broadened HWHM",
    "description_html" : "Temperature exponent for the air-broadened HWHM",
    "default_fmt" : "%7.4f",
    "default_units" : "",
    "data_type" : "float",
    "selectable" : 1,
    "has_reference" : 1,
    "has_error" : 1
  },
  "delta_air" : {
    "id" : 10,
    "name" : "delta_air",
    "name_html" : "<em>&delta;</em><sub>air</sub>",
    "table_name" : "prm_delta_air",
    "description" : "Pressure shift induced by air, referred to p=1 atm",
    "description_html" : "Pressure shift induced by air, referred to <em>p</em>=1&nbsp;atm",
    "default_fmt" : "%9.6f",
    "default_units" : "cm-1.atm-1",
    "data_type" : "float",
    "selectable" : 1,
    "has_reference" : 1,
    "has_error" : 1
  },
  "elower" : {
    "id" : 11,
    "name" : "elower",
    "name_html" : "<em>E\"</em>",
    "table_name" : "",
    "description" : "Lower-state energy",
    "description_html" : "Lower-state energy",
    "default_fmt" : "%10.4f",
    "default_units" : "cm-1",
    "data_type" : "float",
    "selectable" : 1,
    "has_reference" : 0,
    "has_error" : 0
  },
  "gp" : {
    "id" : 12,
    "name" : "gp",
    "name_html" : "<em>g</em>\'",
    "table_name" : "",
    "description" : "Upper state degeneracy",
    "description_html" : "Upper state degeneracy",
    "default_fmt" : "%5d",
    "default_units" : "",
    "data_type" : "int",
    "selectable" : 1,
    "has_reference" : 0,
    "has_error" : 0
  },
  "gpp" : {
    "id" : 13,
    "name" : "gpp",
    "name_html" : "<em>g</em>\"",
    "table_name" : "",
    "description" : "Lower state degeneracy",
    "description_html" : "Lower state degeneracy",
    "default_fmt" : "%5d",
    "default_units" : "",
    "data_type" : "int",
    "selectable" : 1,
    "has_reference" : 0,
    "has_error" : 0
  },
  "global_upper_quanta" : {
    "id" : 14,
    "name" : "global_upper_quanta",
    "name_html" : "Global upper quanta",
    "table_name" : "",
    "description" : "Electronic and vibrational quantum numbers and labels for the upper state of a transition",
    "description_html" : "Electronic and vibrational quantum numbers and labels for the upper state of a transition",
    "default_fmt" : "%15s",
    "default_units" : None,
    "data_type" : "str",
    "selectable" : 0,
    "has_reference" : 0,
    "has_error" : 0
  },
  "global_lower_quanta" : {
    "id" : 15,
    "name" : "global_lower_quanta",
    "name_html" : "Global lower quanta",
    "table_name" : "",
    "description" : "Electronic and vibrational quantum numbers and labels for the lower state of a transition",
    "description_html" : "Electronic and vibrational quantum numbers and labels for the lower state of a transition",
    "default_fmt" : "%15s",
    "default_units" : None,
    "data_type" : "str",
    "selectable" : 0,
    "has_reference" : 0,
    "has_error" : 0
  },
  "local_upper_quanta" : {
    "id" : 16,
    "name" : "local_upper_quanta",
    "name_html" : "Local upper quanta",
    "table_name" : "",
    "description" : "Rotational, hyperfine and other quantum numbers and labels for the upper state of a transition",
    "description_html" : "Rotational, hyperfine and other quantum numbers and labels for the upper state of a transition",
    "default_fmt" : "%15s",
    "default_units" : None,
    "data_type" : "str",
    "selectable" : 0,
    "has_reference" : 0,
    "has_error" : 0
  },
  "local_lower_quanta" : {
    "id" : 17,
    "name" : "local_lower_quanta",
    "name_html" : "Local lower quanta",
    "table_name" : "",
    "description" : "Rotational, hyperfine and other quantum numbers and labels for the lower state of a transition",
    "description_html" : "Rotational, hyperfine and other quantum numbers and labels for the lower state of a transition",
    "default_fmt" : "%15s",
    "default_units" : None,
    "data_type" : "str",
    "selectable" : 0,
    "has_reference" : 0,
    "has_error" : 0
  },
  "line_mixing_flag" : {
    "id" : 18,
    "name" : "line_mixing_flag",
    "name_html" : "Line mixing flag",
    "table_name" : "",
    "description" : "A flag indicating the presence of additional data and code relating to line-mixing",
    "description_html" : "A flag indicating the presence of additional data and code relating to line-mixing",
    "default_fmt" : "%1s",
    "default_units" : "",
    "data_type" : "str",
    "selectable" : 0,
    "has_reference" : 0,
    "has_error" : 0
  },
  "ierr" : {
    "id" : 19,
    "name" : "ierr",
    "name_html" : "Error indices",
    "table_name" : "",
    "description" : "Ordered list of indices corresponding to uncertainty estimates of transition parameters",
    "description_html" : "Ordered list of indices corresponding to uncertainty estimates of transition parameters",
    "default_fmt" : "%s",
    "default_units" : "",
    "data_type" : "str",
    "selectable" : 0,
    "has_reference" : 0,
    "has_error" : 0
  },
  "iref" : {
    "id" : 20,
    "name" : "iref",
    "name_html" : "References",
    "table_name" : "",
    "description" : "Ordered list of reference identifiers for transition parameters",
    "description_html" : "Ordered list of reference identifiers for transition parameters",
    "default_fmt" : "%s",
    "default_units" : None,
    "data_type" : "str",
    "selectable" : 0,
    "has_reference" : 0,
    "has_error" : 0
  },
  "deltap_air" : {
    "id" : 21,
    "name" : "deltap_air",
    "name_html" : "<em>&delta;\'</em><sub>air</sub>",
    "table_name" : "prm_deltap_air",
    "description" : "Linear temperature dependence coefficient for air-induced pressure shift",
    "description_html" : "Linear temperature dependence coefficient for air-induced pressure shift",
    "default_fmt" : "%10.3e",
    "default_units" : "",
    "data_type" : "float",
    "selectable" : 1,
    "has_reference" : 1,
    "has_error" : 1
  },
  "n_self" : {
    "id" : 22,
    "name" : "n_self",
    "name_html" : "<em>n</em><sub>self</sub>",
    "table_name" : "prm_n_self",
    "description" : "Temperature exponent for the self-broadened HWHM",
    "description_html" : "Temperature exponent for the self-broadened HWHM",
    "default_fmt" : "%7.4f",
    "default_units" : "",
    "data_type" : "float",
    "selectable" : 1,
    "has_reference" : 1,
    "has_error" : 1
  },
  "delta_self" : {
    "id" : 23,
    "name" : "delta_self",
    "name_html" : "<em>&delta;</em><sub>self</sub>",
    "table_name" : "prm_delta_self",
    "description" : "Self-induced pressure shift, referred to p=1 atm",
    "description_html" : "Self-induced pressure shift, referred to <em>p</em>=1&nbsp;atm",
    "default_fmt" : "%9.6f",
    "default_units" : "cm-1.atm-1",
    "data_type" : "float",
    "selectable" : 1,
    "has_reference" : 1,
    "has_error" : 1
  },
  "deltap_self" : {
    "id" : 24,
    "name" : "deltap_self",
    "name_html" : "<em>&delta;\'</em><sub>self</sub>",
    "table_name" : "prm_deltap_self",
    "description" : "Linear temperature dependence coefficient for self-induced pressure shift",
    "description_html" : "Linear temperature dependence coefficient for self-induced pressure shift",
    "default_fmt" : "%10.3e",
    "default_units" : "",
    "data_type" : "float",
    "selectable" : 1,
    "has_reference" : 1,
    "has_error" : 1
  },
  "SD_air" : {
    "id" : 28,
    "name" : "SD_air",
    "name_html" : "SD</sub>air</sub>",
    "table_name" : "prm_sd_air",
    "description" : "Speed-dependence parameter, air-broadened lines",
    "description_html" : "Speed-dependence parameter, air-broadened lines",
    "default_fmt" : "%9.6f",
    "default_units" : "",
    "data_type" : "float",
    "selectable" : 1,
    "has_reference" : 1,
    "has_error" : 1
  },
  "SD_self" : {
    "id" : 29,
    "name" : "SD_self",
    "name_html" : "SD</sub>self</sub>",
    "table_name" : "prm_sd_self",
    "description" : "Speed-dependence parameter, self-broadened lines",
    "description_html" : "Speed-dependence parameter, self-broadened lines",
    "default_fmt" : "%9.6f",
    "default_units" : "",
    "data_type" : "float",
    "selectable" : 1,
    "has_reference" : 1,
    "has_error" : 1
  },
  "beta_g_air" : {
    "id" : 30,
    "name" : "beta_g_air",
    "name_html" : "<em>&beta;</em><sub>G, air</sub>",
    "table_name" : "prm_beta_g_air",
    "description" : "Dicke narrowing parameter for the air broadened Galatry line profile",
    "description_html" : "Dicke narrowing parameter for the air broadened Galatry line profile",
    "default_fmt" : "%9.6f",
    "default_units" : "",
    "data_type" : "float",
    "selectable" : 1,
    "has_reference" : 1,
    "has_error" : 1
  },
  "y_self" : {
    "id" : 31,
    "name" : "y_self",
    "name_html" : "<em>Y</em><sub>self</sub>",
    "table_name" : "prm_y_self",
    "description" : "First-order (Rosenkranz) line coupling coefficient; self-broadened environment",
    "description_html" : "First-order (Rosenkranz) line coupling coefficient; self-broadened environment",
    "default_fmt" : "%10.3e",
    "default_units" : "cm-1.atm-1",
    "data_type" : "float",
    "selectable" : 1,
    "has_reference" : 1,
    "has_error" : 1
  },
  "y_air" : {
    "id" : 32,
    "name" : "y_air",
    "name_html" : "<em>Y</em><sub>air</sub>",
    "table_name" : "prm_y_air",
    "description" : "First-order (Rosenkranz) line coupling coefficient; air-broadened environment",
    "description_html" : "First-order (Rosenkranz) line coupling coefficient; air-broadened environment",
    "default_fmt" : "%10.3e",
    "default_units" : "cm-1.atm-1",
    "data_type" : "float",
    "selectable" : 1,
    "has_reference" : 1,
    "has_error" : 1
  },
  "statep" : {
    "id" : 33,
    "name" : "statep",
    "name_html" : "qns\'",
    "table_name" : "",
    "description" : "Upper state quantum numbers",
    "description_html" : "Upper state quantum numbers",
    "default_fmt" : "%256s",
    "default_units" : "",
    "data_type" : "str",
    "selectable" : 1,
    "has_reference" : 0,
    "has_error" : 0
  },
  "statepp" : {
    "id" : 34,
    "name" : "statepp",
    "name_html" : "qns\"",
    "table_name" : "",
    "description" : "Lower state quantum numbers",
    "description_html" : "Lower state quantum numbers",
    "default_fmt" : "%256s",
    "default_units" : "",
    "data_type" : "str",
    "selectable" : 1,
    "has_reference" : 0,
    "has_error" : 0
  },
  "beta_g_self" : {
    "id" : 35,
    "name" : "beta_g_self",
    "name_html" : "<em>&beta;</em><sub>G, self</sub>",
    "table_name" : "prm_beta_g_self",
    "description" : "Dicke narrowing parameter for the self-broadened Galatry line profile",
    "description_html" : "Dicke narrowing parameter for the self-broadened Galatry line profile",
    "default_fmt" : "%9.6f",
    "default_units" : "",
    "data_type" : "float",
    "selectable" : 1,
    "has_reference" : 1,
    "has_error" : 1
  },
  "trans_id" : {
    "id" : 36,
    "name" : "trans_id",
    "name_html" : "Transition ID",
    "table_name" : "",
    "description" : "Unique integer ID of a particular transition entry in the database. (The same physical transition may have different IDs if its parameters have been revised or updated).",
    "description_html" : "Unique integer ID of a particular transition entry in the database. (The same physical transition may have different IDs if its parameters have been revised or updated).",
    "default_fmt" : "%12d",
    "default_units" : "",
    "data_type" : "int",
    "selectable" : 1,
    "has_reference" : 0,
    "has_error" : 0
  },
  "par_line" : {
    "id" : 37,
    "name" : "par_line",
    "name_html" : ".par line",
    "table_name" : "",
    "description" : "Native 160-character formatted HITRAN line",
    "description_html" : "Native 160-character formatted HITRAN line",
    "default_fmt" : "%160s",
    "default_units" : "",
    "data_type" : "str",
    "selectable" : 1,
    "has_reference" : 0,
    "has_error" : 0
  },
  "gamma_H2" : {
    "id" : 38,
    "name" : "gamma_H2",
    "name_html" : "<em>&gamma;</em><sub>H2</sub> ",
    "table_name" : "prm_gamma_H2",
    "description" : "Lorentzian lineshape HWHM due to pressure broadening by H2 at 1 atm pressure",
    "description_html" : "Lorentzian lineshape HWHM due to pressure broadening by H<sub>2</sub> at 1&nbsp;atm pressure",
    "default_fmt" : "%6.4f",
    "default_units" : "cm-1.atm-1",
    "data_type" : "float",
    "selectable" : 1,
    "has_reference" : 1,
    "has_error" : 1
  },
  "n_H2" : {
    "id" : 39,
    "name" : "n_H2",
    "name_html" : "<em>n</em><sub>H2</sub>",
    "table_name" : "prm_n_H2",
    "description" : "Temperature exponent for the H2-broadened HWHM",
    "description_html" : "Temperature exponent for the H<sub>2</sub>-broadened HWHM",
    "default_fmt" : "%7.4f",
    "default_units" : "",
    "data_type" : "float",
    "selectable" : 1,
    "has_reference" : 1,
    "has_error" : 1
  },
  "delta_H2" : {
    "id" : 40,
    "name" : "delta_H2",
    "name_html" : "<em>&delta;</em><sub>H2</sub>",
    "table_name" : "prm_delta_H2",
    "description" : "Pressure shift induced by H2, referred to p=1 atm",
    "description_html" : "Pressure shift induced by H<sub>2</sub>, referred to <em>p</em>=1&nbsp;atm",
    "default_fmt" : "%9.6f",
    "default_units" : "cm-1.atm-1",
    "data_type" : "float",
    "selectable" : 1,
    "has_reference" : 1,
    "has_error" : 1
  },
  "deltap_H2" : {
    "id" : 41,
    "name" : "deltap_H2",
    "name_html" : "<em>&delta;\'</em><sub>H2</sub>",
    "table_name" : "prm_deltap_H2",
    "description" : "Linear temperature dependence coefficient for H2-induced pressure shift",
    "description_html" : "Linear temperature dependence coefficient for H<sub>2</sub>-induced pressure shift",
    "default_fmt" : "%10.3e",
    "default_units" : "",
    "data_type" : "float",
    "selectable" : 1,
    "has_reference" : 1,
    "has_error" : 1
  },
  "gamma_He": {
    "id" : 42,
    "name" : "gamma_He",
    "name_html" : "<em>&gamma;</em><sub>He</sub> ",
    "table_name" : "prm_gamma_He",
    "description" : "Lorentzian lineshape HWHM due to pressure broadening by He at 1 atm pressure",
    "description_html" : "Lorentzian lineshape HWHM due to pressure broadening by He at 1&nbsp;atm pressure",
    "default_fmt" : "%6.4f",
    "default_units" : "cm-1.atm-1",
    "data_type" : "float",
    "selectable" : 1,
    "has_reference" : 1,
    "has_error" : 1
  },
  "n_He" : {
    "id" : 43,
    "name" : "n_He",
    "name_html" : "<em>n</em><sub>He</sub>",
    "table_name" : "prm_n_He",
    "description" : "Temperature exponent for the He-broadened HWHM",
    "description_html" : "Temperature exponent for the He-broadened HWHM",
    "default_fmt" : "%7.4f",
    "default_units" : "",
    "data_type" : "float",
    "selectable" : 1,
    "has_reference" : 1,
    "has_error" : 1
  },
  "delta_He" : {
    "id" : 44,
    "name" : "delta_He",
    "name_html" : "<em>&delta;</em><sub>He</sub>",
    "table_name" : "prm_delta_He",
    "description" : "Pressure shift induced by He, referred to p=1 atm",
    "description_html" : "Pressure shift induced by He, referred to <em>p</em>=1&nbsp;atm",
    "default_fmt" : "%9.6f",
    "default_units" : "cm-1.atm-1",
    "data_type" : "float",
    "selectable" : 1,
    "has_reference" : 1,
    "has_error" : 1
  },
  "gamma_CO2" : {
    "id" : 45,
    "name" : "gamma_CO2",
    "name_html" : "<em>&gamma;</em><sub>CO2</sub> ",
    "table_name" : "prm_gamma_CO2",
    "description" : "Lorentzian lineshape HWHM due to pressure broadening by CO2 at 1 atm pressure",
    "description_html" : "Lorentzian lineshape HWHM due to pressure broadening by CO<sub>2</sub> at 1&nbsp;atm pressure",
    "default_fmt" : "%6.4f",
    "default_units" : "cm-1.atm-1",
    "data_type" : "float",
    "selectable" : 1,
    "has_reference" : 1,
    "has_error" : 1
  },
  "n_CO2" : {
    "id" : 46,
    "name" : "n_CO2",
    "name_html" : "<em>n</em><sub>CO2</sub>",
    "table_name" : "prm_n_CO2",
    "description" : "Temperature exponent for the CO2-broadened HWHM",
    "description_html" : "Temperature exponent for the CO<sub>2</sub>-broadened HWHM",
    "default_fmt" : "%7.4f",
    "default_units" : "",
    "data_type" : "float",
    "selectable" : 1,
    "has_reference" : 1,
    "has_error" : 1
  },
  "delta_CO2" : {
    "id" : 47,
    "name" : "delta_CO2",
    "name_html" : "<em>&delta;</em><sub>CO2</sub>",
    "table_name" : "prm_delta_CO2",
    "description" : "Pressure shift induced by CO2, referred to p=1 atm",
    "description_html" : "Pressure shift induced by CO<sub>2</sub>, referred to <em>p</em>=1&nbsp;atm",
    "default_fmt" : "%9.6f",
    "default_units" : "cm-1.atm-1",
    "data_type" : "float",
    "selectable" : 1,
    "has_reference" : 1,
    "has_error" : 1
  }, 
  "gamma_HT_0_self_50" : {
    "default_fmt" : "%6.4f",
  },
  "n_HT_self_50" : {
    "default_fmt" : "%9.6f",
  },
  "gamma_HT_2_self_50" : {
    "default_fmt" : "%6.4f",
  },
  "delta_HT_0_self_50" : {
    "default_fmt" : "%9.6f",
  },
  "deltap_HT_self_50" : {
    "default_fmt" : "%9.6f",
  },
  "delta_HT_2_self_50" : {
    "default_fmt" : "%9.6f",
  },
  "gamma_HT_0_self_150" : {
    "default_fmt" : "%6.4f",
  },
  "n_HT_self_150" : {
    "default_fmt" : "%9.6f",
  },
  "gamma_HT_2_self_150" : {
    "default_fmt" : "%6.4f",
  },
  "delta_HT_0_self_150" : {
    "default_fmt" : "%9.6f",
  },
  "deltap_HT_self_150" : {
    "default_fmt" : "%9.6f",
  },
  "delta_HT_2_self_150" : {
    "default_fmt" : "%9.6f",
  },
  "gamma_HT_0_self_296" : {
    "default_fmt" : "%6.4f",
  },
  "n_HT_self_296" : {
    "default_fmt" : "%9.6f",
  },
  "gamma_HT_2_self_296" : {
    "default_fmt" : "%6.4f",
  },
  "delta_HT_0_self_296" : {
    "default_fmt" : "%9.6f",
  },
  "deltap_HT_self_296" : {
    "default_fmt" : "%9.6f",
  },
  "delta_HT_2_self_296" : {
    "default_fmt" : "%9.6f",
  },
  "gamma_HT_0_self_700" : {
    "default_fmt" : "%6.4f",
  },
  "n_HT_self_700" : {
    "default_fmt" : "%9.6f",
  },
  "gamma_HT_2_self_700" : {
    "default_fmt" : "%6.4f",
  },
  "delta_HT_0_self_700" : {
    "default_fmt" : "%9.6f",
  },
  "deltap_HT_self_700" : {
    "default_fmt" : "%9.6f",
  },
  "delta_HT_2_self_700" : {
    "default_fmt" : "%9.6f",
  },
  "nu_HT_self" : {
    "default_fmt" : "%6.4f",
  },
  "kappa_HT_self" : {
    "default_fmt" : "%9.6f",
  },
  "eta_HT_self" : {
    "default_fmt" : "%9.6f",
  },
  "gamma_HT_0_air_50" : {
    "default_fmt" : "%6.4f",
  },
  "n_HT_air_50" : {
    "default_fmt" : "%9.6f",
  },
  "gamma_HT_2_air_50" : {
    "default_fmt" : "%6.4f",
  },
  "delta_HT_0_air_50" : {
    "default_fmt" : "%9.6f",
  },
  "deltap_HT_air_50" : {
    "default_fmt" : "%9.6f",
  },
  "delta_HT_2_air_50" : {
    "default_fmt" : "%9.6f",
  },
  "gamma_HT_0_air_150" : {
    "default_fmt" : "%6.4f",
  },
  "n_HT_air_150" : {
    "default_fmt" : "%9.6f",
  },
  "gamma_HT_2_air_150" : {
    "default_fmt" : "%6.4f",
  },
  "delta_HT_0_air_150" : {
    "default_fmt" : "%9.6f",
  },
  "deltap_HT_air_150" : {
    "default_fmt" : "%9.6f",
  },
  "delta_HT_2_air_150" : {
    "default_fmt" : "%9.6f",
  },
  "gamma_HT_0_air_296" : {
    "default_fmt" : "%6.4f",
  },
  "n_HT_air_296" : {
    "default_fmt" : "%9.6f",
  },
  "gamma_HT_2_air_296" : {
    "default_fmt" : "%6.4f",
  },
  "delta_HT_0_air_296" : {
    "default_fmt" : "%9.6f",
  },
  "deltap_HT_air_296" : {
    "default_fmt" : "%9.6f",
  },
  "delta_HT_2_air_296" : {
    "default_fmt" : "%9.6f",
  },
  "gamma_HT_0_air_700" : {
    "default_fmt" : "%6.4f",
  },
  "n_HT_air_700" : {
    "default_fmt" : "%9.6f",
  },
  "gamma_HT_2_air_700" : {
    "default_fmt" : "%6.4f",
  },
  "delta_HT_0_air_700" : {
    "default_fmt" : "%9.6f",
  },
  "deltap_HT_air_700" : {
    "default_fmt" : "%9.6f",
  },
  "delta_HT_2_air_700" : {
    "default_fmt" : "%9.6f",
  },
  "nu_HT_air" : {
    "default_fmt" : "%6.4f",
  },
  "kappa_HT_air" : {
    "default_fmt" : "%9.6f",
  },
  "eta_HT_air" : {
    "default_fmt" : "%9.6f",
  },  
  "gamma_H2O" : {
    "default_fmt" : "%6.4f",
  },
  "n_H2O" : {
    "default_fmt" : "%9.6f",
  },
}

# lower the case of all parameter names (fix for case-sensitive databases)
PARAMETER_META = {}
for param in PARAMETER_META_:
    PARAMETER_META[param.lower()] = PARAMETER_META_[param]
    
# pld_update Nate Malarich 6June2019: allow shift temperature-scaling exponent
# Only look for this parameter if deltap doesn't exist (what if all values are zero?)
PARAMETER_META["n_delta_self"] = {"default_fmt":"%7.4f"}
PARAMETER_META["n_delta_air"] = {"default_fmt":"%7.4f"}
# end pld_update

def getFullTableAndHeaderName(TableName,ext=None):
    #print('TableName=',TableName)
    if ext is None: ext = 'data'
    flag_abspath = False # check if the supplied table name already contains absolute path
    if os.path.isabs(TableName): flag_abspath = True        
    fullpath_data = TableName + '.' + ext
    if not flag_abspath: fullpath_data = os.path.join(VARIABLES['BACKEND_DATABASE_NAME'],fullpath_data)
    if not os.path.isfile(fullpath_data):
        fullpath_data = VARIABLES['BACKEND_DATABASE_NAME'] + '/' + TableName + '.par'
        if not os.path.isfile(fullpath_data) and TableName!='sampletab':
            raise Exception('Lonely header \"%s\"' % fullpath_data)
    fullpath_header = TableName + '.header'
    if not flag_abspath: fullpath_header = os.path.join(VARIABLES['BACKEND_DATABASE_NAME'],fullpath_header)
    return fullpath_data,fullpath_header

def getParameterFormat(ParameterName,TableName):
    return LOCAL_TABLE_CACHE[TableName]['header']['format']

def getTableHeader(TableName):
    return LOCAL_TABLE_CACHE[TableName]['header']

def getRowObject(RowID,TableName):
    # return RowObject from TableObject in CACHE
    RowObject = []
    for par_name in LOCAL_TABLE_CACHE[TableName]['header']['order']:
        par_value = LOCAL_TABLE_CACHE[TableName]['data'][par_name][RowID]
        par_format = LOCAL_TABLE_CACHE[TableName]['header']['format'][par_name]
        RowObject.append((par_name,par_value,par_format))
    return RowObject

# INCREASE ROW COUNT
def addRowObject(RowObject,TableName):
    #print 'addRowObject: '
    #print 'RowObject: '+str(RowObject)
    #print 'TableName:'+TableName
    for par_name,par_value,par_format in RowObject:
        #print 'par_name,par_value,par_format: '+str((par_name,par_value,par_format))
        #print '>>> '+ str(LOCAL_TABLE_CACHE[TableName]['data'][par_name])
        #LOCAL_TABLE_CACHE[TableName]['data'][par_name] += [par_value]
        LOCAL_TABLE_CACHE[TableName]['data'][par_name].append(par_value)

def setRowObject(RowID,RowObject,TableName):
    number_of_rows = LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']
    if RowID >= 0 and RowID < number_of_rows:
       for par_name,par_value,par_format in RowObject:
           LOCAL_TABLE_CACHE[TableName]['data'][par_name][RowID] = par_value
    else:
       # !!! XXX ATTENTION: THIS IS A TEMPORARY INSERTION XXX !!!
       LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows'] += 1
       addRowObject(RowObject,TableName)

def getDefaultRowObject(TableName):
    # get a default RowObject from a table
    RowObject = []
    for par_name in LOCAL_TABLE_CACHE[TableName]['header']['order']:
        par_value = LOCAL_TABLE_CACHE[TableName]['header']['default'][par_name]
        par_format = LOCAL_TABLE_CACHE[TableName]['header']['format'][par_name]
        RowObject.append((par_name,par_value,par_format))
    return RowObject

def subsetOfRowObject(ParameterNames,RowObject):
    # return a subset of RowObject according to 
    #RowObjectNew = []
    #for par_name,par_value,par_format in RowObject:
    #     if par_name in ParameterNames:
    #        RowObjectNew.append((par_name,par_value,par_format))
    #return RowObjectNew
    dct = {}
    for par_name,par_value,par_format in RowObject:
        dct[par_name] = (par_name,par_value,par_format)
    RowObjectNew = []
    for par_name in ParameterNames:
        RowObjectNew.append(dct[par_name])
    return RowObjectNew

#FORMAT_PYTHON_REGEX = '^\%([0-9]*)\.?([0-9]*)([dfs])$'
FORMAT_PYTHON_REGEX = '^\%(\d*)(\.(\d*))?([edfsEDFS])$'

# Fortran string formatting
#  based on a pythonic format string
def formatString(par_format,par_value,lang='FORTRAN'):
    # Fortran format rules:
    #  %M.NP
    #        M - total field length (optional)
    #             (minus sign included in M)
    #        . - decimal ceparator (optional)
    #        N - number of digits after . (optional)
    #        P - [dfs] int/float/string
    # PYTHON RULE: if N is abcent, default value is 6
    regex = FORMAT_PYTHON_REGEX
    (lng,trail,lngpnt,ty) = re.search(regex,par_format).groups()
    result = par_format % par_value
    if ty.lower() in set(['f','e']):
       lng = int(lng) if lng else 0
       lngpnt = int(lngpnt) if lngpnt else 0
       result = par_format % par_value
       res = result.strip()
       if lng==lngpnt+1:
          if res[0:1]=='0':
             result =  '%%%ds' % lng % res[1:]
       if par_value<0:
          if res[1:2]=='0':
             result = '%%%ds' % lng % (res[0:1]+res[2:])
    return result

def putRowObjectToString(RowObject):
    # serialize RowObject to string
    # TODO: support different languages (C,Fortran)
    output_string = ''
    for par_name,par_value,par_format in RowObject:
        # Python formatting
        #output_string += par_format % par_value
        # Fortran formatting
        #print 'par_name,par_value,par_format: '+str((par_name,par_value,par_format))
        output_string += formatString(par_format,par_value)
    return output_string

# Parameter nicknames are hard-coded.
PARAMETER_NICKNAMES = {
    "a": "A", 
    "gamma_air": "gair", 
    "gp": "g", 
    "local_iso_id": "I", 
    "molec_id": "M", 
    "sw": "S", 
    "local_lower_quanta": "Q_", 
    "local_upper_quanta": "Q", 
    "gpp": "g_", 
    "elower": "E_", 
    "n_air": "nair", 
    "delta_air": "dair", 
    "global_upper_quanta": "V", 
    "iref": "Iref", 
    "line_mixing_flag": "f", 
    "ierr": "ierr", 
    "nu": "nu", 
    "gamma_self": "gsel", 
    "global_lower_quanta": "V_"
}  

def putTableHeaderToString(TableName):
    output_string = ''
    regex = FORMAT_PYTHON_REGEX
    for par_name in LOCAL_TABLE_CACHE[TableName]['header']['order']:
        par_format = LOCAL_TABLE_CACHE[TableName]['header']['format'][par_name]
        (lng,trail,lngpnt,ty) = re.search(regex,par_format).groups()
        fmt = '%%%ss' % lng
        try:
            par_name_short = PARAMETER_NICKNAMES[par_name]
        except:
            par_name_short = par_name
        #output_string += fmt % par_name
        output_string += (fmt % par_name_short)[:int(lng)]
    return output_string

def getRowObjectFromString(input_string,TableName):
    # restore RowObject from string, get formats and names in TableName
    #print 'getRowObjectFromString:'
    pos = 0
    RowObject = []
    for par_name in LOCAL_TABLE_CACHE[TableName]['header']['order']:
        par_format = LOCAL_TABLE_CACHE[TableName]['header']['format'][par_name]
        regex = '^\%([0-9]+)\.?[0-9]*([dfs])$' #
        regex = FORMAT_PYTHON_REGEX
        (lng,trail,lngpnt,ty) = re.search(regex,par_format).groups()
        lng = int(lng)
        par_value = input_string[pos:(pos+lng)]
        if ty=='d': # integer value
           par_value = int(par_value)
        elif ty.lower() in set(['e','f']): # float value
           par_value = float(par_value)
        elif ty=='s': # string value
           pass # don't strip string value
        else:
           print('err1')
           raise Exception('Format \"%s\" is unknown' % par_format)
        RowObject.append((par_name,par_value,par_format))
        pos += lng
    # Do the same but now for extra (comma-separated) parameters
    if 'extra' in set(LOCAL_TABLE_CACHE[TableName]['header']):
        csv_chunks = input_string.split(LOCAL_TABLE_CACHE[TableName]['header'].\
                                        get('extra_separator',','))
        # Disregard the first "column-fixed" container if it presents:
        if LOCAL_TABLE_CACHE[TableName]['header'].get('order',[]):
            pos = 1
        else:
            pos = 0
        for par_name in LOCAL_TABLE_CACHE[TableName]['header']['extra']:
            par_format = LOCAL_TABLE_CACHE[TableName]['header']['extra_format'][par_name]
            regex = '^\%([0-9]+)\.?[0-9]*([dfs])$' #
            regex = FORMAT_PYTHON_REGEX
            (lng,trail,lngpnt,ty) = re.search(regex,par_format).groups()
            lng = int(lng)
            par_value = csv_chunks[pos]
            if ty=='d': # integer value
                try:
                    par_value = int(par_value)
                except:
                    par_value = 0
            elif ty.lower() in set(['e','f']): # float value
                try:
                    par_value = float(par_value)
                except:
                    par_value = 0.0
            elif ty=='s': # string value
                pass # don't strip string value
            else:
                print('err')
                raise Exception('Format \"%s\" is unknown' % par_format)
            RowObject.append((par_name,par_value,par_format))
            pos += 1   
    return RowObject

# Conversion between OBJECT_FORMAT and STORAGE_FORMAT
# This will substitute putTableToStorage and getTableFromStorage
def cache2storage(TableName):
    try:
       os.mkdir(VARIABLES['BACKEND_DATABASE_NAME'])
    except:
       pass
    #fullpath_data,fullpath_header = getFullTableAndHeaderName(TableName) # "lonely header" bug
    fullpath_data = VARIABLES['BACKEND_DATABASE_NAME'] + '/' + TableName + '.data' # bugfix
    fullpath_header = VARIABLES['BACKEND_DATABASE_NAME'] + '/' + TableName + '.header' # bugfix
    OutfileData = open(fullpath_data,'w')
    OutfileHeader = open(fullpath_header,'w')
    # write table data
    line_count = 1
    line_number = LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']
    for RowID in range(0,line_number):
        line_count += 1
        RowObject = getRowObject(RowID,TableName)
        raw_string = putRowObjectToString(RowObject)
        OutfileData.write(raw_string+'\n')
    # write table header
    TableHeader = getTableHeader(TableName)
    OutfileHeader.write(json.dumps(TableHeader,indent=2))
    
def storage2cache(TableName,cast=True,ext=None,nlines=None):
    """ edited by NHL
    TableName: name of the HAPI table to read in
    ext: file extension
    nlines: number of line in the block; if None, read all line at once 
    """
    #print 'storage2cache:'
    #print('TableName',TableName)
    if nlines is not None:
        print('WARNING: storage2cache is reading the block of maximum %d lines'%nlines)
    fullpath_data,fullpath_header = getFullTableAndHeaderName(TableName,ext)
    if TableName in LOCAL_TABLE_CACHE and \
       'filehandler' in LOCAL_TABLE_CACHE[TableName] and \
       LOCAL_TABLE_CACHE[TableName]['filehandler'] is not None:
        InfileData = LOCAL_TABLE_CACHE[TableName]['filehandler'] 
    else:
        InfileData = open_(fullpath_data,'r')            
    InfileHeader = open(fullpath_header,'r')
    #try:
    header_text = InfileHeader.read()
    try:
        Header = json.loads(header_text)
    except:
        print('HEADER:')
#        print(header_text)
        raise Exception('Invalid header')
    #print 'Header:'+str(Header)
    LOCAL_TABLE_CACHE[TableName] = {}
    LOCAL_TABLE_CACHE[TableName]['header'] = Header
    LOCAL_TABLE_CACHE[TableName]['data'] = {}    
    LOCAL_TABLE_CACHE[TableName]['filehandler'] = InfileData
    # Check if Header['order'] and Header['extra'] contain
    #  parameters with same names, raise exception if true.
    #intersct = set(Header['order']).intersection(set(Header.get('extra',[])))
    intersct = set(Header.get('order',[])).intersection(set(Header.get('extra',[])))
    if intersct:
        raise Exception('Parameters with the same names: {}'.format(intersct))
    # initialize empty data to avoid problems
    glob_order = []; glob_format = {}; glob_default = {}
    if "order" in LOCAL_TABLE_CACHE[TableName]['header'].keys():
        glob_order += LOCAL_TABLE_CACHE[TableName]['header']['order']
        glob_format.update(LOCAL_TABLE_CACHE[TableName]['header']['format'])
        glob_default.update(LOCAL_TABLE_CACHE[TableName]['header']['default'])
        for par_name in LOCAL_TABLE_CACHE[TableName]['header']['order']:
            LOCAL_TABLE_CACHE[TableName]['data'][par_name] = []
    if "extra" in LOCAL_TABLE_CACHE[TableName]['header'].keys():
        glob_order += LOCAL_TABLE_CACHE[TableName]['header']['extra']
        glob_format.update(LOCAL_TABLE_CACHE[TableName]['header']['extra_format'])
        for par_name in LOCAL_TABLE_CACHE[TableName]['header']['extra']:
            glob_default[par_name] = PARAMETER_META[par_name]['default_fmt']
            LOCAL_TABLE_CACHE[TableName]['data'][par_name] = []
    
    header = LOCAL_TABLE_CACHE[TableName]['header']
    if 'extra' in header and header['extra']:
        line_count = 0
        flag_EOF = False
        #line_number = LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']
        #for line in InfileData:
        while True:
            #print '%d line from %d' % (line_count,line_number)
            #print 'line: '+line #
            if nlines is not None and line_count>=nlines: break
            line = InfileData.readline()
            if line=='': # end of file is represented by an empty string
                flag_EOF = True
                break 
            try:
                RowObject = getRowObjectFromString(line,TableName)
                line_count += 1
            except:
                continue
            #print 'RowObject: '+str(RowObject)
            addRowObject(RowObject,TableName)
        #except:
        #    raise Exception('TABLE FETCHING ERROR')
        LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows'] = line_count
    else:
        quantities = header['order']
        formats = [header['format'][qnt] for qnt in quantities]
        types = {'d':int, 'f':float, 'E':float, 's':str}
        converters = []
        end = 0
        for qnt, fmt in zip(quantities, formats):
            # pre-defined positions are needed to skip the existing parameters in headers (new feature)
            if 'position' in header:
                start = header['position'][qnt]
            else:
                start = end
            dtype = types[fmt[-1]]
            aux = fmt[fmt.index('%')+1:-1]
            if '.' in aux:
                aux = aux[:aux.index('.')]
            size = int(aux)
            end = start + size
            def cfunc(line, dtype=dtype, start=start, end=end, qnt=qnt):
                # return dtype(line[start:end]) # this will fail on the float number with D exponent (Fortran notation)
                if dtype==float:
                    try:
                        return dtype(line[start:end])
                    except ValueError: # possible D exponent instead of E 
                        try:
                            return dtype(line[start:end].replace('D','E'))
                        except ValueError: # this is a special case and it should not be in the main version tree!
                            # Dealing with the weird and unparsable intensity format such as "2.700-164, i.e with no E or D characters.
                            res = re.search('(\d\.\d\d\d)\-(\d\d\d)',line[start:end])
                            if res:
                                return dtype(res.group(1)+'E-'+res.group(2))
                            else:
                                raise Exception('PARSE ERROR: unknown format of the par value (%s)'%line[start:end])
                elif dtype==int and qnt=='local_iso_id':
                    if line[start:end]=='0': return 10
                    try:
                        return dtype(line[start:end])
                    except ValueError:
                        # convert letters to numbers: A->11, B->12, etc... ; .par file must be in ASCII or Unicode.
                        return 11+ord(line[start:end])-ord('A')
                else:
                    return dtype(line[start:end])
            #cfunc.__doc__ = 'converter {} {}'.format(qnt, fmt) # doesn't work in earlier versions of Python
            converters.append(cfunc)
            #start = end
        #data_matrix = [[cvt(line) for cvt in converters] for line in InfileData]
        flag_EOF = False
        line_count = 0
        data_matrix = []
        while True:
            if nlines is not None and line_count>=nlines: break   
            line = InfileData.readline()
            if line=='': # end of file is represented by an empty string
                flag_EOF = True
                break 
            data_matrix.append([cvt(line) for cvt in converters])
            line_count += 1
        data_columns = zip(*data_matrix)
        for qnt, col in zip(quantities, data_columns):
            #LOCAL_TABLE_CACHE[TableName]['data'][qnt].extend(col) # old code
            if type(col[0]) in {int,float}:
                LOCAL_TABLE_CACHE[TableName]['data'][qnt] = np.array(col) # new code
            else:
                LOCAL_TABLE_CACHE[TableName]['data'][qnt].extend(col) # old code
            #LOCAL_TABLE_CACHE[TableName]['data'][qnt] = list(col)
            #LOCAL_TABLE_CACHE[TableName]['data'][qnt] = col
        header['number_of_rows'] = line_count = (
            len(LOCAL_TABLE_CACHE[TableName]['data'][quantities[0]]))
    
    # Delete all character-separated values, treat them as column-fixed.
    try:
        del LOCAL_TABLE_CACHE[TableName]['header']['extra']
        del LOCAL_TABLE_CACHE[TableName]['header']['extra_format']
        del LOCAL_TABLE_CACHE[TableName]['header']['extra_separator']
    except:
        pass
    # Update header.order/format with header.extra/format if exist.
    LOCAL_TABLE_CACHE[TableName]['header']['order'] = glob_order
    LOCAL_TABLE_CACHE[TableName]['header']['format'] = glob_format
    LOCAL_TABLE_CACHE[TableName]['header']['default'] = glob_default
    if flag_EOF:
        InfileData.close()
        LOCAL_TABLE_CACHE[TableName]['filehandler'] = None
    InfileHeader.close()
#    print('                     Lines parsed: %d' % line_count)
    return flag_EOF    
    
## old version based on regular expressions    
#def storage2cache(TableName):
#    fullpath_data,fullpath_header = getFullTableAndHeaderName(TableName)
#    InfileData = open(fullpath_data,'r')
#    InfileHeader = open(fullpath_header,'r')
#    #try:
#    header_text = InfileHeader.read()
#    try:
#        Header = json.loads(header_text)
#    except:
#        print('HEADER:')
#        print(header_text)
#        raise Exception('Invalid header')
#    LOCAL_TABLE_CACHE[TableName] = {}
#    LOCAL_TABLE_CACHE[TableName]['header'] = Header
#    LOCAL_TABLE_CACHE[TableName]['data'] = {}
#    # Check if Header['order'] and Header['extra'] contain
#    #  parameters with same names, raise exception if true.
#    intersct = set(Header.get('order',[])).intersection(set(Header.get('extra',[])))
#    if intersct:
#        raise Exception('Parameters with the same names: {}'.format(intersct))
#    # initialize empty data to avoid problems
#    glob_order = []; glob_format = {}; glob_default = {}
#    if "order" in LOCAL_TABLE_CACHE[TableName]['header'].keys():
#        glob_order += LOCAL_TABLE_CACHE[TableName]['header']['order']
#        glob_format.update(LOCAL_TABLE_CACHE[TableName]['header']['format'])
#        glob_default.update(LOCAL_TABLE_CACHE[TableName]['header']['default'])
#        for par_name in LOCAL_TABLE_CACHE[TableName]['header']['order']:
#            LOCAL_TABLE_CACHE[TableName]['data'][par_name] = []
#    if "extra" in LOCAL_TABLE_CACHE[TableName]['header'].keys():
#        glob_order += LOCAL_TABLE_CACHE[TableName]['header']['extra']
#        glob_format.update(LOCAL_TABLE_CACHE[TableName]['header']['extra_format'])
#        for par_name in LOCAL_TABLE_CACHE[TableName]['header']['extra']:
#            glob_default[par_name] = PARAMETER_META[par_name]['default_fmt']
#            LOCAL_TABLE_CACHE[TableName]['data'][par_name] = []
#    line_count = 0
#    for line in InfileData:
#        try:
#            RowObject = getRowObjectFromString(line,TableName)
#            line_count += 1
#        except:
#            continue
#        addRowObject(RowObject,TableName)
#    LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows'] = line_count
#    # Delete all character-separated values, treat them as column-fixed.
#    try:
#        del LOCAL_TABLE_CACHE[TableName]['header']['extra']
#        del LOCAL_TABLE_CACHE[TableName]['header']['extra_format']
#        del LOCAL_TABLE_CACHE[TableName]['header']['extra_separator']
#    except:
#        pass
#    # Update header.order/format with header.extra/format if exist.
#    LOCAL_TABLE_CACHE[TableName]['header']['order'] = glob_order
#    LOCAL_TABLE_CACHE[TableName]['header']['format'] = glob_format
#    LOCAL_TABLE_CACHE[TableName]['header']['default'] = glob_default
#    InfileData.close()
#    InfileHeader.close()
#    print('                     Lines parsed: %d' % line_count)
#    pass

# / FORMAT CONVERSION LAYER    
    
def getTableNamesFromStorage(StorageName):
    file_names = listdir(StorageName)
    table_names = []
    for file_name in file_names:
        matchObject = re.search('(.+)\.header$',file_name)
        if matchObject:
           table_names.append(matchObject.group(1))
    return table_names

# FIX POSSIBLE BUG: SIMILAR NAMES OF .PAR AND .DATA FILES
# BUG FIXED BY INTRODUCING A PRIORITY:
#   *.data files have more priority than *.par files
#   See getFullTableAndHeaderName function for explanation
def scanForNewParfiles(StorageName):
    file_names = listdir(StorageName)
    headers = {} # without extensions!
    parfiles_without_header = []
    for file_name in file_names:
        # create dictionary of unique headers
        try:
            fname,fext = re.search('(.+)\.(\w+)',file_name).groups()
        except:
            continue
        if fext == 'header': headers[fname] = True
    for file_name in file_names:
        # check if extension is 'par' and the header is absent
        try:
            fname,fext = re.search('(.+)\.(\w+)',file_name).groups()
        except:
            continue
        if fext == 'par' and fname not in headers:
            parfiles_without_header.append(fname)
    return parfiles_without_header

def createHeader(TableName):
    fname = TableName+'.header'
    fp = open(VARIABLES['BACKEND_DATABASE_NAME']+'/'+fname,'w')
    if os.path.isfile(TableName):
        raise Exception('File \"%s\" already exists!' % fname)
    fp.write(json.dumps(HITRAN_DEFAULT_HEADER,indent=2))
    fp.close()

def loadCache():
    print('Using '+VARIABLES['BACKEND_DATABASE_NAME']+'\n')
    LOCAL_TABLE_CACHE = {}
    table_names = getTableNamesFromStorage(VARIABLES['BACKEND_DATABASE_NAME'])
    parfiles_without_header = scanForNewParfiles(VARIABLES['BACKEND_DATABASE_NAME'])
    # create headers for new parfiles
    for tab_name in parfiles_without_header:
        # get name without 'par' extension
        createHeader(tab_name)
        table_names.append(tab_name)
    for TableName in table_names:
        print(TableName)
        storage2cache(TableName)

def saveCache():
    try:
        # delete query buffer
        del LOCAL_TABLE_CACHE[QUERY_BUFFER]
    except:
        pass
    for TableName in LOCAL_TABLE_CACHE:
        print(TableName)
        cache2storage(TableName)

# DB backend level, start transaction
def databaseBegin(db=None):
    if db:
       VARIABLES['BACKEND_DATABASE_NAME'] = db
    else:
       VARIABLES['BACKEND_DATABASE_NAME'] = BACKEND_DATABASE_NAME_DEFAULT
    if not os.path.exists(VARIABLES['BACKEND_DATABASE_NAME']):
       os.mkdir(VARIABLES['BACKEND_DATABASE_NAME'])
    loadCache()

# DB backend level, end transaction
def databaseCommit():
    saveCache()

# ----------------------------------------------------
# ----------------------------------------------------
# CONDITIONS
# ----------------------------------------------------
# ----------------------------------------------------
# ----------------------------------------------------
# hierarchic query.condition language:
# Conditions: CONS = ('and', ('=','p1','p2'), ('<','p1',13))
# String literals are distinguished from variable names 
#  by using the operation ('STRING','some_string')
# ----------------------------------------------------

# necessary conditions for hitranonline:
SAMPLE_CONDITIONS = ('AND',('SET','internal_iso_id',[1,2,3,4,5,6]),('>=','nu',0),('<=','nu',100))

# sample hitranonline protocol
# http://hitran.cloudapp.net/lbl/5?output_format_id=1&iso_ids_list=5&numin=0&numax=100&access=api&key=e20e4bd3-e12c-4931-99e0-4c06e88536bd

CONDITION_OPERATIONS = set(['AND','OR','NOT','RANGE','IN','<','>','<=','>=','==','!=','LIKE','STR','+','-','*','/','MATCH','SEARCH','FINDALL'])

# Operations used in Condition verification
# Basic scheme: operationXXX(args),
# where args - list/array of arguments (>=1)

def operationAND(args):
    # any number if arguments
    for arg in args:
        if not arg:
           return False
    return True

def operationOR(args):
    # any number of arguments
    for arg in args:
        if arg:
           return True
    return False

def operationNOT(arg):
    # one argument
    return not arg

def operationRANGE(x,x_min,x_max):
    return x_min <= x <= x_max
    
def operationSUBSET(arg1,arg2):
    # True if arg1 is subset of arg2
    # arg1 is an element
    # arg2 is a set
    return arg1 in arg2

def operationLESS(args):
    # any number of args
    for i in range(1,len(args)):
        if args[i-1] >= args[i]:
           return False
    return True

def operationMORE(args):
    # any number of args
    for i in range(1,len(args)):
        if args[i-1] <= args[i]:
           return False
    return True

def operationLESSOREQUAL(args):
    # any number of args
    for i in range(1,len(args)):
        if args[i-1] > args[i]:
           return False
    return True

def operationMOREOREQUAL(args):
    # any number of args
    for i in range(1,len(args)):
        if args[i-1] < args[i]:
           return False
    return True

def operationEQUAL(args):
    # any number of args
    for i in range(1,len(args)):
        if args[i] != args[i-1]:
           return False
    return True

def operationNOTEQUAL(arg1,arg2):
    return arg1 != arg2
    
def operationSUM(args):
    # any numbers of arguments
    if type(args[0]) in set([int,float]):
       result = 0
    elif type(args[0]) in set([str,unicode]):
       result = ''
    else:
       raise Exception('SUM error: unknown arg type')
    for arg in args:
        result += arg
    return result

def operationDIFF(arg1,arg2):
    return arg1-arg2

def operationMUL(args):
    # any numbers of arguments
    if type(args[0]) in set([int,float]):
       result = 1
    else:
       raise Exception('MUL error: unknown arg type')
    for arg in args:
        result *= arg
    return result

def operationDIV(arg1,arg2):
    return arg1/arg2

def operationSTR(arg):
    # transform arg to str
    if type(arg)!=str:
       raise Exception('Type mismatch: STR')
    return arg

def operationSET(arg):
    # transform arg to list
    if type(arg) not in set([list,tuple,set]):
        raise Exception('Type mismatch: SET')
    return list(arg)

def operationMATCH(arg1,arg2):
    # Match regex (arg1) and string (arg2)
    #return bool(re.match(arg1,arg2)) # works wrong
    return bool(re.search(arg1,arg2))

def operationSEARCH(arg1,arg2):
    # Search regex (arg1) in string (arg2)
    # Output list of entries
    group = re.search(arg1,arg2).groups()
    result = []
    for item in group:
        result.append(('STR',item))
    return result

def operationFINDALL(arg1,arg2):
    # Search all groups of a regex
    # Output a list of groups of entries
    # XXX: If a group has more than 1 entry,
    #    there could be potential problems
    list_of_groups = re.findall(arg1,arg2)
    result = []
    for item in list_of_groups:
        result.append(('STR',item))
    return result

def operationLIST(args):
    # args is a list: do nothing (almost)
    return list(args)

# /operations

# GROUPING ---------------------------------------------- 

GROUP_INDEX = {}
# GROUP_INDEX has the following structure:
#  GROUP_INDEX[KEY] = VALUE
#    KEY = table line values
#    VALUE = {'FUNCTIONS':DICT,'FLAG':LOGICAL,'ROWID':INTEGER}
#      FUNCTIONS = {'FUNC_NAME':DICT}
#            FUNC_NAME = {'FLAG':LOGICAL,'NAME':STRING}

# name and default value
GROUP_FUNCTION_NAMES = { 'COUNT' :  0,
                         'SUM'   :  0,
                         'MUL'   :  1,
                         'AVG'   :  0,
                         'MIN'   : +1e100,
                         'MAX'   : -1e100,
                         'SSQ'   : 0,
                       }

def clearGroupIndex():
    #GROUP_INDEX = {}
    for key in GROUP_INDEX.keys():
        del GROUP_INDEX[key]

def getValueFromGroupIndex(GroupIndexKey,FunctionName):
    # If no such index_key, create it and return a value
    if FunctionName not in GROUP_FUNCTION_NAMES:
       raise Exception('No such function \"%s\"' % FunctionName)
    # In the case if NewRowObjectDefault is requested
    if not GroupIndexKey:
       return GROUP_FUNCTION_NAMES[FunctionName]
    if FunctionName not in GROUP_INDEX[GroupIndexKey]['FUNCTIONS']:
       GROUP_INDEX[GroupIndexKey]['FUNCTIONS'][FunctionName] = {}
       GROUP_INDEX[GroupIndexKey]['FUNCTIONS'][FunctionName]['FLAG'] = True
       GROUP_INDEX[GroupIndexKey]['FUNCTIONS'][FunctionName]['VALUE'] = \
         GROUP_FUNCTION_NAMES[FunctionName]
    return GROUP_INDEX[GroupIndexKey]['FUNCTIONS'][FunctionName]['VALUE']

def setValueToGroupIndex(GroupIndexKey,FunctionName,Value):
    GROUP_INDEX[GroupIndexKey]['FUNCTIONS'][FunctionName]['VALUE'] = Value

GROUP_DESC = {}
def initializeGroup(GroupIndexKey):
    if GroupIndexKey not in GROUP_INDEX:
        print('GROUP_DESC[COUNT]='+str(GROUP_DESC['COUNT']))
        GROUP_INDEX[GroupIndexKey] = {}
        GROUP_INDEX[GroupIndexKey]['FUNCTIONS'] = {}
        GROUP_INDEX[GroupIndexKey]['ROWID'] = len(GROUP_INDEX) - 1
    for FunctionName in GROUP_FUNCTION_NAMES:
        # initialize function flags (UpdateFlag)
        if FunctionName in GROUP_INDEX[GroupIndexKey]['FUNCTIONS']:
           GROUP_INDEX[GroupIndexKey]['FUNCTIONS'][FunctionName]['FLAG'] = True
    print('initializeGroup: GROUP_INDEX='+str(GROUP_INDEX))

def groupCOUNT(GroupIndexKey):
    FunctionName = 'COUNT'
    Value = getValueFromGroupIndex(GroupIndexKey,FunctionName)
    if GroupIndexKey:
       if GROUP_INDEX[GroupIndexKey]['FUNCTIONS'][FunctionName]['FLAG']:
          GROUP_INDEX[GroupIndexKey]['FUNCTIONS'][FunctionName]['FLAG'] = False
          Value = Value + 1
          setValueToGroupIndex(GroupIndexKey,FunctionName,Value)
    return Value

def groupSUM():
    pass

def groupMUL():
    pass

def groupAVG():
    pass

def groupMIN():
    pass

def groupMAX():
    pass

def groupSSQ():
    pass

OPERATORS = {\
# List
'LIST' : lambda args : operationLIST(args),
# And
'&' : lambda args : operationAND(args),
'&&' : lambda args : operationAND(args),
'AND' : lambda args : operationAND(args),
# Or
'|' : lambda args : operationOR(args),
'||' : lambda args : operationOR(args),
'OR' : lambda args : operationOR(args),
# Not
'!' : lambda args : operationNOT(args[0]),
'NOT' : lambda args : operationNOT(args[0]),
# Between
'RANGE' : lambda args : operationRANGE(args[0],args[1],args[2]),
'BETWEEN' : lambda args : operationRANGE(args[0],args[1],args[2]),
# Subset
'IN' : lambda args : operationSUBSET(args[0],args[1]),
'SUBSET': lambda args : operationSUBSET(args[0],args[1]),
# Less
'<' : lambda args : operationLESS(args),
'LESS' : lambda args : operationLESS(args),
'LT'  : lambda args : operationLESS(args),
# More
'>' : lambda args : operationMORE(args),
'MORE' : lambda args : operationMORE(args),
'MT'   : lambda args : operationMORE(args),
# Less or equal
'<=' : lambda args : operationLESSOREQUAL(args),
'LESSOREQUAL' : lambda args : operationLESSOREQUAL(args),
'LTE' : lambda args : operationLESSOREQUAL(args),
# More or equal
'>=' : lambda args : operationMOREOREQUAL(args),
'MOREOREQUAL' : lambda args : operationMOREOREQUAL(args),
'MTE' : lambda args : operationMOREOREQUAL(args),
# Equal
'=' : lambda args : operationEQUAL(args),
'==' : lambda args : operationEQUAL(args),
'EQ' : lambda args : operationEQUAL(args),
'EQUAL' : lambda args : operationEQUAL(args),
'EQUALS' : lambda args : operationEQUAL(args),
# Not equal
'!=' : lambda args : operationNOTEQUAL(args[0],args[1]),
'<>' : lambda args : operationNOTEQUAL(args[0],args[1]),
'~=' : lambda args : operationNOTEQUAL(args[0],args[1]),
'NE' : lambda args : operationNOTEQUAL(args[0],args[1]),
'NOTEQUAL' : lambda args : operationNOTEQUAL(args[0],args[1]),
# Plus
'+' : lambda args : operationSUM(args),
'SUM' : lambda args : operationSUM(args),
# Minus
'-' : lambda args : operationDIFF(args[0],args[1]),
'DIFF' : lambda args : operationDIFF(args[0],args[1]),
# Mul
'*' : lambda args : operationMUL(args),
'MUL' : lambda args : operationMUL(args),
# Div
'/' : lambda args : operationDIV(args[0],args[1]),
'DIV' : lambda args : operationDIV(args[0],args[1]),
# Regexp match
'MATCH' : lambda args : operationMATCH(args[0],args[1]),
'LIKE' : lambda args : operationMATCH(args[0],args[1]),
# Regexp search
'SEARCH' : lambda args : operationSEARCH(args[0],args[1]),
# Regexp findal
'FINDALL' : lambda args : operationFINDALL(args[0],args[1]),
# Group count
'COUNT' : lambda args : groupCOUNT(args[0]),
}
    
# new evaluateExpression function,
#  accounting for groups
"""
def evaluateExpression(root,VarDictionary,GroupIndexKey=None):
    # input = local tree root
    # XXX: this could be very slow due to passing
    #      every time VarDictionary as a parameter
    # Two special cases: 1) root=varname
    #                    2) root=list/tuple
    # These cases must be processed in a separate way
    if type(root) in set([list,tuple]):
       # root is not a leaf
       head = root[0].upper()
       # string constants are treated specially
       if head in set(['STR','STRING']): # one arg
          return operationSTR(root[1])
       elif head in set(['SET']):
          return operationSET(root[1])
       tail = root[1:]
       args = []
       # evaluate arguments recursively
       for element in tail: # resolve tree by recursion
           args.append(evaluateExpression(element,VarDictionary,GroupIndexKey))
       # call functions with evaluated arguments
       if head in set(['LIST']): # list arg
          return operationLIST(args)
       elif head in set(['&','&&','AND']): # many args 
          return operationAND(args)
       elif head in set(['|','||','OR']): # many args
          return operationOR(args)
       elif head in set(['!','NOT']): # one args
          return operationNOT(args[0])
       elif head in set(['RANGE','BETWEEN']): # three args
          return operationRANGE(args[0],args[1],args[2])
       elif head in set(['IN','SUBSET']): # two args
          return operationSUBSET(args[0],args[1])
       elif head in set(['<','LESS','LT']): # many args
          return operationLESS(args)
       elif head in set(['>','MORE','MT']): # many args
          return operationMORE(args)
       elif head in set(['<=','LESSOREQUAL','LTE']): # many args
          return operationLESSOREQUAL(args)
       elif head in set(['>=','MOREOREQUAL','MTE']): # many args
          return operationMOREOREQUAL(args)
       elif head in set(['=','==','EQ','EQUAL','EQUALS']): # many args
          return operationEQUAL(args)
       elif head in set(['!=','<>','~=','NE','NOTEQUAL']): # two args
          return operationNOTEQUAL(args[0],args[1])
       elif head in set(['+','SUM']): # many args
          return operationSUM(args)
       elif head in set(['-','DIFF']): # two args
          return operationDIFF(args[0],args[1])
       elif head in set(['*','MUL']): # many args
          return operationMUL(args)
       elif head in set(['/','DIV']): # two args
          return operationDIV(args[0],args[1])
       elif head in set(['MATCH','LIKE']): # two args
          return operationMATCH(args[0],args[1])
       elif head in set(['SEARCH']): # two args
          return operationSEARCH(args[0],args[1])
       elif head in set(['FINDALL']): # two args
          return operationFINDALL(args[0],args[1])
       # --- GROUPING OPERATIONS ---
       elif head in set(['COUNT']):
          return groupCOUNT(GroupIndexKey)
       else:
          raise Exception('Unknown operator: %s' % root[0])
    elif type(root)==str:
       # root is a par_name
       return VarDictionary[root]
    else: 
       # root is a non-string constant
       return root
"""

def evaluateExpression(root,VarDictionary,GroupIndexKey=None):
    # input = local tree root
    # XXX: this could be very slow due to passing
    #      every time VarDictionary as a parameter
    # Two special cases: 1) root=varname
    #                    2) root=list/tuple
    # These cases must be processed in a separate way
    if type(root) in set([list,tuple]):
        # root is not a leaf
        head = root[0].upper()
        # string constants are treated specially
        if head in set(['STR','STRING']): # one arg
            return operationSTR(root[1])
        elif head in set(['SET']):
            return operationSET(root[1])
        tail = root[1:]
        args = []
        # evaluate arguments recursively
        for element in tail: # resolve tree by recursion
            args.append(evaluateExpression(element,VarDictionary,GroupIndexKey))
        # call functions with evaluated arguments
        try:
            return OPERATORS[head](args)
        except KeyError:
            raise Exception('Unknown operator: %s' % head)
    elif type(root)==str:
       # root is a par_name
       return VarDictionary[root]
    else: 
       # root is a non-string constant
       return root

def getVarDictionary(RowObject):
    # get VarDict from RowObject
    # VarDict: par_name => par_value
    VarDictionary = {}
    for par_name,par_value,par_format in RowObject:
        VarDictionary[par_name] = par_value
    return VarDictionary

def checkRowObject(RowObject,Conditions,VarDictionary):
    #VarDictionary = getVarDictionary(RowObject)   
    if Conditions:
       Flag = evaluateExpression(Conditions,VarDictionary)
    else:
       Flag=True
    return Flag

# ----------------------------------------------------
# /CONDITIONS
# ----------------------------------------------------


# ----------------------------------------------------
# PARAMETER NAMES (includeing creation of new ones)
# ----------------------------------------------------

# Bind an expression to a new parameter
#   in a form: ('BIND','new_par',('some_exp',...))
def operationBIND(parname,Expression,VarDictionary):
    pass

# This section is for more detailed processing of parlists. 

# Table creation must include not only subsets of 
#   existing parameters, but also new parameters
#   derived from functions on a special prefix language
# For this reason subsetOfRowObject(..) must be substituted
#   by newRowObject(ParameterNames,RowObject)

# For parsing use the function evaluateExpression

# Get names from expression.
#  Must merge this one with evaluateExrpression.
# This is VERY LIMITED version of what will be 
#  when make the language parser is implemented.
# For more ideas and info see LANGUAGE_REFERENCE

# more advansed version of expression evaluator
def evaluateExpressionPAR(ParameterNames,VarDictionary=None):
    # RETURN: 1) Upper-level Expression names
    #         2) Upper-level Expression values
    # Is it reasonable to pass a Context to every parse function?
    # For now the function does the following:
    #   1) iterates through all UPPER-LEVEL list elements
    #   2) if element is a par name: return par name
    #      if element is an BIND expression: return bind name
    #              (see operationBIND)
    #   3) if element is an anonymous expression: return #N(=1,2,3...)
    # N.B. Binds can be only on the 0-th level of Expression    
    pass

def getContextFormat(RowObject):
    # Get context format from the whole RowObject
    ContextFormat = {}
    for par_name,par_value,par_format in RowObject:
        ContextFormat[par_name] = par_format
    return ContextFormat

def getDefaultFormat(Type):
    if Type is int:
       return '%10d'
    elif Type is float:
       return '%25.15E'
    elif Type is str:
       return '%20s'
    elif Type is bool:
       return '%2d'
    else:
       raise Exception('Unknown type')
     
def getDefaultValue(Type):
    if Type is int:
       return 0
    elif Type is float:
       return 0.0
    elif Type is str:
       return ''
    elif Type is bool:
       return False
    else:
       raise Exception('Unknown type')

# VarDictionary = Context (this name is more suitable)

# GroupIndexKey is a key to special structure/dictionary GROUP_INDEX.
# GROUP_INDEX contains information needed to calculate streamed group functions
#  such as COUNT, AVG, MIN, MAX etc...

def newRowObject(ParameterNames,RowObject,VarDictionary,ContextFormat,GroupIndexKey=None):
    # Return a subset of RowObject according to 
    # ParameterNames include either par names
    #  or expressions containing par names literals
    # ContextFormat contains format for ParNames
    anoncount = 0
    RowObjectNew = []
    for expr in ParameterNames:
        if type(expr) in set([list,tuple]): # bind
           head = expr[0]
           if head in set(['let','bind','LET','BIND']):
              par_name = expr[1]
              par_expr = expr[2]
           else:
              par_name = "#%d" % anoncount
              anoncount += 1
              par_expr = expr
           par_value = evaluateExpression(par_expr,VarDictionary,GroupIndexKey)
           try:
              par_format = expr[3]
           except:
              par_format = getDefaultFormat(type(par_value))
        else: # parname
           par_name = expr
           par_value = VarDictionary[par_name]
           par_format = ContextFormat[par_name]
        RowObjectNew.append((par_name,par_value,par_format))
    return RowObjectNew

# ----------------------------------------------------
# /PARAMETER NAMES
# ----------------------------------------------------


# ----------------------------------------------------
# OPERATIONS ON TABLES
# ----------------------------------------------------

QUERY_BUFFER = '__BUFFER__'

def getTableList():
    return LOCAL_TABLE_CACHE.keys()

def describeTable(TableName):
    """
    INPUT PARAMETERS: 
        TableName: name of the table to describe
    OUTPUT PARAMETERS: 
        none
    ---
    DESCRIPTION:
        Print information about table, including 
        parameter names, formats and wavenumber range.
    ---
    EXAMPLE OF USAGE:
        describeTable('sampletab')
    ---
    """
    print('-----------------------------------------')
    print(TableName+' summary:')
    try:
       print('-----------------------------------------')
       print('Comment: \n'+LOCAL_TABLE_CACHE[TableName]['header']['comment'])
    except:
       pass
    print('Number of rows: '+str(LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']))
    print('Table type: '+str(LOCAL_TABLE_CACHE[TableName]['header']['table_type']))
    print('-----------------------------------------')
    print('            PAR_NAME           PAR_FORMAT')
    print('')
    for par_name in LOCAL_TABLE_CACHE[TableName]['header']['order']:
        par_format = LOCAL_TABLE_CACHE[TableName]['header']['format'][par_name]
        print('%20s %20s' % (par_name,par_format))
    print('-----------------------------------------')

# Write a table to File or STDOUT
def outputTable(TableName,Conditions=None,File=None,Header=True):
    # Display or record table with condition checking
    if File:
       Header = False
       OutputFile = open(File,'w')
    if Header:
       headstr = putTableHeaderToString(TableName)
       if File:
          OutputFile.write(headstr)
       else:
          print(headstr)
    for RowID in range(0,LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']):
        RowObject = getRowObject(RowID,TableName)
        VarDictionary = getVarDictionary(RowObject)
        VarDictionary['LineNumber'] = RowID
        if not checkRowObject(RowObject,Conditions,VarDictionary):
           continue
        raw_string = putRowObjectToString(RowObject)
        if File:
           OutputFile.write(raw_string+'\n')
        else:
           print(raw_string)

# Create table "prototype-based" way
def createTable(TableName,RowObjectDefault):
    # create a Table based on a RowObjectDefault
    LOCAL_TABLE_CACHE[TableName] = {}
    header_order = []
    header_format = {}
    header_default = {}
    data = {}
    for par_name,par_value,par_format in RowObjectDefault:
        header_order.append(par_name)
        header_format[par_name] = par_format
        header_default[par_name] = par_value
        data[par_name] = []
    #header_order = tuple(header_order) # XXX ?
    LOCAL_TABLE_CACHE[TableName]['header']={}
    LOCAL_TABLE_CACHE[TableName]['header']['order'] = header_order 
    LOCAL_TABLE_CACHE[TableName]['header']['format'] = header_format
    LOCAL_TABLE_CACHE[TableName]['header']['default'] = header_default
    LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows'] = 0
    LOCAL_TABLE_CACHE[TableName]['header']['size_in_bytes'] = 0
    LOCAL_TABLE_CACHE[TableName]['header']['table_name'] = TableName
    LOCAL_TABLE_CACHE[TableName]['header']['table_type'] = 'column-fixed'
    LOCAL_TABLE_CACHE[TableName]['data'] = data
    

# simple "drop table" capability
def dropTable(TableName):
    """
    INPUT PARAMETERS: 
        TableName:  name of the table to delete
    OUTPUT PARAMETERS: 
        none
    ---
    DESCRIPTION:
        Deletes a table from local database.
    ---
    EXAMPLE OF USAGE:
        dropTable('some_dummy_table')
    ---
    """
    # delete Table from both Cache and Storage
    try:
       #LOCAL_TABLE_CACHE[TableName] = {}
       del LOCAL_TABLE_CACHE[TableName]
    except:
       pass
    # delete from storage
    pass # TODO

# Returns a column corresponding to parameter name
def getColumn(TableName,ParameterName):
    """
    INPUT PARAMETERS: 
        TableName:      source table name     (required)
        ParameterName:  name of column to get (required)
    OUTPUT PARAMETERS: 
        ColumnData:     list of values from specified column 
    ---
    DESCRIPTION:
        Returns a column with a name ParameterName from
        table TableName. Column is returned as a list of values.
    ---
    EXAMPLE OF USAGE:
        p1 = getColumn('sampletab','p1')
    ---
    """
    return LOCAL_TABLE_CACHE[TableName]['data'][ParameterName]

# Returns a list of columns corresponding to parameter names
def getColumns(TableName,ParameterNames):
    """
    INPUT PARAMETERS: 
        TableName:       source table name           (required)
        ParameterNames:  list of column names to get (required)
    OUTPUT PARAMETERS: 
        ListColumnData:   tuple of lists of values from specified column 
    ---
    DESCRIPTION:
        Returns columns with a names in ParameterNames from
        table TableName. Columns are returned as a tuple of lists.
    ---
    EXAMPLE OF USAGE:
        p1,p2,p3 = getColumns('sampletab',('p1','p2','p3'))
    ---
    """
    Columns = []
    for par_name in ParameterNames:
        Columns.append(LOCAL_TABLE_CACHE[TableName]['data'][par_name])
    return Columns

def addColumn(TableName,ParameterName,Before=None,Expression=None,Type=None,Default=None,Format=None):
    if ParameterName in LOCAL_TABLE_CACHE[TableName]['header']['format']:
       raise Exception('Column \"%s\" already exists' % ParameterName)
    if not Type: Type = float
    if not Default: Default = getDefaultValue(Type)
    if not Format: Format = getDefaultFormat(Type)
    number_of_rows = LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']
    # Mess with data
    if not Expression:
       LOCAL_TABLE_CACHE[TableName]['data'][ParameterName]=[Default for i in range(0,number_of_rows)]
    else:
       data = []
       for RowID in range(0,number_of_rows):
           RowObject = getRowObject(RowID,TableName)
           VarDictionary = getVarDictionary(RowObject)
           VarDictionary['LineNumber'] = RowID
           par_value = evaluateExpression(Expression,VarDictionary)
           data.append(par_value)
           LOCAL_TABLE_CACHE[TableName]['data'][ParameterName] = data
    # Mess with header
    header_order = LOCAL_TABLE_CACHE[TableName]['header']['order']
    if not Before: 
       header_order.append(ParameterName)
    else:
       #i = 0
       #for par_name in header_order:
       #    if par_name == Before: break
       #    i += 1
       i = header_order.index(Before)
       header_order = header_order[:i] + [ParameterName,] + header_order[i:]
    LOCAL_TABLE_CACHE[TableName]['header']['order'] = header_order
    LOCAL_TABLE_CACHE[TableName]['header']['format'][ParameterName] = Format
    LOCAL_TABLE_CACHE[TableName]['header']['default'][ParameterName] = Default
   

def deleteColumn(TableName,ParameterName):
    if ParameterName not in LOCAL_TABLE_CACHE[TableName]['header']['format']:
       raise Exception('No such column \"%s\"' % ParameterName)
    # Mess with data
    i = LOCAL_TABLE_CACHE[TableName]['header']['order'].index(ParameterName)
    del LOCAL_TABLE_CACHE[TableName]['header']['order'][i]
    del LOCAL_TABLE_CACHE[TableName]['header']['format'][ParameterName]
    del LOCAL_TABLE_CACHE[TableName]['header']['default'][ParameterName]
    if not LOCAL_TABLE_CACHE[TableName]['header']['order']:
       LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows'] = 0
    # Mess with header
    del LOCAL_TABLE_CACHE[TableName]['data'][ParameterName]

def deleteColumns(TableName,ParameterNames):
    if type(ParameterNames) not in set([list,tuple,set]):
       ParameterNames = [ParameterNames]
    for ParameterName in ParameterNames:
        deleteColumn(TableName,ParameterName)

def renameColumn(TableName,OldParameterName,NewParameterName):
    pass

def insertRow():
    pass

def deleteRows(TableName,ParameterNames,Conditions):
    pass

# select from table to another table
def selectInto(DestinationTableName,TableName,ParameterNames,Conditions):
    # TableName must refer to an existing table in cache!!
    # Conditions = Restrictables in specific format
    # Sample conditions: cond = {'par1':{'range',[b_lo,b_hi]},'par2':b}
    # return structure similar to TableObject and put it to QUERY_BUFFER
    # if ParameterNames is '*' then all parameters are used
    #table_columns = LOCAL_TABLE_CACHE[TableName]['data'].keys()
    #table_length = len(TableObject['header']['number_of_rows'])
    #if ParameterNames=='*':
    #   ParameterNames = table_columns
    # check if Conditions contain elements which are not in the TableObject
    #condition_variables = getConditionVariables(Conditions)
    #strange_pars = set(condition_variables)-set(table_variables)
    #if strange_pars: 
    #   raise Exception('The following parameters are not in the table \"%s\"' % (TableName,list(strange_pars)))
    # do full scan each time
    if DestinationTableName == TableName:
       raise Exception('Selecting into source table is forbidden')
    table_length = LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']
    row_count = 0
    for RowID in range(0,table_length):
        RowObject = getRowObject(RowID,TableName)
        VarDictionary = getVarDictionary(RowObject)
        VarDictionary['LineNumber'] = RowID
        ContextFormat = getContextFormat(RowObject)
        RowObjectNew = newRowObject(ParameterNames,RowObject,VarDictionary,ContextFormat)
        if checkRowObject(RowObject,Conditions,VarDictionary):
           addRowObject(RowObjectNew,DestinationTableName)
           row_count += 1
    LOCAL_TABLE_CACHE[DestinationTableName]['header']['number_of_rows'] += row_count

def length(TableName):
    tab_len = LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']
    #print(str(tab_len)+' rows in '+TableName)
    return tab_len

# Select parameters from a table with certain conditions.
# Parameters can be the names or expressions.
# Conditions contain a list of expressions in a special language.
# Set Output to False to suppress output
# Set File=FileName to redirect output to a file.
def select(TableName,DestinationTableName=QUERY_BUFFER,ParameterNames=None,Conditions=None,Output=True,File=None):
    """
    INPUT PARAMETERS: 
        TableName:            name of source table              (required)
        DestinationTableName: name of resulting table           (optional)
        ParameterNames:       list of parameters or expressions (optional)
        Conditions:           list of logincal expressions      (optional)
        Output:   enable (True) or suppress (False) text output (optional)
        File:     enable (True) or suppress (False) file output (optional)
    OUTPUT PARAMETERS: 
        none
    ---
    DESCRIPTION:
        Select or filter the data in some table 
        either to standard output or to file (if specified)
    ---
    EXAMPLE OF USAGE:
        select('sampletab',DestinationTableName='outtab',ParameterNames=(p1,p2),
                Conditions=(('and',('>=','p1',1),('<',('*','p1','p2'),20))))
        Conditions means (p1>=1 and p1*p2<20)
    ---
    """
    # TODO: Variables defined in ParameterNames ('LET') MUST BE VISIBLE IN Conditions !!
    # check if table exists
    if TableName not in LOCAL_TABLE_CACHE.keys():
        raise Exception('%s: no such table. Check tableList() for more info.' % TableName)
    if not ParameterNames: ParameterNames=LOCAL_TABLE_CACHE[TableName]['header']['order']
    LOCAL_TABLE_CACHE[DestinationTableName] = {} # clear QUERY_BUFFER for the new result
    RowObjectDefault = getDefaultRowObject(TableName)
    VarDictionary = getVarDictionary(RowObjectDefault)
    ContextFormat = getContextFormat(RowObjectDefault)
    RowObjectDefaultNew = newRowObject(ParameterNames,RowObjectDefault,VarDictionary,ContextFormat)
    dropTable(DestinationTableName) # redundant
    createTable(DestinationTableName,RowObjectDefaultNew)
    selectInto(DestinationTableName,TableName,ParameterNames,Conditions)
    if DestinationTableName!=QUERY_BUFFER:
        if File: outputTable(DestinationTableName,File=File)
    elif Output:
        outputTable(DestinationTableName,File=File)

# SORTING ===========================================================

def arrangeTable(TableName,DestinationTableName=None,RowIDList=None):
    #print 'AT/'
    #print 'AT: RowIDList = '+str(RowIDList)
    # make a subset of table rows according to RowIDList
    if not DestinationTableName:
       DestinationTableName = TableName
    if DestinationTableName != TableName:
       dropTable(DestinationTableName)
       LOCAL_TABLE_CACHE[DestinationTableName]['header']=LOCAL_TABLE_CACHE[TableName]['header']
       LOCAL_TABLE_CACHE[DestinationTableName]['data']={}
    LOCAL_TABLE_CACHE[DestinationTableName]['header']['number_of_rows'] = len(RowIDList)
    #print 'AT: RowIDList = '+str(RowIDList)
    for par_name in LOCAL_TABLE_CACHE[DestinationTableName]['header']['order']:
        par_data = LOCAL_TABLE_CACHE[TableName]['data'][par_name]
        LOCAL_TABLE_CACHE[DestinationTableName]['data'][par_name] = [par_data[i] for i in RowIDList]
    
def compareLESS(RowObject1,RowObject2,ParameterNames):
    #print 'CL/'
    # arg1 and arg2 are RowObjects
    # Compare them according to ParameterNames
    # Simple validity check:
    #if len(arg1) != len(arg2):
    #   raise Exception('Arguments have different lengths')
    #RowObject1Subset = subsetOfRowObject(ParameterNames,RowObject1)
    #RowObject2Subset = subsetOfRowObject(ParameterNames,RowObject2)
    #return RowObject1Subset < RowObject2Subset
    row1 = []
    row2 = []
    #n = len(RowObject1)
    #for i in range(0,n):
    #    par_name1 = RowObject1[i][0]
    #    if par_name1 in ParameterNames:
    #       par_value1 = RowObject1[i][1]
    #       par_value2 = RowObject2[i][1]
    #       row1 += [par_value1]
    #       row2 += [par_value2]
    VarDictionary1 = getVarDictionary(RowObject1)
    VarDictionary2 = getVarDictionary(RowObject2)
    for par_name in ParameterNames:
        par_value1 = VarDictionary1[par_name]
        par_value2 = VarDictionary2[par_name]
        row1 += [par_value1]
        row2 += [par_value2]
    Flag = row1 < row2
    return Flag

def quickSort(index,TableName,ParameterNames,Accending=True):
    # ParameterNames: names of parameters which are
    #  taking part in the sorting
    if index == []:
       return []
    else:
       PivotID = index[0]
       Pivot = getRowObject(PivotID,TableName)
       lesser_index = []
       greater_index = [];
       for RowID in index[1:]:
           RowObject = getRowObject(RowID,TableName)           
           if compareLESS(RowObject,Pivot,ParameterNames): 
              lesser_index += [RowID]
           else:
              greater_index += [RowID]
       lesser = quickSort(lesser_index,TableName,ParameterNames,Accending)
       greater = quickSort(greater_index,TableName,ParameterNames,Accending)
       if Accending:
          return lesser + [PivotID] + greater
       else:
          return greater + [PivotID] + lesser

# Sorting must work well on the table itself!
def sort(TableName,DestinationTableName=None,ParameterNames=None,Accending=True,Output=False,File=None):
    """
    INPUT PARAMETERS: 
        TableName:                name of source table          (required)
        DestinationTableName:     name of resulting table       (optional)
        ParameterNames:       list of parameters or expressions to sort by    (optional)
        Accending:       sort in ascending (True) or descending (False) order (optional)
        Output:   enable (True) or suppress (False) text output (optional)
        File:     enable (True) or suppress (False) file output (optional)
    OUTPUT PARAMETERS: 
        none
    ---
    DESCRIPTION:
        Sort a table by a list of it's parameters or expressions.
        The sorted table is saved in DestinationTableName (if specified).
    ---
    EXAMPLE OF USAGE:
        sort('sampletab',ParameterNames=(p1,('+',p1,p2)))
    ---
    """
    number_of_rows = LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']
    index = range(0,number_of_rows)
    if not DestinationTableName:
       DestinationTableName = TableName
    # if names are not provided use all parameters in sorting
    if not ParameterNames:
       ParameterNames = LOCAL_TABLE_CACHE[TableName]['header']['order']
    elif type(ParameterNames) not in set([list,tuple]):
       ParameterNames = [ParameterNames] # fix of stupid bug where ('p1',) != ('p1')
    index_sorted = quickSort(index,TableName,ParameterNames,Accending)
    arrangeTable(TableName,DestinationTableName,index_sorted)
    if Output:
       outputTable(DestinationTableName,File=File)

# /SORTING ==========================================================
    

# GROUPING ==========================================================

# GROUP_INDEX global auxiliary structure is a Dictionary,
#   which has the following properties:
#      1) Each key is a composite variable:
#          [array of values of ParameterNames variable
#           STREAM_UPDATE_FLAG]
#      2) Each value is an index in LOCAL_TABLE_CACHE[TableName]['data'][...],
#          corresponding to this key
#   STREAM_UPDATE_FLAG = TRUE if value in GROUP_INDEX needs updating
#                      = FALSE otherwise
#   If no grouping variables are specified (GroupParameterNames==None)
#    than the following key is used: "__GLOBAL__"


def group(TableName,DestinationTableName=QUERY_BUFFER,ParameterNames=None,GroupParameterNames=None,File=None,Output=True):
    """
    INPUT PARAMETERS: 
        TableName:                name of source table          (required)
        DestinationTableName:     name of resulting table       (optional)
        ParameterNames:       list of parameters or expressions to take       (optional)
        GroupParameterNames:  list of parameters or expressions to group by   (optional)
        Accending:       sort in ascending (True) or descending (False) order (optional)
        Output:   enable (True) or suppress (False) text output (optional)
    OUTPUT PARAMETERS: 
        none
    ---
    DESCRIPTION:
        none
    ---
    EXAMPLE OF USAGE:
        group('sampletab',ParameterNames=('p1',('sum','p2')),GroupParameterNames=('p1'))
        ... makes grouping by p1,p2. For each group it calculates sum of p2 values.
    ---
    """
    # Implements such functions as:
    # count,sum,avg,min,max,ssq etc...
    # 1) ParameterNames can contain group functions
    # 2) GroupParameterNames can't contain group functions
    # 3) If ParameterNames contains parameters defined by LET directive,
    #    it IS visible in the sub-context of GroupParameterNames
    # 4) Parameters defined in GroupParameterNames are NOT visible in ParameterNames
    # 5) ParameterNames variable represents the structure of the resulting table/collection
    # 6) GroupParameterNames can contain either par_names or expressions with par_names
    # Clear old GROUP_INDEX value
    clearGroupIndex()
    # Consistency check
    if TableName == DestinationTableName:
       raise Exception('TableName and DestinationTableName must be different')
    #if not ParameterNames: ParameterNames=LOCAL_TABLE_CACHE[TableName]['header']['order']
    # Prepare the new DestinationTable
    RowObjectDefault = getDefaultRowObject(TableName)
    VarDictionary = getVarDictionary(RowObjectDefault)
    ContextFormat = getContextFormat(RowObjectDefault)
    RowObjectDefaultNew = newRowObject(ParameterNames,RowObjectDefault,VarDictionary,ContextFormat)
    dropTable(DestinationTableName) # redundant
    createTable(DestinationTableName,RowObjectDefaultNew)
    # Loop through rows of source Table
    # On each iteration group functions update GROUP_INDEX (see description above)
    number_of_rows = LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']   
    # STAGE 1: CREATE GROUPS
    print('LOOP:')
    for RowID in range(0,number_of_rows):
        print('--------------------------------')
        print('RowID='+str(RowID))
        RowObject = getRowObject(RowID,TableName) # RowObject from source table
        VarDictionary = getVarDictionary(RowObject)
        print('VarDictionary='+str(VarDictionary))
        # This is a trick which makes evaluateExpression function
        #   not consider first expression as an operation
        GroupParameterNames_ = ['LIST'] + list(GroupParameterNames)
        GroupIndexKey = evaluateExpression(GroupParameterNames_,VarDictionary)
        # List is an unhashable type in Python!
        GroupIndexKey = tuple(GroupIndexKey)       
        initializeGroup(GroupIndexKey)
        print('GROUP_INDEX='+str(GROUP_INDEX))
        ContextFormat = getContextFormat(RowObject)
        RowObjectNew = newRowObject(ParameterNames,RowObject,VarDictionary,ContextFormat,GroupIndexKey)
        RowIDGroup = GROUP_INDEX[GroupIndexKey]['ROWID']
        setRowObject(RowIDGroup,RowObjectNew,DestinationTableName)
    # Output result if required
    if Output and DestinationTableName==QUERY_BUFFER:
       outputTable(DestinationTableName,File=File)

# /GROUPING =========================================================

# EXTRACTING ========================================================

REGEX_INTEGER = '[+-]?\d+'
REGEX_STRING = '[^\s]+'
REGEX_FLOAT_F = '[+-]?\d*\.?\d+'
REGEX_FLOAT_E = '[+-]?\d*\.?\d+[eEfF]?[+-]?\d+' 

REGEX_INTEGER_FIXCOL = lambda n: '\d{%d}' % n
REGEX_STRING_FIXCOL = lambda n: '[^\s]{%d}' % n
REGEX_FLOAT_F_FIXCOL = lambda n: '[\+\-\.\d]{%d}' % n
REGEX_FLOAT_E_FIXCOL = lambda n: '[\+\-\.\deEfF]{%d}' % n

# Extract sub-columns from string column
def extractColumns(TableName,SourceParameterName,ParameterFormats,ParameterNames=None,FixCol=False):
    """
    INPUT PARAMETERS: 
        TableName:             name of source table              (required)
        SourceParameterName:   name of source column to process  (required)
        ParameterFormats:      c formats of unpacked parameters  (required)
        ParameterNames:        list of resulting parameter names (optional)
        FixCol:      column-fixed (True) format of source column (optional)
    OUTPUT PARAMETERS: 
        none
    ---
    DESCRIPTION:
        Note, that this function is aimed to do some extra job on
        interpreting string parameters which is normally supposed
        to be done by the user.
    ---
    EXAMPLE OF USAGE:
        extractColumns('sampletab',SourceParameterName='p5',
                        ParameterFormats=('%d','%d','%d'),
                        ParameterNames=('p5_1','p5_2','p5_3'))
        This example extracts three integer parameters from
        a source column 'p5' and puts results in ('p5_1','p5_2','p5_3').
    ---
    """
    # ParameterNames = just the names without expressions
    # ParFormats contains python formats for par extraction
    # Example: ParameterNames=('v1','v2','v3')
    #          ParameterFormats=('%1s','%1s','%1s')
    # By default the format of parameters is column-fixed
    if type(LOCAL_TABLE_CACHE[TableName]['header']['default'][SourceParameterName]) not in set([str,unicode]):
       raise Exception('Source parameter must be a string')
    i=-1
    # bug when (a,) != (a)
    if ParameterNames and type(ParameterNames) not in set([list,tuple]):
       ParameterNames = [ParameterNames]
    if ParameterFormats and type(ParameterFormats) not in set([list,tuple]):
       ParameterFormats = [ParameterFormats]
    # if ParameterNames is empty, fill it with #1-2-3-...
    if not ParameterNames:
       ParameterNames = []
       # using naming convension #i, i=0,1,2,3...
       for par_format in ParameterFormats:
           while True:
                 i+=1
                 par_name = '#%d' % i
                 fmt = LOCAL_TABLE_CACHE[TableName]['header']['format'].get(par_name,None)
                 if not fmt: break
           ParameterNames.append(par_name)
    # check if ParameterNames are valid
    Intersection = set(ParameterNames).intersection(LOCAL_TABLE_CACHE[TableName]['header']['order'])
    if Intersection:
       raise Exception('Parameters %s already exist' % str(list(Intersection)))
    # loop over ParameterNames to prepare LOCAL_TABLE_CACHE
    i=0
    for par_name in ParameterNames:  
        par_format = ParameterFormats[i]     
        LOCAL_TABLE_CACHE[TableName]['header']['format'][par_name]=par_format
        LOCAL_TABLE_CACHE[TableName]['data'][par_name]=[] 
        i+=1
    # append new parameters in order list
    LOCAL_TABLE_CACHE[TableName]['header']['order'] += ParameterNames
    # cope with default values
    i=0
    format_regex = []
    format_types = []
    for par_format in ParameterFormats:
        par_name = ParameterNames[i]
        regex = FORMAT_PYTHON_REGEX
        (lng,trail,lngpnt,ty) = re.search(regex,par_format).groups()
        ty = ty.lower()
        if ty == 'd':
           par_type = int
           if FixCol:
              format_regex_part = REGEX_INTEGER_FIXCOL(lng)
           else:
              format_regex_part = REGEX_INTEGER
        elif ty == 's':
           par_type = str
           if FixCol:
              format_regex_part = REGEX_STRING_FIXCOL(lng)
           else:
              format_regex_part = REGEX_STRING
        elif ty == 'f':
           par_type = float
           if FixCol:
              format_regex_part = REGEX_FLOAT_F_FIXCOL(lng)
           else:
              format_regex_part = REGEX_FLOAT_F
        elif ty == 'e':
           par_type = float
           if FixCol:
              format_regex_part = REGEX_FLOAT_E_FIXCOL(lng)
           else:
              format_regex_part = REGEX_FLOAT_E
        else:
           raise Exception('Unknown data type')
        format_regex.append('('+format_regex_part+')')
        format_types.append(par_type)
        def_val = getDefaultValue(par_type)
        LOCAL_TABLE_CACHE[TableName]['header']['default'][par_name]=def_val
        i+=1
    format_regex = '\s*'.join(format_regex)
    # loop through values of SourceParameter
    for SourceParameterString in LOCAL_TABLE_CACHE[TableName]['data'][SourceParameterName]:
        try:
           ExtractedValues = list(re.search(format_regex,SourceParameterString).groups())
        except:
           raise Exception('Error with line \"%s\"' % SourceParameterString)
        i=0
        # loop through all parameters which are supposed to be extracted
        for par_name in ParameterNames:
            par_value = format_types[i](ExtractedValues[i])
            LOCAL_TABLE_CACHE[TableName]['data'][par_name].append(par_value)
            i+=1
    # explicitly check that number of rows are equal
    number_of_rows = LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']
    number_of_rows2 = len(LOCAL_TABLE_CACHE[TableName]['data'][SourceParameterName])
    number_of_rows3 = len(LOCAL_TABLE_CACHE[TableName]['data'][ParameterNames[0]])
    if not (number_of_rows == number_of_rows2 == number_of_rows3):
       raise Exception('Error while extracting parameters: check your regexp')

# Split string columns into sub-columns with given names
def splitColumn(TableName,SourceParameterName,ParameterNames,Splitter):
    pass

# /EXTRACTING =======================================================

# ---------------------------------------------------------------
# ---------------------------------------------------------------
# /LOCAL DATABASE MANAGEMENT SYSTEM
# ---------------------------------------------------------------
# ---------------------------------------------------------------


# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# GLOBAL API FUNCTIONS
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

def mergeParlist(*arg):
    # Merge parlists and remove duplicates.
    # Argument contains a list of lists/tuples.
    container = []
    for a in arg:
        container += list(a)
    result = []
    index = set()
    for par_name in container:
        if par_name not in index:
            index.add(par_name)
            result.append(par_name)
    return result

# Define parameter groups to simplify the usage of fetch_
PARLIST_DOTPAR = ['par_line',]
PARLIST_ID = ['trans_id',]
PARLIST_STANDARD = ['molec_id','local_iso_id','nu','sw','a','elower','gamma_air',
                    'delta_air','gamma_self','n_air','n_self','gp','gpp']
PARLIST_LABELS = ['statep','statepp']
PARLIST_LINEMIXING = ['y_air','y_self']

PARLIST_VOIGT_AIR = ['gamma_air','delta_air','deltap_air','n_air']
PARLIST_VOIGT_SELF = ['gamma_self','delta_self','deltap_self','n_self']
PARLIST_VOIGT_H2 = ['gamma_H2','delta_H2','deltap_H2','n_H2']
PARLIST_VOIGT_CO2 = ['gamma_CO2','delta_CO2','n_CO2']
PARLIST_VOIGT_HE = ['gamma_He','delta_He','n_He']
PARLIST_VOIGT_H2O = ['gamma_H2O','n_H2O']
PARLIST_VOIGT_ALL = mergeParlist(PARLIST_VOIGT_AIR,PARLIST_VOIGT_SELF,
                                 PARLIST_VOIGT_H2,PARLIST_VOIGT_CO2,
                                 PARLIST_VOIGT_HE,PARLIST_VOIGT_H2O)

PARLIST_SDVOIGT_AIR = ['gamma_air','delta_air','deltap_air','n_air','SD_air']
PARLIST_SDVOIGT_SELF = ['gamma_self','delta_self','deltap_self','n_self','SD_self']
PARLIST_SDVOIGT_H2 = []
PARLIST_SDVOIGT_CO2 = []
PARLIST_SDVOIGT_HE = []
PARLIST_SDVOIGT_ALL = mergeParlist(PARLIST_SDVOIGT_AIR,PARLIST_SDVOIGT_SELF,
                                   PARLIST_SDVOIGT_H2,PARLIST_SDVOIGT_CO2,
                                   PARLIST_SDVOIGT_HE)

PARLIST_GALATRY_AIR = ['gamma_air','delta_air','deltap_air','n_air','beta_g_air']
PARLIST_GALATRY_SELF = ['gamma_self','delta_self','deltap_self','n_self','beta_g_self']
PARLIST_GALATRY_H2 = []
PARLIST_GALATRY_CO2 = []
PARLIST_GALATRY_HE = []
PARLIST_GALATRY_ALL = mergeParlist(PARLIST_GALATRY_AIR,PARLIST_GALATRY_SELF,
                                   PARLIST_GALATRY_H2,PARLIST_GALATRY_CO2,
                                   PARLIST_GALATRY_HE)

PARLIST_HT_SELF = ['gamma_HT_0_self_50','n_HT_self_50','gamma_HT_2_self_50',
                   'delta_HT_0_self_50','deltap_HT_self_50','delta_HT_2_self_50',
                   'gamma_HT_0_self_150','n_HT_self_150','gamma_HT_2_self_150',
                   'delta_HT_0_self_150','deltap_HT_self_150','delta_HT_2_self_150',
                   'gamma_HT_0_self_296','n_HT_self_296','gamma_HT_2_self_296',
                   'delta_HT_0_self_296','deltap_HT_self_296','delta_HT_2_self_296',
                   'gamma_HT_0_self_700','n_HT_self_700','gamma_HT_2_self_700',
                   'delta_HT_0_self_700','deltap_HT_self_700','delta_HT_2_self_700',
                   'nu_HT_self','kappa_HT_self','eta_HT_self']
#PARLIST_HT_AIR = ['gamma_HT_0_air_50','n_HT_air_50','gamma_HT_2_air_50',
#                  'delta_HT_0_air_50','deltap_HT_air_50','delta_HT_2_air_50',
#                  'gamma_HT_0_air_150','n_HT_air_150','gamma_HT_2_air_150',
#                  'delta_HT_0_air_150','deltap_HT_air_150','delta_HT_2_air_150',
#                  'gamma_HT_0_air_296','n_HT_air_296','gamma_HT_2_air_296',
#                  'delta_HT_0_air_296','deltap_HT_air_296','delta_HT_2_air_296',
#                  'gamma_HT_0_air_700','n_HT_air_700','gamma_HT_2_air_700',
#                  'delta_HT_0_air_700','deltap_HT_air_700','delta_HT_2_air_700',
#                  'nu_HT_air','kappa_HT_air','eta_HT_air']
PARLIST_HT_AIR = ['gamma_HT_0_air_296','n_HT_air_296','gamma_HT_2_air_296',
                  'delta_HT_0_air_296','deltap_HT_air_296','delta_HT_2_air_296',
                  'nu_HT_air','kappa_HT_air','eta_HT_air']
PARLIST_HT_ALL = mergeParlist(PARLIST_HT_SELF,PARLIST_HT_AIR)
                                   
PARLIST_ALL = mergeParlist(PARLIST_ID,PARLIST_DOTPAR,PARLIST_STANDARD,
                           PARLIST_LABELS,PARLIST_LINEMIXING,PARLIST_VOIGT_ALL,
                           PARLIST_SDVOIGT_ALL,PARLIST_GALATRY_ALL,PARLIST_HT_ALL)

PARAMETER_GROUPS = {
  'par_line' : PARLIST_DOTPAR,
  '160-char' : PARLIST_DOTPAR,
  '.par' : PARLIST_DOTPAR,
  'id' : PARLIST_ID,
  'standard' : PARLIST_STANDARD,
  'labels' : PARLIST_LABELS,
  'linemixing' : PARLIST_LINEMIXING,
  'voigt_air' : PARLIST_VOIGT_AIR,
  'voigt_self' : PARLIST_VOIGT_SELF,
  'voigt_h2' : PARLIST_VOIGT_H2,
  'voigt_co2' : PARLIST_VOIGT_CO2,
  'voigt_he' : PARLIST_VOIGT_HE,
  'voigt_h2o' : PARLIST_VOIGT_H2O,
  'voigt' : PARLIST_VOIGT_ALL,
  'sdvoigt_air' : PARLIST_SDVOIGT_AIR,
  'sdvoigt_self' : PARLIST_SDVOIGT_SELF,
  'sdvoigt_h2' : PARLIST_SDVOIGT_H2,
  'sdvoigt_co2' : PARLIST_SDVOIGT_CO2,
  'sdvoigt_he' : PARLIST_SDVOIGT_HE,
  'sdvoigt' : PARLIST_SDVOIGT_ALL,
  'galatry_air' : PARLIST_GALATRY_AIR,
  'galatry_self' : PARLIST_GALATRY_SELF,
  'galatry_h2' : PARLIST_GALATRY_H2,
  'galatry_co2' : PARLIST_GALATRY_CO2,
  'galatry_he' : PARLIST_GALATRY_HE,
  'galatry' : PARLIST_GALATRY_ALL,
  'ht' : PARLIST_HT_ALL,
  'all' : PARLIST_ALL
}

def prepareParlist(pargroups=[],params=[],dotpar=True):
    # Apply defaults
    parlist_default = []
    if dotpar:
        parlist_default += ['par_line']
    #parlist_default += PARAMETER_GROUPS['id']
    
    # Make a dictionary of "assumed" parameters.
    ASSUMED_PARAMS = {}
    if 'par_line' in set(parlist_default):
        ASSUMED_PARAMS = HITRAN_DEFAULT_HEADER['format']
    
    parlist = parlist_default
    
    # Iterate over parameter groups.
    for pargroup in pargroups:
        pargroup = pargroup.lower()
        parlist += PARAMETER_GROUPS[pargroup]
        
    # Iterate over single parameters.
    for param in params:
        #param = param.lower()
        parlist.append(param)
        
    # Clean up parameter list.
    parlist = mergeParlist(parlist)
    result = []
    for param in parlist:
        if param not in ASSUMED_PARAMS:
            result.append(param)
    
    return result

def prepareHeader(parlist):
    HEADER = {'table_name':'','number_of_rows':-1,'format':{},
              'default':{},'table_type':'column-fixed',
              'size_in_bytes':-1,'order':[],'description':{}}
    
    # Add column-fixed 160-character part, if specified in parlist.
    if 'par_line' in set(parlist):
        HEADER['order'] = HITRAN_DEFAULT_HEADER['order']
        HEADER['format'] = HITRAN_DEFAULT_HEADER['format']
        HEADER['default'] = HITRAN_DEFAULT_HEADER['default']
        HEADER['description'] = HITRAN_DEFAULT_HEADER['description']
        HEADER['position'] = HITRAN_DEFAULT_HEADER['position']

    # Insert all other parameters in the "extra" section of the header.
    plist = [v for v in parlist if v!='par_line']
    HEADER['extra'] = []
    HEADER['extra_format'] = {}
    HEADER['extra_separator'] = ','
    for param in plist:
        param = param.lower()
        HEADER['extra'].append(param)
        HEADER['extra_format'][param] = PARAMETER_META[param]['default_fmt']
        
    return HEADER
        
def queryHITRAN(TableName,iso_id_list,numin,numax,pargroups=[],params=[],dotpar=True,head=False):
    ParameterList = prepareParlist(pargroups=pargroups,params=params,dotpar=dotpar)
    TableHeader = prepareHeader(ParameterList)
    TableHeader['table_name'] = TableName
    DataFileName = VARIABLES['BACKEND_DATABASE_NAME'] + '/' + TableName + '.data'
    HeaderFileName = VARIABLES['BACKEND_DATABASE_NAME'] + '/' + TableName + '.header'
    # create URL
    iso_id_list_str = [str(iso_id) for iso_id in iso_id_list]
    iso_id_list_str = ','.join(iso_id_list_str)
    print('\nData is fetched from %s\n'%VARIABLES['GLOBAL_HOST'])
    if pargroups or params: # custom par search
        url = VARIABLES['GLOBAL_HOST'] + '/lbl/api?' + \
        'iso_ids_list=' + iso_id_list_str + '&' + \
        'numin=' + str(numin) + '&' + \
        'numax=' + str(numax) + '&' + \
        'head=' + str(head) + '&' + \
        'fixwidth=0&sep=[comma]&' +\
        'request_params=' + ','.join(ParameterList)
    else: # old-fashioned .par search
        url = VARIABLES['GLOBAL_HOST'] + '/lbl/api?' + \
        'iso_ids_list=' + iso_id_list_str + '&' + \
        'numin=' + str(numin) + '&' + \
        'numax=' + str(numax)
    #raise Exception(url)
    # Download data by chunks.
    if VARIABLES['DISPLAY_FETCH_URL']: print(url+'\n')
    try:       
        # Proxy handling # https://stackoverflow.com/questions/1450132/proxy-with-urllib2
        if VARIABLES['PROXY']:
            print('Using proxy '+str(VARIABLES['PROXY']))
            proxy = urllib2.ProxyHandler(VARIABLES['PROXY'])
            opener = urllib2.build_opener(proxy)
            urllib2.install_opener(opener)            
        req = urllib2.urlopen(url)
    except urllib2.HTTPError:
        raise Exception('Failed to retrieve data for given parameters.')
    except urllib2.URLError:
        raise Exception('Cannot connect to %s. Try again or edit GLOBAL_HOST variable.' % GLOBAL_HOST)
    CHUNK = 64 * 1024
    print('BEGIN DOWNLOAD: '+TableName)
    with open_(DataFileName,'w') as fp:
       while True:
          chunk = req.read(CHUNK)
          if not chunk: break
          fp.write(chunk.decode('utf-8'))
          print('  %d bytes written to %s' % (CHUNK,DataFileName))
    with open(HeaderFileName,'w') as fp:       
       fp.write(json.dumps(TableHeader,indent=2))
       print('Header written to %s' % HeaderFileName)
    print('END DOWNLOAD')
    # Set comment
    # Get this table to LOCAL_TABLE_CACHE
    storage2cache(TableName)
    print('PROCESSED')

def saveHeader(TableName):
    ParameterList = prepareParlist(dotpar=True)    
    TableHeader = prepareHeader(ParameterList)
    with open(TableName+'.header','w') as fp:
       fp.write(json.dumps(TableHeader,indent=2))
    
# ---------- DATABASE FRONTEND END -------------

# simple implementation of getting a line list from a remote server
def getLinelist(local_name,query,api_key):
    return makeQuery(local_name)

# -------------------------------------------------------------------
# -------------------------------------------------------------------
# / GLOBABL API FUNCTIONS
# -------------------------------------------------------------------
# -------------------------------------------------------------------



# ---------------- FILTER ---------------------------------------------

def filter(TableName,Conditions):
    select(TableName=TableName,Conditions=Conditions,Output=False)

# ---------------------- ISO.PY ---------------------------------------

ISO_ID_INDEX = {

'M':0,
'I':1,
'iso_name':2,
'abundance':3,
'mass':4,
'mol_name':5

}

#    id           M    I    iso_name                    abundance           mass        mol_name

ISO_ID = {
                            
      1 : [       1,   1,  'H2(16O)',                   0.997317,           18.010565,      'H2O'     ],
      2 : [       1,   2,  'H2(18O)',                   0.00199983,         20.014811,      'H2O'     ],
      3 : [       1,   3,  'H2(17O)',                   0.000372,           19.01478,       'H2O'     ],
      4 : [       1,   4,  'HD(16O)',                   0.00031069,         19.01674,       'H2O'     ],
      5 : [       1,   5,  'HD(18O)',                   0.000000623,        21.020985,      'H2O'     ],
      6 : [       1,   6,  'HD(17O)',                   0.000000116,        20.020956,      'H2O'     ],
    129 : [       1,   7,  'D2(16O)',                   0.000000024197,     20.022915,      'H2O'     ],
      7 : [       2,   1,  '(12C)(16O)2',               0.984204,           43.98983,       'CO2'     ],
      8 : [       2,   2,  '(13C)(16O)2',               0.011057,           44.993185,      'CO2'     ],
      9 : [       2,   3,  '(16O)(12C)(18O)',           0.0039471,          45.994076,      'CO2'     ],
     10 : [       2,   4,  '(16O)(12C)(17O)',           0.000734,           44.994045,      'CO2'     ],
     11 : [       2,   5,  '(16O)(13C)(18O)',           0.00004434,         46.997431,      'CO2'     ],
     12 : [       2,   6,  '(16O)(13C)(17O)',           0.00000825,         45.9974,        'CO2'     ],
     13 : [       2,   7,  '(12C)(18O)2',               0.0000039573,       47.998322,      'CO2'     ],
     14 : [       2,   8,  '(17O)(12C)(18O)',           0.00000147,         46.998291,      'CO2'     ],
    121 : [       2,   9,  '(12C)(17O)2',               0.0000001368,       45.998262,      'CO2'     ],
     15 : [       2,  10,  '(13C)(18O)2',               0.000000044967,     49.001675,      'CO2'     ],  # 0->11
    120 : [       2,  11,  '(18O)(13C)(17O)',           0.00000001654,      48.00165,       'CO2'     ],  # 'A'->11
    122 : [       2,  12,  '(13C)(17O)2',               0.0000000015375,    47.001618,      'CO2'     ],  # 'B'->12
     16 : [       3,   1,  '(16O)3',                    0.992901,           47.984745,      'O3'      ],
     17 : [       3,   2,  '(16O)(16O)(18O)',           0.00398194,         49.988991,      'O3'      ],
     18 : [       3,   3,  '(16O)(18O)(16O)',           0.00199097,         49.988991,      'O3'      ],
     19 : [       3,   4,  '(16O)(16O)(17O)',           0.00074,            48.98896,       'O3'      ],
     20 : [       3,   5,  '(16O)(17O)(16O)',           0.00037,            48.98896,       'O3'      ],
     21 : [       4,   1,  '(14N)2(16O)',               0.990333,           44.001062,      'N2O'     ],
     22 : [       4,   2,  '(14N)(15N)(16O)',           0.0036409,          44.998096,      'N2O'     ],
     23 : [       4,   3,  '(15N)(14N)(16O)',           0.0036409,          44.998096,      'N2O'     ],
     24 : [       4,   4,  '(14N)2(18O)',               0.00198582,         46.005308,      'N2O'     ],
     25 : [       4,   5,  '(14N)2(17O)',               0.000369,           45.005278,      'N2O'     ],
     26 : [       5,   1,  '(12C)(16O)',                0.98654,            27.994915,      'CO'      ],
     27 : [       5,   2,  '(13C)(16O)',                0.01108,            28.99827,       'CO'      ],
     28 : [       5,   3,  '(12C)(18O)',                0.0019782,          29.999161,      'CO'      ],
     29 : [       5,   4,  '(12C)(17O)',                0.000368,           28.99913,       'CO'      ],
     30 : [       5,   5,  '(13C)(18O)',                0.00002222,         31.002516,      'CO'      ],
     31 : [       5,   6,  '(13C)(17O)',                0.00000413,         30.002485,      'CO'      ],
     32 : [       6,   1,  '(12C)H4',                   0.98827,            16.0313,        'CH4'     ],
     33 : [       6,   2,  '(13C)H4',                   0.0111,             17.034655,      'CH4'     ],
     34 : [       6,   3,  '(12C)H3D',                  0.00061575,         17.037475,      'CH4'     ],
     35 : [       6,   4,  '(13C)H3D',                  0.0000049203,       18.04083,       'CH4'     ],
     36 : [       7,   1,  '(16O)2',                    0.995262,           31.98983,       'O2'      ],
     37 : [       7,   2,  '(16O)(18O)',                0.00399141,         33.994076,      'O2'      ],
     38 : [       7,   3,  '(16O)(17O)',                0.000742,           32.994045,      'O2'      ],
     39 : [       8,   1,  '(14N)(16O)',                0.993974,           29.997989,      'NO'      ],
     40 : [       8,   2,  '(15N)(16O)',                0.0036543,          30.995023,      'NO'      ],
     41 : [       8,   3,  '(14N)(18O)',                0.00199312,         32.002234,      'NO'      ],
     42 : [       9,   1,  '(32S)(16O)2',               0.94568,            63.961901,      'SO2'     ],
     43 : [       9,   2,  '(34S)(16O)2',               0.04195,            65.957695,      'SO2'     ],
     44 : [      10,   1,  '(14N)(16O)2',               0.991616,           45.992904,      'NO2'     ],
     45 : [      11,   1,  '(14N)H3',                   0.9958715,          17.026549,      'NH3'     ],
     46 : [      11,   2,  '(15N)H3',                   0.0036613,          18.023583,      'NH3'     ],
     47 : [      12,   1,  'H(14N)(16O)3',              0.98911,            62.995644,      'HNO3'    ],
    117 : [      12,   2,  'H(15N)(16O)3',              0.003636,           63.99268,       'HNO3'    ],
     48 : [      13,   1,  '(16O)H',                    0.997473,           17.00274,       'OH'      ],
     49 : [      13,   2,  '(18O)H',                    0.00200014,         19.006986,      'OH'      ],
     50 : [      13,   3,  '(16O)D',                    0.00015537,         18.008915,      'OH'      ],
     51 : [      14,   1,  'H(19F)',                    0.99984425,         20.006229,      'HF'      ],
    110 : [      14,   2,  'D(19F)',                    0.000115,           21.0125049978,  'HF'      ],
     52 : [      15,   1,  'H(35Cl)',                   0.757587,           35.976678,      'HCl'     ],
     53 : [      15,   2,  'H(37Cl)',                   0.242257,           37.973729,      'HCl'     ],
    107 : [      15,   3,  'D(35Cl)',                   0.000118005,        36.9829544578,  'HCl'     ],
    108 : [      15,   4,  'D(37Cl)',                   0.000037735,        38.9800043678,  'HCl'     ],
     54 : [      16,   1,  'H(79Br)',                   0.50678,            79.92616,       'HBr'     ],
     55 : [      16,   2,  'H(81Br)',                   0.49306,            81.924115,      'HBr'     ],
    111 : [      16,   3,  'D(79Br)',                   0.0000582935,       80.9324388778,  'HBr'     ],
    112 : [      16,   4,  'D(81Br)',                   0.0000567065,       82.9303923778,  'HBr'     ],
     56 : [      17,   1,  'H(127I)',                   0.99984425,         127.912297,     'HI'      ],
    113 : [      17,   2,  'D(127I)',                   0.000115,           128.918574778,  'HI'      ],
     57 : [      18,   1,  '(35Cl)(16O)',               0.75591,            50.963768,      'ClO'     ],
     58 : [      18,   2,  '(37Cl)(16O)',               0.24172,            52.960819,      'ClO'     ],
     59 : [      19,   1,  '(16O)(12C)(32S)',           0.93739,            59.966986,      'OCS'     ],
     60 : [      19,   2,  '(16O)(12C)(34S)',           0.04158,            61.96278,       'OCS'     ],
     61 : [      19,   3,  '(16O)(13C)(32S)',           0.01053,            60.970341,      'OCS'     ],
     62 : [      19,   4,  '(16O)(12C)(33S)',           0.01053,            60.966371,      'OCS'     ],
     63 : [      19,   5,  '(18O)(12C)(32S)',           0.00188,            61.971231,      'OCS'     ],
     64 : [      20,   1,  'H2(12C)(16O)',              0.98624,            30.010565,      'H2CO'    ],
     65 : [      20,   2,  'H2(13C)(16O)',              0.01108,            31.01392,       'H2CO'    ],
     66 : [      20,   3,  'H2(12C)(18O)',              0.0019776,          32.014811,      'H2CO'    ],
     67 : [      21,   1,  'H(16O)(35Cl)',              0.75579,            51.971593,      'HOCl'    ],
     68 : [      21,   2,  'H(16O)(37Cl)',              0.24168,            53.968644,      'HOCl'    ],
     69 : [      22,   1,  '(14N)2',                    0.9926874,          28.006147,      'N2'      ],
    118 : [      22,   2,  '(14N)(15N)',                0.0072535,          29.997989,      'N2'      ],
     70 : [      23,   1,  'H(12C)(14N)',               0.98511,            27.010899,      'HCN'     ],
     71 : [      23,   2,  'H(13C)(14N)',               0.01107,            28.014254,      'HCN'     ],
     72 : [      23,   3,  'H(12C)(15N)',               0.0036217,          28.007933,      'HCN'     ],
     73 : [      24,   1,  '(12C)H3(35Cl)',             0.74894,            49.992328,      'CH3Cl'   ],
     74 : [      24,   2,  '(12C)H3(37Cl)',             0.23949,            51.989379,      'CH3Cl'   ],
     75 : [      25,   1,  'H2(16O)2',                  0.994952,           34.00548,       'H2O2'    ],
     76 : [      26,   1,  '(12C)2H2',                  0.9776,             26.01565,       'C2H2'    ],
     77 : [      26,   2,  '(12C)(13C)H2',              0.02197,            27.019005,      'C2H2'    ],
    105 : [      26,   3,  '(12C)2HD',                  0.00030455,         27.021825,      'C2H2'    ],
     78 : [      27,   1,  '(12C)2H6',                  0.97699,            30.04695,       'C2H6'    ],
    106 : [      27,   2,  '(12C)H3(13C)H3',            0.021952611,        31.050305,      'C2H6'    ],
     79 : [      28,   1,  '(31P)H3',                   0.99953283,         33.997238,      'PH3'     ],
     80 : [      29,   1,  '(12C)(16O)(19F)2',          0.98654,            65.991722,      'COF2'    ],
    119 : [      29,   2,  '(13C)(16O)(19F)2',          0.0110834,          66.995083,      'COF2'    ],
    126 : [      30,   1,  '(32S)(19F)6',               0.950180,          145.962492,      'SF6'     ],
     81 : [      31,   1,  'H2(32S)',                   0.94988,            33.987721,      'H2S'     ],
     82 : [      31,   2,  'H2(34S)',                   0.04214,            35.983515,      'H2S'     ],
     83 : [      31,   3,  'H2(33S)',                   0.007498,           34.987105,      'H2S'     ],
     84 : [      32,   1,  'H(12C)(16O)(16O)H',         0.983898,           46.00548,       'HCOOH'   ],
     85 : [      33,   1,  'H(16O)2',                   0.995107,           32.997655,      'HO2'     ],
     86 : [      34,   1,  '(16O)',                     0.997628,           15.994915,      'O'       ],
     87 : [      36,   1,  '(14N)(16O)+',               0.993974,           29.997989,      'NOp'     ],
     88 : [      37,   1,  'H(16O)(79Br)',              0.5056,             95.921076,      'HOBr'    ],
     89 : [      37,   2,  'H(16O)(81Br)',              0.4919,             97.919027,      'HOBr'    ],
     90 : [      38,   1,  '(12C)2H4',                  0.9773,             28.0313,        'C2H4'    ],
     91 : [      38,   2,  '(12C)H2(13C)H2',            0.02196,            29.034655,      'C2H4'    ],
     92 : [      39,   1,  '(12C)H3(16O)H',             0.98593,            32.026215,      'CH3OH'   ],
     93 : [      40,   1,  '(12C)H3(79Br)',             0.5013,             93.941811,      'CH3Br'   ],
     94 : [      40,   2,  '(12C)H3(81Br)',             0.48766,            95.939764,      'CH3Br'   ],
     95 : [      41,   1,  '(12C)H3(12C)(14N)',         0.97482,            41.026549,      'CH3CN'   ],
     96 : [      42,   1,  '(12C)(19F)4',               0.9893,             87.993616,      'CF4'     ],
    116 : [      43,   1,  '(12C)4H2',                  0.955998,           50.01565,       'C4H2'    ],
    109 : [      44,   1,  'H(12C)3(14N)',              0.9646069,          51.01089903687, 'HC3N'    ],
    103 : [      45,   1,  'H2',                        0.999688,           2.01565,        'H2'      ],
    115 : [      45,   2,  'HD',                        0.000311432,        3.021825,       'H2'      ],
     97 : [      46,   1,  '(12C)(32S)',                0.939624,           43.971036,      'CS'      ],
     98 : [      46,   2,  '(12C)(34S)',                0.0416817,          45.966787,      'CS'      ],
     99 : [      46,   3,  '(13C)(32S)',                0.0105565,          44.974368,      'CS'      ],
    100 : [      46,   4,  '(12C)(33S)',                0.00741668,         44.970399,      'CS'      ],
    114 : [      47,   1,  '(32S)(16O)3',               0.9423964,          79.95682,       'SO3'     ],    
    123 : [      48,   1,  '(12C)2(14N)2',              0.970752433,        52.006148,      'C2N2'    ],
    124 : [      49,   1,  '(12C)(16O)(35Cl)2',         0.566391761,        97.9326199796,  'COCl2'   ],
    125 : [      49,   2,  '(12C)(16O)(35Cl)(37Cl)',    0.362235278,        99.9296698896,  'COCl2'   ],    
#    101 : [    1001,   1,  'H',                         None,               None,           'H'       ],
#    102 : [    1002,   1,  'He',                        None,               None,           'He'      ],
#    104 : [    1018,   1,  'Ar',                        None,               None,           'Ar'      ],

}

ISO_INDEX = {

'id':0,
'iso_name':1,
'abundance':2,
'mass':3,
'mol_name':4

}

#        M    I             id    iso_name                    abundance           mass        mol_name

ISO = {
                            
(        1,   1    ): [      1,  'H2(16O)',                   0.997317,           18.010565,      'H2O'     ],
(        1,   2    ): [      2,  'H2(18O)',                   0.00199983,         20.014811,      'H2O'     ],
(        1,   3    ): [      3,  'H2(17O)',                   0.000372,           19.01478,       'H2O'     ],
(        1,   4    ): [      4,  'HD(16O)',                   0.00031069,         19.01674,       'H2O'     ],
(        1,   5    ): [      5,  'HD(18O)',                   0.000000623,        21.020985,      'H2O'     ],
(        1,   6    ): [      6,  'HD(17O)',                   0.000000116,        20.020956,      'H2O'     ],
(        1,   7    ): [    129,  'D2(16O)',                   0.000000024197,     20.022915,      'H2O'     ],
(        2,   1    ): [      7,  '(12C)(16O)2',               0.984204,           43.98983,       'CO2'     ],
(        2,   2    ): [      8,  '(13C)(16O)2',               0.011057,           44.993185,      'CO2'     ],
(        2,   3    ): [      9,  '(16O)(12C)(18O)',           0.0039471,          45.994076,      'CO2'     ],
(        2,   4    ): [     10,  '(16O)(12C)(17O)',           0.000734,           44.994045,      'CO2'     ],
(        2,   5    ): [     11,  '(16O)(13C)(18O)',           0.00004434,         46.997431,      'CO2'     ],
(        2,   6    ): [     12,  '(16O)(13C)(17O)',           0.00000825,         45.9974,        'CO2'     ],
(        2,   7    ): [     13,  '(12C)(18O)2',               0.0000039573,       47.998322,      'CO2'     ],
(        2,   8    ): [     14,  '(17O)(12C)(18O)',           0.00000147,         46.998291,      'CO2'     ],
(        2,   9    ): [    121,  '(12C)(17O)2',               0.0000001368,       45.998262,      'CO2'     ],
(        2,  10    ): [     15,  '(13C)(18O)2',               0.000000044967,     49.001675,      'CO2'     ],  # 0->10
(        2,  11    ): [    120,  '(18O)(13C)(17O)',           0.00000001654,      48.00165,       'CO2'     ],  # 'A'->11
(        2,  12    ): [    122,  '(13C)(17O)2',               0.0000000015375,    47.001618,      'CO2'     ],  # 'B'->12
(        3,   1    ): [     16,  '(16O)3',                    0.992901,           47.984745,      'O3'      ],
(        3,   2    ): [     17,  '(16O)(16O)(18O)',           0.00398194,         49.988991,      'O3'      ],
(        3,   3    ): [     18,  '(16O)(18O)(16O)',           0.00199097,         49.988991,      'O3'      ],
(        3,   4    ): [     19,  '(16O)(16O)(17O)',           0.00074,            48.98896,       'O3'      ],
(        3,   5    ): [     20,  '(16O)(17O)(16O)',           0.00037,            48.98896,       'O3'      ],
(        4,   1    ): [     21,  '(14N)2(16O)',               0.990333,           44.001062,      'N2O'     ],
(        4,   2    ): [     22,  '(14N)(15N)(16O)',           0.0036409,          44.998096,      'N2O'     ],
(        4,   3    ): [     23,  '(15N)(14N)(16O)',           0.0036409,          44.998096,      'N2O'     ],
(        4,   4    ): [     24,  '(14N)2(18O)',               0.00198582,         46.005308,      'N2O'     ],
(        4,   5    ): [     25,  '(14N)2(17O)',               0.000369,           45.005278,      'N2O'     ],
(        5,   1    ): [     26,  '(12C)(16O)',                0.98654,            27.994915,      'CO'      ],
(        5,   2    ): [     27,  '(13C)(16O)',                0.01108,            28.99827,       'CO'      ],
(        5,   3    ): [     28,  '(12C)(18O)',                0.0019782,          29.999161,      'CO'      ],
(        5,   4    ): [     29,  '(12C)(17O)',                0.000368,           28.99913,       'CO'      ],
(        5,   5    ): [     30,  '(13C)(18O)',                0.00002222,         31.002516,      'CO'      ],
(        5,   6    ): [     31,  '(13C)(17O)',                0.00000413,         30.002485,      'CO'      ],
(        6,   1    ): [     32,  '(12C)H4',                   0.98827,            16.0313,        'CH4'     ],
(        6,   2    ): [     33,  '(13C)H4',                   0.0111,             17.034655,      'CH4'     ],
(        6,   3    ): [     34,  '(12C)H3D',                  0.00061575,         17.037475,      'CH4'     ],
(        6,   4    ): [     35,  '(13C)H3D',                  0.0000049203,       18.04083,       'CH4'     ],
(        7,   1    ): [     36,  '(16O)2',                    0.995262,           31.98983,       'O2'      ],
(        7,   2    ): [     37,  '(16O)(18O)',                0.00399141,         33.994076,      'O2'      ],
(        7,   3    ): [     38,  '(16O)(17O)',                0.000742,           32.994045,      'O2'      ],
(        8,   1    ): [     39,  '(14N)(16O)',                0.993974,           29.997989,      'NO'      ],
(        8,   2    ): [     40,  '(15N)(16O)',                0.0036543,          30.995023,      'NO'      ],
(        8,   3    ): [     41,  '(14N)(18O)',                0.00199312,         32.002234,      'NO'      ],
(        9,   1    ): [     42,  '(32S)(16O)2',               0.94568,            63.961901,      'SO2'     ],
(        9,   2    ): [     43,  '(34S)(16O)2',               0.04195,            65.957695,      'SO2'     ],
(       10,   1    ): [     44,  '(14N)(16O)2',               0.991616,           45.992904,      'NO2'     ],
(       11,   1    ): [     45,  '(14N)H3',                   0.9958715,          17.026549,      'NH3'     ],
(       11,   2    ): [     46,  '(15N)H3',                   0.0036613,          18.023583,      'NH3'     ],
(       12,   1    ): [     47,  'H(14N)(16O)3',              0.98911,            62.995644,      'HNO3'    ],
(       12,   2    ): [    117,  'H(15N)(16O)3',              0.003636,           63.99268,       'HNO3'    ],
(       13,   1    ): [     48,  '(16O)H',                    0.997473,           17.00274,       'OH'      ],
(       13,   2    ): [     49,  '(18O)H',                    0.00200014,         19.006986,      'OH'      ],
(       13,   3    ): [     50,  '(16O)D',                    0.00015537,         18.008915,      'OH'      ],
(       14,   1    ): [     51,  'H(19F)',                    0.99984425,         20.006229,      'HF'      ],
(       14,   2    ): [    110,  'D(19F)',                    0.000115,           21.0125049978,  'HF'      ],
(       15,   1    ): [     52,  'H(35Cl)',                   0.757587,           35.976678,      'HCl'     ],
(       15,   2    ): [     53,  'H(37Cl)',                   0.242257,           37.973729,      'HCl'     ],
(       15,   3    ): [    107,  'D(35Cl)',                   0.000118005,        36.9829544578,  'HCl'     ],
(       15,   4    ): [    108,  'D(37Cl)',                   0.000037735,        38.9800043678,  'HCl'     ],
(       16,   1    ): [     54,  'H(79Br)',                   0.50678,            79.92616,       'HBr'     ],
(       16,   2    ): [     55,  'H(81Br)',                   0.49306,            81.924115,      'HBr'     ],
(       16,   3    ): [    111,  'D(79Br)',                   0.0000582935,       80.9324388778,  'HBr'     ],
(       16,   4    ): [    112,  'D(81Br)',                   0.0000567065,       82.9303923778,  'HBr'     ],
(       17,   1    ): [     56,  'H(127I)',                   0.99984425,         127.912297,     'HI'      ],
(       17,   2    ): [    113,  'D(127I)',                   0.000115,           128.918574778,  'HI'      ],
(       18,   1    ): [     57,  '(35Cl)(16O)',               0.75591,            50.963768,      'ClO'     ],
(       18,   2    ): [     58,  '(37Cl)(16O)',               0.24172,            52.960819,      'ClO'     ],
(       19,   1    ): [     59,  '(16O)(12C)(32S)',           0.93739,            59.966986,      'OCS'     ],
(       19,   2    ): [     60,  '(16O)(12C)(34S)',           0.04158,            61.96278,       'OCS'     ],
(       19,   3    ): [     61,  '(16O)(13C)(32S)',           0.01053,            60.970341,      'OCS'     ],
(       19,   4    ): [     62,  '(16O)(12C)(33S)',           0.01053,            60.966371,      'OCS'     ],
(       19,   5    ): [     63,  '(18O)(12C)(32S)',           0.00188,            61.971231,      'OCS'     ],
(       20,   1    ): [     64,  'H2(12C)(16O)',              0.98624,            30.010565,      'H2CO'    ],
(       20,   2    ): [     65,  'H2(13C)(16O)',              0.01108,            31.01392,       'H2CO'    ],
(       20,   3    ): [     66,  'H2(12C)(18O)',              0.0019776,          32.014811,      'H2CO'    ],
(       21,   1    ): [     67,  'H(16O)(35Cl)',              0.75579,            51.971593,      'HOCl'    ],
(       21,   2    ): [     68,  'H(16O)(37Cl)',              0.24168,            53.968644,      'HOCl'    ],
(       22,   1    ): [     69,  '(14N)2',                    0.9926874,          28.006147,      'N2'      ],
(       22,   2    ): [    118,  '(14N)(15N)',                0.0072535,          29.997989,      'N2'      ],
(       23,   1    ): [     70,  'H(12C)(14N)',               0.98511,            27.010899,      'HCN'     ],
(       23,   2    ): [     71,  'H(13C)(14N)',               0.01107,            28.014254,      'HCN'     ],
(       23,   3    ): [     72,  'H(12C)(15N)',               0.0036217,          28.007933,      'HCN'     ],
(       24,   1    ): [     73,  '(12C)H3(35Cl)',             0.74894,            49.992328,      'CH3Cl'   ],
(       24,   2    ): [     74,  '(12C)H3(37Cl)',             0.23949,            51.989379,      'CH3Cl'   ],
(       25,   1    ): [     75,  'H2(16O)2',                  0.994952,           34.00548,       'H2O2'    ],
(       26,   1    ): [     76,  '(12C)2H2',                  0.9776,             26.01565,       'C2H2'    ],
(       26,   2    ): [     77,  '(12C)(13C)H2',              0.02197,            27.019005,      'C2H2'    ],
(       26,   3    ): [    105,  '(12C)2HD',                  0.00030455,         27.021825,      'C2H2'    ],
(       27,   1    ): [     78,  '(12C)2H6',                  0.97699,            30.04695,       'C2H6'    ],
(       27,   2    ): [    106,  '(12C)H3(13C)H3',            0.021952611,        31.050305,      'C2H6'    ],
(       28,   1    ): [     79,  '(31P)H3',                   0.99953283,         33.997238,      'PH3'     ],
(       29,   1    ): [     80,  '(12C)(16O)(19F)2',          0.98654,            65.991722,      'COF2'    ],
(       29,   2    ): [    119,  '(13C)(16O)(19F)2',          0.0110834,          66.995083,      'COF2'    ],
(       30,   1    ): [    126,  '(32S)(19F)6',               0.950180,          145.962492,      'SF6'     ],
(       31,   1    ): [     81,  'H2(32S)',                   0.94988,            33.987721,      'H2S'     ],
(       31,   2    ): [     82,  'H2(34S)',                   0.04214,            35.983515,      'H2S'     ],
(       31,   3    ): [     83,  'H2(33S)',                   0.007498,           34.987105,      'H2S'     ],
(       32,   1    ): [     84,  'H(12C)(16O)(16O)H',         0.983898,           46.00548,       'HCOOH'   ],
(       33,   1    ): [     85,  'H(16O)2',                   0.995107,           32.997655,      'HO2'     ],
(       34,   1    ): [     86,  '(16O)',                     0.997628,           15.994915,      'O'       ],
(       36,   1    ): [     87,  '(14N)(16O)+',               0.993974,           29.997989,      'NOp'     ],
(       37,   1    ): [     88,  'H(16O)(79Br)',              0.5056,             95.921076,      'HOBr'    ],
(       37,   2    ): [     89,  'H(16O)(81Br)',              0.4919,             97.919027,      'HOBr'    ],
(       38,   1    ): [     90,  '(12C)2H4',                  0.9773,             28.0313,        'C2H4'    ],
(       38,   2    ): [     91,  '(12C)H2(13C)H2',            0.02196,            29.034655,      'C2H4'    ],
(       39,   1    ): [     92,  '(12C)H3(16O)H',             0.98593,            32.026215,      'CH3OH'   ],
(       40,   1    ): [     93,  '(12C)H3(79Br)',             0.5013,             93.941811,      'CH3Br'   ],
(       40,   2    ): [     94,  '(12C)H3(81Br)',             0.48766,            95.939764,      'CH3Br'   ],
(       41,   1    ): [     95,  '(12C)H3(12C)(14N)',         0.97482,            41.026549,      'CH3CN'   ],
(       42,   1    ): [     96,  '(12C)(19F)4',               0.9893,             87.993616,      'CF4'     ],
(       43,   1    ): [    116,  '(12C)4H2',                  0.955998,           50.01565,       'C4H2'    ],
(       44,   1    ): [    109,  'H(12C)3(14N)',              0.9646069,          51.01089903687, 'HC3N'    ],
(       45,   1    ): [    103,  'H2',                        0.999688,           2.01565,        'H2'      ],
(       45,   2    ): [    115,  'HD',                        0.000311432,        3.021825,       'H2'      ],
(       46,   1    ): [     97,  '(12C)(32S)',                0.939624,           43.971036,      'CS'      ],
(       46,   2    ): [     98,  '(12C)(34S)',                0.0416817,          45.966787,      'CS'      ],
(       46,   3    ): [     99,  '(13C)(32S)',                0.0105565,          44.974368,      'CS'      ],
(       46,   4    ): [    100,  '(12C)(33S)',                0.00741668,         44.970399,      'CS'      ],
(       47,   1    ): [    114,  '(32S)(16O)3',               0.9423964,          79.95682,       'SO3'     ],
(       48,   1    ): [    123,  '(12C)2(14N)2',              0.970752433,        52.006148,      'C2N2'    ],
(       49,   1    ): [    124,  '(12C)(16O)(35Cl)2',         0.566391761,        97.9326199796,  'COCl2'   ],
(       49,   2    ): [    125,  '(12C)(16O)(35Cl)(37Cl)',    0.362235278,        99.9296698896,  'COCl2'   ],
#(     1001,   1    ): [    101,  'H',                         None,               None,           'H'       ],
#(     1002,   1    ): [    102,  'He',                        None,               None,           'He'      ],
#(     1018,   1    ): [    104,  'Ar',                        None,               None,           'Ar'      ],

}

def print_iso():
    print('The dictionary \"ISO\" contains information on isotopologues in HITRAN\n')
    print('   M    I          id                  iso_name   abundance      mass        mol_name')
    for i in ISO:
        ab = ISO[i][ISO_INDEX['abundance']]
        ma = ISO[i][ISO_INDEX['mass']]
        ab = ab if ab else -1
        ma = ma if ma else -1
        print('%4i %4i     : %5i %25s %10f %10f %15s' % (i[0],i[1],ISO[i][ISO_INDEX['id']],ISO[i][ISO_INDEX['iso_name']],ab,ma,ISO[i][ISO_INDEX['mol_name']]))

def print_iso_id():
    print('The dictionary \"ISO_ID\" contains information on \"global\" IDs of isotopologues in HITRAN\n')
    print('   id            M    I                    iso_name       abundance       mass        mol_name')
    for i in ISO_ID:
        ab = ISO_ID[i][ISO_ID_INDEX['abundance']]
        ma = ISO_ID[i][ISO_ID_INDEX['mass']]
        ab = ab if ab else -1
        ma = ma if ma else -1
        print('%5i     :   %4i %4i   %25s %15.10f %10f %15s' % (i,ISO_ID[i][ISO_ID_INDEX['M']],ISO_ID[i][ISO_ID_INDEX['I']],ISO_ID[i][ISO_ID_INDEX['iso_name']],ab,ma,ISO_ID[i][ISO_ID_INDEX['mol_name']]))

profiles = 'profiles'
def print_profiles():
    print('Profiles available:')
    print('  HT        : PROFILE_HT')
    print('  SDRautian : PROFILE_SDRAUTIAN')
    print('  Rautian   : PROFILE_RAUTIAN')
    print('  SDVoigt   : PROFILE_SDVOIGT')
    print('  Voigt     : PROFILE_VOIGT')
    print('  Lorentz   : PROFILE_LORENTZ')
    print('  Doppler   : PROFILE_DOPPLER')

slit_functions = 'slit_functions'
def print_slit_functions():
    print('  RECTANGULAR : SLIT_RECTANGULAR')
    print('  TRIANGULAR  : SLIT_TRIANGULAR')
    print('  GAUSSIAN    : SLIT_GAUSSIAN')
    print('  DIFFRACTION : SLIT_DIFFRACTION')
    print('  MICHELSON   : SLIT_MICHELSON')
    print('  DISPERSION/LORENTZ : SLIT_DISPERSION')

tutorial='tutorial'
units='units'
index='index'
data='data'
spectra='spectra'
plotting='plotting'
python='python'

python_tutorial_text = \
"""
THIS TUTORIAL IS TAKEN FROM http://www.stavros.io/tutorials/python/
AUTHOR: Stavros Korokithakis


----- LEARN PYTHON IN 10 MINUTES -----


PRELIMINARY STUFF

So, you want to learn the Python programming language but can't find a concise 
and yet full-featured tutorial. This tutorial will attempt to teach you Python in 10 minutes. 
It's probably not so much a tutorial as it is a cross between a tutorial and a cheatsheet, 
so it will just show you some basic concepts to start you off. Obviously, if you want to 
really learn a language you need to program in it for a while. I will assume that you are 
already familiar with programming and will, therefore, skip most of the non-language-specific stuff. 
The important keywords will be highlighted so you can easily spot them. Also, pay attention because, 
due to the terseness of this tutorial, some things will be introduced directly in code and only 
briefly commented on.


PROPERTIES

Python is strongly typed (i.e. types are enforced), dynamically, implicitly typed (i.e. you don't 
have to declare variables), case sensitive (i.e. var and VAR are two different variables) and 
object-oriented (i.e. everything is an object). 


GETTING HELP

Help in Python is always available right in the interpreter. If you want to know how an object works, 
all you have to do is call help(<object>)! Also useful are dir(), which shows you all the object's methods, 
and <object>.__doc__, which shows you its documentation string: 

>>> help(5)
Help on int object:
(etc etc)

>>> dir(5)
['__abs__', '__add__', ...]

>>> abs.__doc__
'abs(number) -> number

Return the absolute value of the argument.'


SYNTAX

Python has no mandatory statement termination characters and blocks are specified by indentation. 
Indent to begin a block, dedent to end one. Statements that expect an indentation level end in a colon (:). 
Comments start with the pound (#) sign and are single-line, multi-line strings are used for multi-line comments. 
Values are assigned (in fact, objects are bound to names) with the _equals_ sign ("="), and equality testing is 
done using two _equals_ signs ("=="). You can increment/decrement values using the += and -= operators respectively 
by the right-hand amount. This works on many datatypes, strings included. You can also use multiple variables on one 
line. For example: 

>>> myvar = 3
>>> myvar += 2
>>> myvar
5

>>> myvar -= 1
>>> myvar
4

\"\"\"This is a multiline comment.
The following lines concatenate the two strings.\"\"\"

>>> mystring = "Hello"
>>> mystring += " world."
>>> print mystring
Hello world.

# This swaps the variables in one line(!).
# It doesn't violate strong typing because values aren't
# actually being assigned, but new objects are bound to
# the old names.
>>> myvar, mystring = mystring, myvar


DATA TYPES

The data structures available in python are lists, tuples and dictionaries. 
Sets are available in the sets library (but are built-in in Python 2.5 and later). 
Lists are like one-dimensional arrays (but you can also have lists of other lists), 
dictionaries are associative arrays (a.k.a. hash tables) and tuples are immutable 
one-dimensional arrays (Python "arrays" can be of any type, so you can mix e.g. integers, 
strings, etc in lists/dictionaries/tuples). The index of the first item in all array types is 0. 
Negative numbers count from the end towards the beginning, -1 is the last item. Variables 
can point to functions. The usage is as follows:

>>> sample = [1, ["another", "list"], ("a", "tuple")]
>>> mylist = ["List item 1", 2, 3.14]
>>> mylist[0] = "List item 1 again" # We're changing the item.
>>> mylist[-1] = 3.21 # Here, we refer to the last item.
>>> mydict = {"Key 1": "Value 1", 2: 3, "pi": 3.14}
>>> mydict["pi"] = 3.15 # This is how you change dictionary values.
>>> mytuple = (1, 2, 3)
>>> myfunction = len
>>> print myfunction(mylist)
3


You can access array ranges using a colon (:). Leaving the start index empty assumes the first item, 
leaving the end index assumes the last item. Negative indexes count from the last item backwards 
(thus -1 is the last item) like so:

>>> mylist = ["List item 1", 2, 3.14]
>>> print mylist[:]
['List item 1', 2, 3.1400000000000001]

>>> print mylist[0:2]
['List item 1', 2]

>>> print mylist[-3:-1]
['List item 1', 2]

>>> print mylist[1:]
[2, 3.14]

# Adding a third parameter, "step" will have Python step in
# N item increments, rather than 1.
# E.g., this will return the first item, then go to the third and
# return that (so, items 0 and 2 in 0-indexing).
>>> print mylist[::2]
['List item 1', 3.14]


STRINGS

Its strings can use either single or double quotation marks, and you can have quotation 
marks of one kind inside a string that uses the other kind (i.e. "He said 'hello'." is valid). 
Multiline strings are enclosed in _triple double (or single) quotes_ (\"\"\"). 
Python supports Unicode out of the box, using the syntax u"This is a unicode string". 
To fill a string with values, you use the % (modulo) operator and a tuple. 
Each %s gets replaced with an item from the tuple, left to right, and you can also use 
dictionary substitutions, like so:

>>>print "Name: %s\
Number: %s\
String: %s" % (myclass.name, 3, 3 * "-")

Name: Poromenos
Number: 3
String: ---

strString = \"\"\"This is
a multiline
string.\"\"\"

# WARNING: Watch out for the trailing s in "%(key)s".
>>> print "This %(verb)s a %(noun)s." % {"noun": "test", "verb": "is"}
This is a test.


FLOW CONTROL STATEMENTS

Flow control statements are if, for, and while. There is no select; instead, use if. 
Use for to enumerate through members of a list. To obtain a list of numbers, 
use range(<number>). These statements' syntax is thus:

rangelist = range(10)
>>> print rangelist
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

>>> for number in rangelist:
        # Check if number is one of
        # the numbers in the tuple.
        if number in (3, 4, 7, 9):
            # "Break" terminates a for without
            # executing the "else" clause.
            break
        else:
            # "Continue" starts the next iteration
            # of the loop. It's rather useless here,
            # as it's the last statement of the loop.
            continue
    else:
        # The "else" clause is optional and is
        # executed only if the loop didn't "break".
        pass # Do nothing

>>> if rangelist[1] == 2:
        print "The second item (lists are 0-based) is 2"
    elif rangelist[1] == 3:
        print "The second item (lists are 0-based) is 3"
    else:
        print "Dunno"

>>> while rangelist[1] == 1:
        pass


FUNCTIONS

Functions are declared with the "def" keyword. Optional arguments are set in 
the function declaration after the mandatory arguments by being assigned a default 
value. For named arguments, the name of the argument is assigned a value. 
Functions can return a tuple (and using tuple unpacking you can effectively return 
multiple values). Lambda functions are ad hoc functions that are comprised of 
a single statement. Parameters are passed by reference, but immutable types (tuples, 
ints, strings, etc) *cannot be changed*. This is because only the memory location of 
the item is passed, and binding another object to a variable discards the old one, 
so immutable types are replaced. For example:

# Same as def funcvar(x): return x + 1
>>> funcvar = lambda x: x + 1
>>> print funcvar(1)
2

# an_int and a_string are optional, they have default values
# if one is not passed (2 and "A default string", respectively).
>>> def passing_example(a_list, an_int=2, a_string="A default string"):
        a_list.append("A new item")
        an_int = 4
        return a_list, an_int, a_string

>>> my_list = [1, 2, 3]
>>> my_int = 10
>>> print passing_example(my_list, my_int)
([1, 2, 3, 'A new item'], 4, "A default string")

>>> my_list
[1, 2, 3, 'A new item']

>>> my_int
10


CLASSES

Python supports a limited form of multiple inheritance in classes. 
Private variables and methods can be declared (by convention, this is not enforced 
by the language) by adding at least two leading underscores and at most one trailing 
one (e.g. "__spam"). We can also bind arbitrary names to class instances. 
An example follows:

>>> class MyClass(object):
        common = 10
        def __init__(self):
            self.myvariable = 3
        def myfunction(self, arg1, arg2):
            return self.myvariable

# This is the class instantiation
>>> classinstance = MyClass()
>>> classinstance.myfunction(1, 2)
3

# This variable is shared by all classes.
>>> classinstance2 = MyClass()
>>> classinstance.common
10

>>> classinstance2.common
10

# Note how we use the class name
# instead of the instance.
>>> MyClass.common = 30
>>> classinstance.common
30

>>> classinstance2.common
30

# This will not update the variable on the class,
# instead it will bind a new object to the old
# variable name.
>>> classinstance.common = 10
>>> classinstance.common
10

>>> classinstance2.common
30

>>> MyClass.common = 50
# This has not changed, because "common" is
# now an instance variable.
>>> classinstance.common
10

>>> classinstance2.common
50

# This class inherits from MyClass. The example
# class above inherits from "object", which makes
# it what's called a "new-style class".
# Multiple inheritance is declared as:
# class OtherClass(MyClass1, MyClass2, MyClassN)
>>> class OtherClass(MyClass):
        # The "self" argument is passed automatically
        # and refers to the class instance, so you can set
        # instance variables as above, but from inside the class.
        def __init__(self, arg1):
            self.myvariable = 3
            print arg1

>>> classinstance = OtherClass("hello")
hello

>>> classinstance.myfunction(1, 2)
3

# This class doesn't have a .test member, but
# we can add one to the instance anyway. Note
# that this will only be a member of classinstance.
>>> classinstance.test = 10
>>> classinstance.test
10


EXCEPTIONS

Exceptions in Python are handled with try-except [exceptionname] blocks:

>>> def some_function():
        try:
            # Division by zero raises an exception
            10 / 0
        except ZeroDivisionError:
            print "Oops, invalid."
        else:
            # Exception didn't occur, we're good.
            pass
        finally:
            # This is executed after the code block is run
            # and all exceptions have been handled, even
            # if a new exception is raised while handling.
            print "We're done with that."

>>> some_function()
Oops, invalid.

We're done with that.


IMPORTING:

External libraries are used with the import [libname] keyword. 
You can also use from [libname] import [funcname] for individual functions. 
Here is an example:

>>> import random
>>> from time import clock

>>> randomint = random.randint(1, 100)
>>> print randomint
64


FILE I/O

Python has a wide array of libraries built in. As an example, here is how serializing 
(converting data structures to strings using the pickle library) with file I/O is used:

>>> import pickle
>>> mylist = ["This", "is", 4, 13327]
# Open the file C:\\binary.dat for writing. The letter r before the
# filename string is used to prevent backslash escaping.
>>> yfile = open(r"C:\\binary.dat", "w")
>>> pickle.dump(mylist, myfile)
>>> myfile.close()

>>> myfile = open(r"C:\\text.txt", "w")
>>> myfile.write("This is a sample string")
>>> myfile.close()

>>> myfile = open(r"C:\\text.txt")
>>> print myfile.read()
'This is a sample string'

>>> myfile.close()

# Open the file for reading.
>>> myfile = open(r"C:\\binary.dat")
>>> loadedlist = pickle.load(myfile)
>>> myfile.close()
>>> print loadedlist
['This', 'is', 4, 13327]


MISCELLANEOUS

    -> Conditions can be chained. 1 < a < 3 checks 
       that a is both less than 3 and greater than 1.
    -> You can use del to delete variables or items in arrays.
    -> List comprehensions provide a powerful way to create 
       and manipulate lists. They consist of an expression 
       followed by a for clause followed by zero or more 
       if or for clauses, like so:

>>> lst1 = [1, 2, 3]
>>> lst2 = [3, 4, 5]
>>> print [x * y for x in lst1 for y in lst2]
[3, 4, 5, 6, 8, 10, 9, 12, 15]

>>> print [x for x in lst1 if 4 > x > 1]
[2, 3]

# Check if a condition is true for any items.
# "any" returns true if any item in the list is true.
>>> any([i % 3 for i in [3, 3, 4, 4, 3]])
True

# This is because 4 % 3 = 1, and 1 is true, so any()
# returns True.

# Check for how many items a condition is true.
>>> sum(1 for i in [3, 3, 4, 4, 3] if i == 4)
2

>>> del lst1[0]
>>> print lst1
[2, 3]

>>> del lst1



    -> Global variables are declared outside of functions 
       and can be read without any special declarations, 
       but if you want to write to them you must declare them 
       at the beginning of the function with the "global" keyword, 
       otherwise Python will bind that object to a new local 
       variable (be careful of that, it's a small catch that can 
       get you if you don't know it). For example:

>>> number = 5

>>> def myfunc():
        # This will print 5.
        print number

>>> def anotherfunc():
        # This raises an exception because the variable has not
        # been bound before printing. Python knows that it an
        # object will be bound to it later and creates a new, local
        # object instead of accessing the global one.
        print number
        number = 3

>>> def yetanotherfunc():
        global number
        # This will correctly change the global.
        number = 3


EPILOGUE

This tutorial is not meant to be an exhaustive list of all (or even a subset) of Python. 
Python has a vast array of libraries and much much more functionality which you will 
have to discover through other means, such as the excellent book Dive into Python. 
I hope I have made your transition in Python easier. Please leave comments if you believe 
there is something that could be improved or added or if there is anything else 
you would like to see (classes, error handling, anything). 

"""
def print_python_tutorial():
    pydoc.pager(python_tutorial_text)

data_tutorial_text = \
"""

ACCESS YOUR DATA!

Welcome to tutorial on retrieving and processing the data from HITRANonline.


  ///////////////
 /// PREFACE ///
///////////////

HITRANonline API is a set of routines in Python which is aimed to 
provide a remote access to functionality and data given by a new project 
HITRANonline (http://hitranazure.cloudapp.net).

At the present moment the API can download, filter and process data on 
molecular and atomic line-by-line spectra which is provided by HITRANonline portal.

One of the major purposes of introducing API is extending a functionality 
of the main site, particularly providing a possibility to calculate several 
types of high- and low-resolution spectra based on a flexible HT lineshape. 

Each feature of API is represented by a Python function with a set of parameters 
providing a flexible approach to the task.


  ///////////////////////
 /// FEATURE SUMMARY ///
///////////////////////

1) Downloading line-by-line data from the HITRANonline site to local database.
2) Filtering and processing the data in SQL-like fashion.
3) Conventional Python structures (lists, tuples, dictionaries) for representing 
   a spectroscopic data.
4) Possibility to use a large set of third-party Python libraries to work with a data
5) Python implementation of an HT (Hartmann-Tran [1]) lineshape which is used in spectra.
   simulations. This lineshape can also be reduced to a number of conventional 
   line profiles such as Gaussian (Doppler), Lorentzian, Voigt, Rautian, 
   Speed-dependent Voigt and Rautian.
6) Python implementation of total internal partition sums (TIPS-2011 [2]) 
   which is used in spectra simulations.
7) High-resolution spectra simulation accounting pressure, 
   temperature and optical path length. The following spectral functions 
   can be calculated:
      a) absorption coefficient
      b) absorption spectrum
      c) transmittance spectrum
      d) radiance spectrum
8) Low-resolution spectra simulation using a number of apparatus functions.
9) Possibility to extend with the user's functionality by adding custom lineshapes, 
   partitions sums and apparatus functions.

References:

[1] N.H. Ngo, D. Lisak, H. Tran, J.-M. Hartmann.
    An isolated line-shape model to go beyond the Voigt profile in 
    spectroscopic databases and radiative transfer codes.
    JQSRT, Volume 129, November 2013, Pages 89–100
    http://dx.doi.org/10.1016/j.jqsrt.2013.05.034

[2] A. L. Laraia, R. R. Gamache, J. Lamouroux, I. E. Gordon, L. S. Rothman.
    Total internal partition sums to support planetary remote sensing.
    Icarus, Volume 215, Issue 1, September 2011, Pages 391–400
    http://dx.doi.org/10.1016/j.icarus.2011.06.004

_______________________________________________________________________


This tutorial will give you an insight of how to use HAPI for Python.

First, let's choose a folder for our local database. Every time you start
your Python project, you have to specify explicitly the name of the 
database folder.

>>> db_begin('data')

So, let's download some data from the server and do some processing on it.
Suppose that we want to get line by line data on the main isotopologue of H2O.

For retrieving the data to the local database, user have to specify the following parameters:
1) Name of the local table which will store the downloaded data.
2) Either a pair of molecule and isotopologue HITRAN numbers (M and I), 
   or a "global" isotopologue ID (iso_id).
3) Wavenumber range (nu_min and nu_max)

N.B. If you specify the name which already exists in the database, 
the existing table with that name will be overrided. 

To get additional information on function fetch,
call getHelp:

>>> getHelp(fetch)
...

To download the data, simply call the function "fetch".
This will establish a connection with the main server and get the data using
the parameters listed above:

>>> fetch('H2O',1,1,3400,4100)
BEGIN DOWNLOAD: H2O
  65536 bytes written to data/H2O.data
  65536 bytes written to data/H2O.data
  65536 bytes written to data/H2O.data
...
  65536 bytes written to data/H2O.data
  65536 bytes written to data/H2O.data
  65536 bytes written to data/H2O.data
Header written to data/H2O.header
END DOWNLOAD
                     Lines parsed: 7524
PROCESSED

The output is shown right after the console line ">>>".
To check the file that you've just downloaded you can open the database
folder. The new plain text file should have a name "H2O.data" and
it should contain line-by-line data in HITRAN format.

N.B. If we want several isotopologues in one table, we should
use fetch_by_ids instead of just fetch. Fetch_by_ids takes a "global" 
isotopologue ID numbers as an input instead of HITRAN's "local" identification.
See getHelp(fetch_by_ids) to get more information on this.

To get a list of tables which are already in the database,
use tableList() function (it takes no arguments):
>>> tableList()

To learn about the table we just downloaded, let's use a function "describeTable".

>>> describeTable('H2O')
-----------------------------------------
H2O summary:
-----------------------------------------
Comment: 
Contains lines for H2(16O)
 in 3400.000-4100.000 wavenumber range
Number of rows: 7524
Table type: column-fixed
-----------------------------------------
            PAR_NAME           PAR_FORMAT

            molec_id                  %2d
        local_iso_id                  %1d
                  nu               %12.6f
                  sw               %10.3E
                   a               %10.3E
           gamma_air                %5.4f
          gamma_self                %5.3f
              elower               %10.4f
               n_air                %4.2f
           delta_air                %8.6f
 global_upper_quanta                 %15s
 global_lower_quanta                 %15s
  local_upper_quanta                 %15s
  local_lower_quanta                 %15s
                ierr                  %6s
                iref                 %12s
    line_mixing_flag                  %1s
                  gp                %7.1f
                 gpp                %7.1f
-----------------------------------------

This output tells how many rows are currenty in the table H2O, which 
wavenumber range was used by fetch(). Also this gives a basic information 
about parameters stored in the table.

So, having the table downloaded, one can perform different operations on it
using API.

Here is a list of operations currently available with API:
1) FILTERING 
2) OUTPUTTING
3) SORTING
4) GROUPING


  ////////////////////////////////
 /// FILTERING AND OUTPUTTING ///
////////////////////////////////

The table data can be filtered with the help of select() function.

Use simple select() call to output the table content:

>>> select('H2O')
MI          nu         S         A gair gsel        E_nair    dair  ...
11 1000.288940 1.957E-24 2.335E-02.07100.350 1813.22270.680.008260  ...
11 1000.532321 2.190E-28 1.305E-05.04630.281 2144.04590.39-.011030  ...
...

This will display the list of line parameters containing in the table "H2O".

That's the simplest way of using the function select(). Full information
on control parameters can be obtained via getHelp(select) statement.

Suppose that we need a lines from a table within some wavenumber range. 
That's what filtering is for. Let's apply a simple range filter on a table.

>>> select('H2O',Conditions=('between','nu',4000,4100))
MI          nu         S         A gair gsel        E_nair    dair     
 11 4000.188800 1.513E-25 1.105E-02.03340.298 1581.33570.51-.013910 ...
 11 4000.204070 3.482E-24 8.479E-03.08600.454  586.47920.61-.007000 ...
 11 4000.469910 3.268E-23 1.627E+00.05410.375 1255.91150.56-.013050 ...
......

As a result of this operation, we see a list of lines of H2O table,
whose wavenumbers lie between 4000 cm-1 and 4100 cm-1.
The condition is taken as an input parameter to API function "select".

To specify a subset of columns to display, use another control parameter - 
ParameterNames:

>>> select('H2O',ParameterNames=('nu','sw'),Conditions=('between','nu',4000,4100))

The usage of ParameterNames is outlined below in the section "Specifying a list 
of parameters". So far it worth mentioning that this parameter is a part 
of a powerful tool for displaying and processing tables from database.

In the next section we will show how to create quieries 
with more complex conditions.


  ////////////////////////////
 /// FILTERING CONDITIONS ///
////////////////////////////

Let's analyze the last example of filtering. Condition input variable is
as follows:

                    ('between','nu',4000,4100)

Thus, this is a python list (or tuple), containing logical expressions
defined under column names of the table. For example, 'nu' is a name of 
the column in 'H2O' table, and this column contains a transition wavenumber.
The structure of a simple condition is as follows:

                    (OPERATION,ARG1,ARG2,...)
                    
Where OPERATION must be in a set of predefined operations (see below),
and ARG1,ARG2 etc. are the arguments for this operation.
Conditions can be nested, i.e. ARG can itself be a condition (see examples).
The following operations are available in select (case insensitive):


DESCRIPTION                   LITERAL                     EXAMPLE
---------------------------------------------------------------------------------
Range:               'RANGE','BETWEEN':         ('BETWEEN','nu',0,1000)
Subset:              'IN','SUBSET':             ('IN','local_iso_id',[1,2,3,4])
And:                 '&','&&','AND':            ('AND',('<','nu',1000),('>','nu',10))
Or:                  '|','||','OR':             ('OR',('>','nu',1000),('<','nu',10))
Not:                 '!','NOT':                 ('NOT',('IN','local_iso_id',[1,2,3]))
Less than:           '<','LESS','LT':                 ('<','nu',1000)
More than:           '>','MORE','MT':                 ('>','sw',1.0e-20)
Less or equal than:  '<=','LESSOREQUAL','LTE':        ('<=','local_iso_id',10)
More or equal than   '>=','MOREOREQUAL','MTE':        ('>=','sw',1e-20)
Equal:               '=','==','EQ','EQUAL','EQUALS':  ('<=','local_iso_id',10)
Not equal:           '!=','<>','~=','NE','NOTEQUAL':  ('!=','local_iso_id',1)
Summation:           '+','SUM':                 ('+','v1','v2','v3')
Difference:          '-','DIFF':                ('-','nu','elow')
Multiplication:      '*','MUL':                 ('*','sw',0.98)
Division:            '/','DIV':                 ('/','A',2)
Cast to string:      'STR','STRING':            ('STR','some_string')
Cast to Python list  'LIST':                    ('LIST',[1,2,3,4,5])
Match regexp         'MATCH','LIKE':            ('MATCH','\w+','some string')
Search single match: 'SEARCH':                  ('SEARCH','\d \d \d','1 2 3 4')
Search all matches:  'FINDALL':                 ('FINDALL','\d','1 2 3 4 5')
Count within group:  'COUNT' :                  ('COUNT','local_iso_id')
---------------------------------------------------------------------------------
   
Let's create a query with more complex condition. Suppese that we are 
interested in all lines between 3500 and 4000 with 1e-19 intensity cutoff.
The query will look like this:

>>> Cond = ('AND',('BETWEEN','nu',3500,4000),('>=','Sw',1e-19))
>>> select('H2O',Conditions=Cond,DestinationTableName='tmp')

Here, apart from other parameters, we have used a new parameter 
DestinationTableName. This parameter contains a name of the table
where we want to put a result of the query. Thus we have chosen 
a name 'tmp' for a new table.


  ////////////////////////////////////
 /// ACCESSING COLUMNS IN A TABLE ///
////////////////////////////////////

To get an access to particular table column (or columns) all we need
is to get a column from a table and put it to Python variable.

For this purpose, there exist two functions:

  getColumn(...)
  getColumns(...)

The first one returns just one column at a time. The second one returns
a list of solumns.

So, here are some examples of how to use both:

>>> nu1 = getColumn('H2O','nu')
>>> nu2,sw2 = getColumns('H2O',['nu','sw'])

N.B. If you don't remember exact names of columns in a particular table,
use describeTable to get an info on it's structure!


  ///////////////////////////////////////
 /// SPECIFYING A LIST OF PARAMETERS ///
///////////////////////////////////////

Suppose that we want not only select a set of parameters/columns
from a table, but do a certain transformations with them (for example,
multiply column on a coefficient, or add one column to another etc...).
We can make it in two ways. First, we can extract a column from table
using one of the functions (getColumn or getColumns) and do the rest 
in Python. The second way is to do it on the level of select.
The select function has a control parameter "ParameterNames", which 
makes it possible to specify parameters we want to be selected, 
and evaluate some simple arithmetic expressions with them.

Assume that we need only wavenumber and intensity from H2O table.
Also we need to scale an intensity to the unitary abundance. To do so,
we must divide an 'sw' parameter by it's natural abundance (0.99731) for 
principal isotopologue of water).

Thus, we have to select two columns:  
wavenumber (nu) and scaled intensity (sw/0.99731)
>>> select('H2O',)


  ////////////////////////////
 /// SAVING QUERY TO DISK ///
////////////////////////////

To quickly save a result of a query to disk, the user can take an 
advantage of an additional parameter "File".
If this parameter is presented in function call, then the query is 
saved to file with the name which was specified in "File".

For example, select all lines from H2O and save the result in file 'H2O.txt':
>>> select('H2O',File='H2O.txt')


  ////////////////////////////////////////////
 /// GETTING INFORMATION ON ISOTOPOLOGUES ///
////////////////////////////////////////////

API provides the following auxillary information about isotopologues
present in HITRAN. Corresponding functions use the standard HITRAN
molecule-isotopologue notation:

1) Natural abundances
>>> abundance(mol_id,iso_id)

2) Molecular masses
>>> molecularMass(mol_id,iso_id)

3) Molecule names
>>> moleculeName(mol_id,iso_id)

4) Isotopologue names
>>> isotopologueName(mol_id,iso_id)

5) ISO_ID
>>> getHelp(ISO_ID)

The latter is a dictionary, which contain all information about 
isotopologues concentrated in one place.

"""
def print_data_tutorial():
    pydoc.pager(data_tutorial_text)

spectra_tutorial_text = \
"""

CALCULATE YOUR SPECTRA!

Welcome to tutorial on calculating a spectra from line-by-line data.


  ///////////////
 /// PREFACE ///
///////////////

This tutorial will demonstrate how to use different lineshapes and partition
functions, and how to calculate synthetic spectra with respect to different 
instruments. It will be shown how to combine different parameters of spectral 
calculation to achieve better precision and performance for cross sections.

API provides a powerful tool to calculate cross-sections based on line-by-line
data containing in HITRAN. This features:

*) Python implementation of an HT (Hartmann-Tran [1]) lineshape which is used in 
   spectra simulations. This lineshape can also be reduced to a number of 
   conventional    line profiles such as Gaussian (Doppler), Lorentzian, Voigt, 
   Rautian, Speed-dependent Voigt and Rautian.
*) Python implementation of total internal partition sums (TIPS-2011 [2]) 
   which is used in spectra simulations.
*) High-resolution spectra simulation accounting pressure, 
   temperature and optical path length. The following spectral functions 
   can be calculated:
      a) absorption coefficient
      b) absorption spectrum
      c) transmittance spectrum
      d) radiance spectrum
*) Low-resolution spectra simulation using a number of apparatus functions.
*) Possibility to extend with the user's functionality by adding custom lineshapes, 
   partitions sums and apparatus functions.
*) An approach to function code is aimed to be flexible enough yet hopefully 
   intuitive.

References:

[1] N.H. Ngo, D. Lisak, H. Tran, J.-M. Hartmann.
    An isolated line-shape model to go beyond the Voigt profile in 
    spectroscopic databases and radiative transfer codes.
    JQSRT, Volume 129, November 2013, Pages 89–100
    http://dx.doi.org/10.1016/j.jqsrt.2013.05.034

[2] A. L. Laraia, R. R. Gamache, J. Lamouroux, I. E. Gordon, L. S. Rothman.
    Total internal partition sums to support planetary remote sensing.
    Icarus, Volume 215, Issue 1, September 2011, Pages 391–400
    http://dx.doi.org/10.1016/j.icarus.2011.06.004

            
  ///////////////////////////
 /// USING LINE PROFILES ///
///////////////////////////

Several lineshape (line profile) families are currently available:
1) Gaussian (Doppler) profile
2) Lorentzian profile
3) Voigt profile
4) Speed-dependent Voigt profile
5) Rautian profile
6) Speed-dependent Rautian profile
7) HT profile (Hartmann-Tran)

Each profile has it's own uniwue set of parameters. Normally one should
use profile parameters only in conjunction with their "native" profiles.

So, let's start exploring the available profiles using getHelp:
>>> getHelp(profiles)
Profiles available:
  HTP       : PROFILE_HT
  SDRautian : PROFILE_SDRAUTIAN
  Rautian   : PROFILE_RAUTIAN
  SDVoigt   : PROFILE_SDVOIGT
  Voigt     : PROFILE_VOIGT
  Lorentz   : PROFILE_LORENTZ
  Doppler   : PROFILE_DOPPLER

Output gives all available profiles. We can get additional info on each
of them just by calling getHelp(ProfileName):
>>> getHelp(PROFILE_HT)

Line profiles, adapted for using with HAPI, are written in Python and
heavily using the numerical library "Numpy". This means that the user
can calculate multiple values of particular profile at once having just
pasted a numpy array as a wavenumber grid (array). Let's give a short 
example of how to calculate HT profile on a numpy array.

>>> from numpy import arange
    w0 = 1000.
    GammaD = 0.005
    Gamma0 = 0.2
    Gamma2 = 0.01 * Gamma0
    Delta0 = 0.002
    Delta2 = 0.001 * Delta0
    nuVC = 0.2
    eta = 0.5
    Dw = 1.
    ww = arange(w0-Dw, w0+Dw, 0.01)  # GRID WITH THE STEP 0.01 
    l1 = PROFILE_HT(w0,GammaD,Gamma0,Gamma2,Delta0,Delta2,nuVC,eta,ww)[0]
    # now l1 contains values of HT profile calculates on the grid ww
    
On additional information about parameters see getHelp(PROFILE_HT).

It worth noting that PROFILE_HT returns 2 entities: real and imaginary part
of lineshape (as it described in the article given in preface). Apart from
HT, all other profiles return just one entity (the real part).


  ////////////////////////////
 /// USING PARTITION SUMS ///
////////////////////////////

As it was mentioned in the preface to this tutorial, the partition sums
are taken from the TIPS-2011 (the link is given above). Partition sums 
are taken for those isotopologues, which are present in HITRAN and in
TIPS-2011 simultaneousely.

N.B. Partition sums are omitted for the following isotopologues which
are in HITRAN at the moment:

ID       M     I         ISO                MOL
--------------------------------------------------
117      12    2     H(15N)(16O)3           HNO3
110      14    2     D(19F)                 HF
107      15    3     D(35Cl)                HCl
108      15    4     D(37Cl)                HCl
111      16    3     D(79Br)                HBr
112      16    4     D(81Br)                HBr
113      17    2     D(127I)                HI
118      22    2     (14N)(15N)             N2
119      29    2     (13C)(16O)(19F)2       COF2
 86      34    1     (16O)                  O
 92      39    1     (12C)H3(16O)H          CH3OH
114      47    1     (32S)(16O)3            SO3
--------------------------------------------------

The data on these isotopologues is not present in TIPS-2011 but is 
present in HITRAN. We're planning to add these molecules after TIPS-2013
is released.

To calculate a partition sum for most of the isotopologues in HITRAN,
we will use a function partitionSum (use getHelp for detailed info).
Let's just mention that 
The syntax is as follows: partitionSum(M,I,T), where M,I - standard 
HITRAN molecule-isotopologue notation, T - definition of temperature
range.

Usecase 1: temperatuer is defined by a list:
>>> Q = partitionSum(1,1,[70,80,90])

Usecase 2: temperature is defined by bounds and the step:
>>> T,Q = partiionSum(1,1,[70,3000],step=1.0)

In the latter example we calculate a partition sum on a range of
temperatures from 70K to 3000K using a step 1.0 K, and having arrays 
of temperature (T) and partition sum (Q) at the output.


  ///////////////////////////////////////////
 /// CALCULATING ABSORPTION COEFFICIENTS ///
///////////////////////////////////////////

Currently API can calculate the following spectral function at arbitrary
thermodynamic parameters:

1) Absorption coefficient
2) Absorption spectrum
3) Transmittance spectrum
4) Radiance spectrum

All these functions can be calculated with or without accounting of 
an instrument properties (apparatus function, resolution, path length etc...)

As it well known, the spectral functions such as absorption,
transmittance, and radiance spectra, are calculated on the basis
of the absorption coefficient. By that resaon, absorption coefficient
is the most important part of simulating a cross section. This part of
tutorial is devoted to demonstration how to calculate absorption 
coefficient from the HITRAN line-by-line data. Here we give a brief 
insight on basic parameters of calculation procedure, talk about some 
useful practices and precautions.

To calculate an absorption coefficient, we can use one of the following
functions:

-> absorptionCoefficient_HT
-> absorptionCoefficient_Voigt
-> absorptionCoefficient_Lorentz
-> absorptionCoefficient_Doppler

Each of these function calculates cross sections using different
lineshapes (the names a quite self-explanatory).
You can get detailed information on using each of these functions
by calling getHelp(function_name).

Let's look more closely to the cross sections based on the Lorentz profile.
For doing that, let's have a table downloaded from HITRANonline.

# get data on CO2 main isotopologue in the range 2000-2100 cm-1
>>> fetch('CO2',2,1,2000,2100)

OK, now we're ready to run a fast example of how to calculate an
absorption coefficient cross section:

>>> nu,coef = absorptionCoefficient_Lorentz(SourceTables='CO2')

This example calculates a Lorentz cross section using the whole set of 
lines in the "co2" table. This is the simplest possible way to use these
functions, because major part of parameters bound to their default values.

If we have matplotlib installed, then we can visualize it using a plotter:
>>> from pylab import plot
>>> plot(nu,coef) 

API provides a flexible control over a calculation procedure. This control
can be achieved by using a number of input parameters. So, let's dig 
into the depth of the settings.

The input parameters of absorptionCoefficient_Lorentz are as follows:

Name                          Default value
-------------------------------------------------------------------
SourceTables                  '__BUFFER__'
Components                    All isotopologues in SourceTables 
partitionFunction             PYTIPS
Environment                   {'T':296.,'p':1.}
WavenumberRange               depends on Components
WavenumberStep                0.01 cm-1
WavenumberWing                10 cm-1
WavenumberWingHW              50 HWHMs
IntensityThreshold            0 cm/molec
GammaL                        'gamma_air'
HITRAN_units                  True 
File                          None
Format                        '%e %e'
-------------------------------------------------------------------

Newt we'll give a brief explanation for each parameter. After each description
we'll make some notes about the usage of the correspondent parameter.


SourceTables:     (required parameter)
   
  List of source tables to take line-by-line data from.
  NOTE: User must provide at least one table in the list.

Components:    (optional parameter)

  List of tuples (M,I,D) to consider in cross section calculation.
  M here is a molecule number, I is an isotopologue number, 
  D is an abundance of the component.
  NOTE: If this input contains more than one tuple, then the output 
        is an absorption coefficient for mixture of corresponding gases.
  NOTE2: If omitted, then all data from the source tables is involved.

partitionFunction:    (optional parameter)

  Instance of partition function of the following format:
  Func(M,I,T), where Func - numae of function, (M,I) - HITRAN numbers
  for molecule and isotopologue, T - temperature.
  Function must return only one output - value of partition sum.
  NOTE: Deafult value is PYTIPS - python version of TIPS-2011

Environment:    (optional parameter)

  Python dictionary containing value of pressure and temperature.
  The format is as follows: Environment = {'p':pval,'T':tval}, 
  where "pval" and "tval" are corresponding values in atm and K 
  respectively.
  NOTE: Default value is {'p':1.0,'T':296.0}

WavenumberRange:    (optional parameter)

  List containing minimum and maximum value of wavenumber to consider
  in cross-section calculation. All lines that are out of htese bounds
  will be skipped. The firmat is as follows: WavenumberRange=[wn_low,wn_high]
  NOTE: If this parameter os skipped, then min and max are taken 
  from the data from SourceTables. Deprecated name is OmegaRange.

WavenumberStep:    (optional parameter)

  Value for the wavenumber step. 
  NOTE: Default value is 0.01 cm-1.
  NOTE2: Normally user would want to take the step under 0.001 when
         calculating absorption coefficient with Doppler profile 
         because of very narrow spectral lines. Deprecated name is OmegaStep.

WavenumberWing:    (optional parameter)

  Absolute value of the line wing in cm-1, i.e. distance from the center 
  of each line to the most far point where the profile is considered 
  to be non zero. Deprecated name is OmegaStep.
  NOTE: if omitted, then only OmegaWingHW is taken into account.

WavenumberWingHW:    (optional parameter)

  Relative value of the line wing in halfwidths. Deprecated name is OmegaWingHW.
  NOTE: The resulting wing is a maximum value from both OmegaWing and
  OmegaWingHW.

IntensityThreshold:    (optional parameter)

  Absolute value of minimum intensity in cm/molec to consider.
  NOTE: default value is 0.

GammaL:    (optional parameter)

  This is the name of broadening parameter to consider a "Lorentzian"
  part in the Voigt profile. In the current 160-char format there is 
  a choise between "gamma_air" and "gamma_self".
  NOTE: If the table has custom columns with a broadening coefficients,
        the user can specify the name of this column in GammaL. This
        would let the function calculate an absorption with custom
        broadening parameter.

HITRAN_units:    (optional parameter)

  Logical flag for units, in which the absorption coefficient shoould be 
  calculated. Currently, the choises are: cm^2/molec (if True) and
  cm-1 (if False).
  NOTE: to calculate other spectral functions like transmitance,
  radiance and absorption spectra, user should set HITRAN_units to False.

File:    (optional parameter)

  The name of the file to save the calculated absorption coefficient.
  The file is saved only if this parameter is specified.

Format:    (optional parameter)

  C-style format for the text data to be saved. Default value is "%e %e".
  NOTE: C-style output format specification (which are mostly valid for Python) 
        can be found, for instance, by the link: 
  http://www.gnu.org/software/libc/manual/html_node/Formatted-Output.html


N.B. Other functions such as absorptionCoefficient_Voigt(_HT,_Doppler) have
identical parameter sets so the description is the same for each function.


  ///////////////////////////////////////////////////////////////////
 /// CALCULATING ABSORPTION, TRANSMITTANCE, AND RADIANCE SPECTRA ///
///////////////////////////////////////////////////////////////////

Let's calculate an absorption, transmittance, and radiance
spectra on the basis of apsorption coefficient. In order to be consistent
with internal API's units, we need to have an absorption coefficient cm-1:

>>> nu,coef = absorptionCoefficient_Lorentz(SourceTables='CO2',HITRAN_units=False)

To calculate absorption spectrum, use the function absorptionSpectrum():
>>> nu,absorp = absorptionSpectrum(nu,coef) 

To calculate transmittance spectrum, use function transmittanceSpectrum():
>>> nu,trans = transmittanceSpectrum(nu,coef) 

To calculate radiance spectrum, use function radianceSpectrum():
>>> nu,radi = radianceSpectrum(nu,coef) 


The last three commands used a default path length (1 m).
To see complete info on all three functions, look for section
"calculating spectra" in getHelp()

Generally, all these three functions use similar set of parameters:

Wavenumber:       (required parameter) 

  Wavenumber grid to for spectrum. Deprecated name is Omegas.

AbsorptionCoefficient        (optional parameter)

  Absorption coefficient as input.

Environment={'T': 296.0, 'l': 100.0}       (optional parameter) 

  Environmental parameters for calculating  spectrum.
  This parameter is a bit specific for each of functions:
  For absorptionSpectrum() and transmittanceSpectrum() the default
  value is as follows: Environment={'l': 100.0}
  For transmittanceSpectrum() the default value, besides path length,
  contains a temperature: Environment={'T': 296.0, 'l': 100.0}
  NOTE: temperature must be equal to that which was used in 
  absorptionCoefficient_ routine!

File         (optional parameter)

  Filename of output file for calculated spectrum.
  If omitted, then the file is not created.

Format        (optional parameter)

  C-style format for spectra output file.
  NOTE: Default value is as follows: Format='%e %e'


  ///////////////////////////////////////
 /// APPLYING INSTRUMENTAL FUNCTIONS ///
///////////////////////////////////////

For comparison of the theoretical spectra with the real-world 
instruments output it's necessary to take into account instrumental resolution.
For this purpose HAPI has a function convolveSpectrum() which can emulate
spectra with lower resolution using custom instrumental functions.

The following instrumental functions are available:
1) Rectangular
2) Triangular
3) Gaussian
4) Diffraction
5) Michelson
6) Dispersion
7) Lorentz

To get a description of each instrumental function we can use getHelp():
>>> getHelp(slit_functions)
  RECTANGULAR : SLIT_RECTANGULAR
  TRIANGULAR  : SLIT_TRIANGULAR
  GAUSSIAN    : SLIT_GAUSSIAN
  DIFFRACTION : SLIT_DIFFRACTION
  MICHELSON   : SLIT_MICHELSON
  DISPERSION/LORENTZ : SLIT_DISPERSION
  
For instance,
>>> getHelp(SLIT_MICHELSON)
... will give a datailed info about Michelson's instrumental function.


The function convolveSpectrum() convolutes a high-resulution spectrum
with one of supplied instrumental (slit) functions. The folowing 
parameters of this function are provided:

Wavenumber     (required parameter)
  
  Array of wavenumbers in high-resolution input spectrum.
  Deprecated name is Omega.

CrossSection     (required parameter)

  Values of high-resolution input spectrum.

Resolution     (optional parameter)

  This parameter is passed to the slit function. It represents
  the resolution of corresponding instrument.
  NOTE: default value is 0.1 cm-1

AF_wing     (optional parameter)

  Width of an instrument function where it is considered non-zero.
  NOTE: default value is 10.0 cm-1

SlitFunction     (optional parameter)

  Custom instrumental function to convolve with spectrum.
  Format of the instrumental function must be as follows:
  Func(x,g), where Func - function name, x - wavenumber,
  g - resolution.
  NOTE: if omitted, then the default value is SLIT_RECTANGULAR


Before using the convolution procedure it worth giving some practical 
advices and remarks: 
1) Quality of a convolution depends on many things: quality of calculated 
spectra, width of AF_wing and WavenumberRange, Resolution, WavenumberStep etc ...
Most of these factors are taken from previus stages of spectral calculation.
Right choise of all these factors is crucial for the correct computation.
2) Dispersion, Diffraction and Michelson AF's don't work well in narrow 
wavenumber range because of their broad wings.
3) Generally one must consider WavenumberRange and AF_wing as wide as possible.
4) After applying a convolution, the resulting spectral range for 
the lower-resolution spectra is reduced by the doubled value of AF_wing.
For this reason, try to make an initial spectral range for high-resolution
spectrum (absorption, transmittance, radiance) sufficiently broad.

The following command will calculate a lower-resolution spectra from 
the CO2 transmittance, which was calculated in a previous section. 
The Spectral resolution is 1 cm-1, 

>>> nu_,trans_,i1,i2,slit = convolveSpectrum(nu,trans)

The outputs are: 

nu_, trans_ - wavenumbers and transmittance for the resulting 
              low-resolution spectrum.

i1,i2 - indexes for initial nu,trans spectrum denoting the part of 
        wavenumber range which was taken for lower resolution spectrum.
        => Low-res spectrum is calculated on nu[i1:i2]

Note, than to achieve more flexibility, one have to specify most of 
the optional parameters. For instance, more complete call is as follows:
>>> nu_,trans_,i1,i2,slit = convolveSpectrum(nu,trans,SlitFunction=SLIT_MICHELSON,Resolution=1.0,AF_wing=20.0)

"""
def print_spectra_tutorial():
    pydoc.pager(spectra_tutorial_text)

plotting_tutorial_text = \
"""

PLOTTING THE SPECTRA WITH MATPLOTLIB

This tutorial briefly explains how to make plots using
the Matplotlib - Python library for plotting.

Prerequisites:
   To tun through this tutorial, user must have the following
   Python libraries installed:
   1) Matplotlib
       Matplotlib can be obtained by the link http://matplotlib.org/ 
   2) Numpy  (required by HAPI itself)
       Numpy can be obtained via pip:  
          sudo pip install numpy (under Linux and Mac)
          pip install numpy (under Windows)
       Or by the link http://www.numpy.org/
       
As an option, user can download one of the many scientific Python
distributions, such as Anaconda, Canopy etc...

So, let's calculate plot the basic entities which ar provided by HAPI.
To do so, we will do all necessary steps to download, filter and 
calculate cross sections "from scratch". To demonstrate the different
possibilities of matplotlib, we will mostly use Pylab - a part of 
Matplotlib with the interface similar to Matlab. Please note, that it's 
not the only way to use Matplotlib. More information can be found on it's site.

The next part is a step-by-step guide, demonstrating basic possilities
of HITRANonline API in conjunction with Matplotlib.

First, do some preliminary imports:
>>> from hapi import *
>>> from pylab import show,plot,subplot,xlim,ylim,title,legend,xlabel,ylabel,hold

Start the database 'data':
>>> db_begin('data') 

Download lines for main isotopologue of ozone in [3900,4050] range:
>>> fetch('O3',3,1,3900,4050)

PLot a sick spectrum using the function getStickXY()
>>> x,y = getStickXY('O3')
>>> plot(x,y); show()

Zoom in spectral region [4020,4035] cm-1:
>>> plot(x,y); xlim([4020,4035]); show()

Calculate and plot difference between Voigt and Lorentzian lineshape:
>>> wn = arange(3002,3008,0.01) # get wavenumber range of interest
>>> voi = PROFILE_VOIGT(3005,0.1,0.3,wn)[0]   # calc Voigt
>>> lor = PROFILE_LORENTZ(3005,0.3,wn)   # calc Lorentz
>>> diff = voi-lor    # calc difference
>>> subplot(2,1,1)   # upper panel
>>> plot(wn,voi,'red',wn,lor,'blue')  # plot both profiles
>>> legend(['Voigt','Lorentz'])   # show legend
>>> title('Voigt and Lorentz profiles')   # show title
>>> subplot(2,1,2)   # lower panel
>>> plot(wn,diff)   # plot diffenence
>>> title('Voigt-Lorentz residual')   # show title
>>> show()   # show all figures

Calculate and plot absorption coefficients for ozone using Voigt 
profile. Spectra are calculated for 4 cases of thermodynamic parameters: 
(1 atm, 296 K), (5 atm, 296 K), (1 atm, 500 K), and (5 atm, 500 K)
>>> nu1,coef1 = absorptionCoefficient_Voigt(((3,1),),'O3',
        WavenumberStep=0.01,HITRAN_units=False,GammaL='gamma_self',
        Environment={'p':1,'T':296.})
>>> nu2,coef2 = absorptionCoefficient_Voigt(((3,1),),'O3',
        WavenumberStep=0.01,HITRAN_units=False,GammaL='gamma_self',
        Environment={'p':5,'T':296.})
>>> nu3,coef3 = absorptionCoefficient_Voigt(((3,1),),'O3',
        WavenumberStep=0.01,HITRAN_units=False,GammaL='gamma_self',
        Environment={'p':1,'T':500.})
>>> nu4,coef4 = absorptionCoefficient_Voigt(((3,1),),'O3',
        WavenumberStep=0.01,HITRAN_units=False,GammaL='gamma_self',
        Environment={'p':5,'T':500.})
>>> subplot(2,2,1); plot(nu1,coef1); title('O3 k(w): p=1 atm, T=296K')
>>> subplot(2,2,2); plot(nu2,coef2); title('O3 k(w): p=5 atm, T=296K')
>>> subplot(2,2,3); plot(nu3,coef3); title('O3 k(w): p=1 atm, T=500K')
>>> subplot(2,2,4); plot(nu4,coef4); title('O3 k(w): p=5 atm, T=500K')
>>> show()

Calculate and plot absorption, transmittance and radiance spectra for 1 atm 
and 296K. Path length is set to 10 m.
>>> nu,absorp = absorptionSpectrum(nu1,coef1,Environment={'l':1000.})
>>> nu,transm = transmittanceSpectrum(nu1,coef1,Environment={'l':1000.})
>>> nu,radian = radianceSpectrum(nu1,coef1,Environment={'l':1000.,'T':296.})
>>> subplot(2,2,1); plot(nu1,coef1,'r'); title('O3 k(w): p=1 atm, T=296K')
>>> subplot(2,2,2); plot(nu,absorp,'g'); title('O3 absorption: p=1 atm, T=296K')
>>> subplot(2,2,3); plot(nu,transm,'b'); title('O3 transmittance: p=1 atm, T=296K')
>>> subplot(2,2,4); plot(nu,radian,'y'); title('O3 radiance: p=1 atm, T=296K')
>>> show()

Calculate and compare high resolution spectrum for O3 with lower resolution
spectrum convoluted with an instrumental function of ideal Michelson interferometer.
>>> nu_,trans_,i1,i2,slit = convolveSpectrum(nu,transm,SlitFunction=SLIT_MICHELSON,Resolution=1.0,AF_wing=20.0)
>>> plot(nu,transm,'red',nu_,trans_,'blue'); legend(['HI-RES','Michelson']); show()

"""
def print_plotting_tutorial():
    pydoc.pager(plotting_tutorial_text)

def getHelp(arg=None):
    """
    This function provides interactive manuals and tutorials.
    """
    if arg==None:
        print('--------------------------------------------------------------')
        print('Hello, this is an interactive help system of HITRANonline API.')
        print('--------------------------------------------------------------')
        print('Run getHelp(.) with one of the following arguments:')
        print('    tutorial  -  interactive tutorials on HAPI')
        print('    units     -  units used in calculations')
        print('    index     -  index of available HAPI functions')
    elif arg=='tutorial':
        print('-----------------------------------')
        print('This is a tutorial section of help.')
        print('-----------------------------------')
        print('Please choose the subject of tutorial:')
        print('    data      -  downloading the data and working with it')
        print('    spectra   -  calculating spectral functions')
        print('    plotting  -  visualizing data with matplotlib')
        print('    python    -  Python quick start guide')
    elif arg=='python':
        print_python_tutorial()
    elif arg=='data':
        print_data_tutorial()
    elif arg=='spectra':
        print_spectra_tutorial()
    elif arg=='plotting':
        print_plotting_tutorial()
    elif arg=='index':
        print('------------------------------')
        print('FETCHING DATA:')
        print('------------------------------')
        print('  fetch')
        print('  fetch_by_ids')
        print('')
        print('------------------------------')
        print('WORKING WITH DATA:')
        print('------------------------------')
        print('  db_begin')
        print('  db_commit')
        print('  tableList')
        print('  describe')
        print('  select')
        print('  sort')
        print('  extractColumns')
        print('  getColumn')
        print('  getColumns')
        print('  dropTable')
        print('')
        print('------------------------------')
        print('CALCULATING SPECTRA:')
        print('------------------------------')
        print('  profiles')
        print('  partitionSum')
        print('  absorptionCoefficient_HT')
        print('  absorptionCoefficient_Voigt')
        print('  absorptionCoefficient_SDVoigt')
        print('  absorptionCoefficient_Lorentz')
        print('  absorptionCoefficient_Doppler')
        print('  transmittanceSpectrum')
        print('  absorptionSpectrum')
        print('  radianceSpectrum')
        print('')
        print('------------------------------')
        print('CONVOLVING SPECTRA:')
        print('------------------------------')
        print('  convolveSpectrum')
        print('  slit_functions')
        print('')
        print('------------------------------')
        print('INFO ON ISOTOPOLOGUES:')
        print('------------------------------')
        print('  ISO_ID')
        print('  abundance')
        print('  molecularMass')
        print('  moleculeName')
        print('  isotopologueName')
        print('')
        print('------------------------------')
        print('MISCELLANEOUS:')
        print('------------------------------')
        print('  getStickXY')
        print('  read_hotw')
    elif arg == ISO:
        print_iso()
    elif arg == ISO_ID:
        print_iso_id()
    elif arg == profiles:
        print_profiles()
    elif arg == slit_functions:
        print_slit_functions()
    else:
       help(arg)

    

# Get atmospheric (natural) abundance
# for a specified isotopologue
# M - molecule number
# I - isotopologue number
def abundance(M,I):
    """
    INPUT PARAMETERS: 
        M: HITRAN molecule number
        I: HITRAN isotopologue number
    OUTPUT PARAMETERS: 
        Abbundance: natural abundance
    ---
    DESCRIPTION:
        Return natural (Earth) abundance of HITRAN isotolopogue.
    ---
    EXAMPLE OF USAGE:
        ab = abundance(1,1) # H2O
    ---
    """
    return ISO[(M,I)][ISO_INDEX['abundance']]

# Get molecular mass
# for a specified isotopologue
# M - molecule number
# I - isotopologue number
def molecularMass(M,I):
    """
    INPUT PARAMETERS: 
        M: HITRAN molecule number
        I: HITRAN isotopologue number
    OUTPUT PARAMETERS: 
        MolMass: molecular mass
    ---
    DESCRIPTION:
        Return molecular mass of HITRAN isotolopogue.
    ---
    EXAMPLE OF USAGE:
        mass = molecularMass(1,1) # H2O
    ---
    """
    return ISO[(M,I)][ISO_INDEX['mass']]

# Get molecule name
# for a specified isotopologue
# M - molecule number
# I - isotopologue number
def moleculeName(M):
    """
    INPUT PARAMETERS: 
        M: HITRAN molecule number
    OUTPUT PARAMETERS: 
        MolName: molecular name
    ---
    DESCRIPTION:
        Return name of HITRAN molecule.
    ---
    EXAMPLE OF USAGE:
        molname = moleculeName(1) # H2O
    ---
    """
    return ISO[(M,1)][ISO_INDEX['mol_name']]

# Get isotopologue name
# for a specified isotopologue
# M - molecule number
# I - isotopologue number
def isotopologueName(M,I):
    """
    INPUT PARAMETERS: 
        M: HITRAN molecule number
        I: HITRAN isotopologue number
    OUTPUT PARAMETERS: 
        IsoMass: isotopologue mass
    ---
    DESCRIPTION:
        Return name of HITRAN isotolopogue.
    ---
    EXAMPLE OF USAGE:
        isoname = isotopologueName(1,1) # H2O
    ---
    """
    return ISO[(M,I)][ISO_INDEX['iso_name']]

# ----------------------- table list ----------------------------------
def tableList():
    """
    INPUT PARAMETERS: 
        none
    OUTPUT PARAMETERS: 
        TableList: a list of available tables
    ---
    DESCRIPTION:
        Return a list of tables present in database.
    ---
    EXAMPLE OF USAGE:
        lst = tableList()
    ---
    """

    return getTableList()

# ----------------------- describe ----------------------------------
def describe(TableName):
    """
    INPUT PARAMETERS: 
        TableName: name of the table to describe
    OUTPUT PARAMETERS: 
        none
    ---
    DESCRIPTION:
        Print information about table, including 
        parameter names, formats and wavenumber range.
    ---
    EXAMPLE OF USAGE:
        describe('sampletab')
    ---
    """
    describeTable(TableName)

# ---------------------- /ISO.PY ---------------------------------------

def db_begin(db=None):
    """
    INPUT PARAMETERS: 
        db: database name (optional)
    OUTPUT PARAMETERS: 
        none
    ---
    DESCRIPTION:
        Open a database connection. A database is stored 
        in a folder given in db input parameter.
        Default=data
    ---
    EXAMPLE OF USAGE:
        db_begin('bar')
    ---
    """
    databaseBegin(db)

def db_commit():
    """
    INPUT PARAMETERS: 
        none
    OUTPUT PARAMETERS: 
        none
    ---
    DESCRIPTION:
        Commit all changes made to opened database.
        All tables will be saved in corresponding files.
    ---
    EXAMPLE OF USAGE:
        db_commit()
    ---
    """
    databaseCommit()

# ------------------ QUERY HITRAN ---------------------------------------

def comment(TableName,Comment):
    LOCAL_TABLE_CACHE[TableName]['header']['comment'] = Comment

def fetch_by_ids(TableName,iso_id_list,numin,numax,ParameterGroups=[],Parameters=[]):
    """
    INPUT PARAMETERS: 
        TableName:   local table name to fetch in (required)
        iso_id_list: list of isotopologue id's    (required)
        numin:       lower wavenumber bound       (required)
        numax:       upper wavenumber bound       (required)
    OUTPUT PARAMETERS: 
        none
    ---
    DESCRIPTION:
        Download line-by-line data from HITRANonline server
        and save it to local table. The input parameter iso_id_list
        contains list of "global" isotopologue Ids (see help on ISO_ID).
        Note: this function is required if user wants to download
        multiple species into single table.
    ---
    EXAMPLE OF USAGE:
        fetch_by_ids('water',[1,2,3,4],4000,4100)
    ---
    """
    if type(iso_id_list) not in set([list,tuple]):
       iso_id_list = [iso_id_list]
    queryHITRAN(TableName,iso_id_list,numin,numax,
                pargroups=ParameterGroups,params=Parameters)
    iso_names = [ISO_ID[i][ISO_ID_INDEX['iso_name']] for i in iso_id_list]
    Comment = 'Contains lines for '+','.join(iso_names)
    Comment += ('\n in %.3f-%.3f wavenumber range' % (numin,numax))
    comment(TableName,Comment)

#def queryHITRAN(TableName,iso_id_list,numin,numax):
def fetch(TableName,M,I,numin,numax,ParameterGroups=[],Parameters=[]):
    """
    INPUT PARAMETERS: 
        TableName:   local table name to fetch in (required)
        M:           HITRAN molecule number       (required)
        I:           HITRAN isotopologue number   (required)
        numin:       lower wavenumber bound       (required)
        numax:       upper wavenumber bound       (required)
    OUTPUT PARAMETERS: 
        none
    ---
    DESCRIPTION:
        Download line-by-line data from HITRANonline server
        and save it to local table. The input parameters M and I
        are the HITRAN molecule and isotopologue numbers.
        This function results in a table containing single 
        isotopologue specie. To have multiple species in a 
        single table use fetch_by_ids instead.
    ---
    EXAMPLE OF USAGE:
        fetch('HOH',1,1,4000,4100)
    ---
    """
    queryHITRAN(TableName,[ISO[(M,I)][ISO_INDEX['id']]],numin,numax,
                pargroups=ParameterGroups,params=Parameters)
    iso_name = ISO[(M,I)][ISO_INDEX['iso_name']]
    Comment = 'Contains lines for '+iso_name
    Comment += ('\n in %.3f-%.3f wavenumber range' % (numin,numax))
    comment(TableName,Comment)



# ------------------ LINESHAPES -----------------------------------------

# ------------------ complex probability function -----------------------
# define static data
zone = __ComplexType__(1.0e0 + 0.0e0j)
zi = __ComplexType__(0.0e0 + 1.0e0j)
tt = __FloatType__([0.5e0,1.5e0,2.5e0,3.5e0,4.5e0,5.5e0,6.5e0,7.5e0,8.5e0,9.5e0,10.5e0,11.5e0,12.5e0,13.5e0,14.5e0])
pipwoeronehalf = __FloatType__(0.564189583547756e0)

# "naive" implementation for benchmarks
def cpf3(X,Y):

    # X,Y,WR,WI - numpy arrays
    if type(X) != ndarray: 
        if type(X) not in set([list,tuple]): 
            X = array([X])
        else:
            X = array(X)
    if type(Y) != ndarray: 
        if type(Y) not in set([list,tuple]): 
            Y = array([Y])
        else:
            Y = array(Y)

    zm1 = zone/__ComplexType__(X + zi*Y) # maybe redundant
    zm2 = zm1**2
    zsum = zone
    zterm=zone

    for tt_i in tt:
        zterm *= zm2*tt_i
        zsum += zterm
    
    zsum *= zi*zm1*pipwoeronehalf
    
    return zsum.real, zsum.imag

T = __FloatType__([0.314240376e0,0.947788391e0,1.59768264e0,2.27950708e0,3.02063703e0,3.8897249e0])
U = __FloatType__([1.01172805e0,-0.75197147e0,1.2557727e-2,1.00220082e-2,-2.42068135e-4,5.00848061e-7])
S = __FloatType__([1.393237e0,0.231152406e0,-0.155351466e0,6.21836624e-3,9.19082986e-5,-6.27525958e-7])

# Complex probability function implementation (Humlicek)
def cpf(X,Y):

    # X,Y,WR,WI - numpy arrays
    if type(X) != ndarray: 
        if type(X) not in set([list,tuple]): 
            X = array([X])
        else:
            X = array(X)
    if type(Y) != ndarray: 
        if type(Y) not in set([list,tuple]): 
            Y = array([Y])
        else:
            Y = array(Y)
    
    # REGION3
    index_REGION3 = where(sqrt(X**2 + Y**2) > __FloatType__(8.0e0))
    X_REGION3 = X[index_REGION3]
    Y_REGION3 = Y[index_REGION3]
    zm1 = zone/__ComplexType__(X_REGION3 + zi*Y_REGION3)
    zm2 = zm1**2
    zsum_REGION3 = zone
    zterm=zone
    for tt_i in tt:
        zterm *= zm2*tt_i
        zsum_REGION3 += zterm
    zsum_REGION3 *= zi*zm1*pipwoeronehalf
    
    index_REGION12 = setdiff1d(array(arange(len(X))),array(index_REGION3))
    X_REGION12 = X[index_REGION12]
    Y_REGION12 = Y[index_REGION12]
    
    WR = __FloatType__(0.0e0)
    WI = __FloatType__(0.0e0)
    
    # REGION12
    Y1_REGION12 = Y_REGION12 + __FloatType__(1.5e0)
    Y2_REGION12 = Y1_REGION12**2

    # REGION2    
    subindex_REGION2 = where((Y_REGION12 <= 0.85e0) & 
                             (abs(X_REGION12) >= (18.1e0*Y_REGION12 + 1.65e0)))
    
    index_REGION2 = index_REGION12[subindex_REGION2]
    
    X_REGION2 = X[index_REGION2]
    Y_REGION2 = Y[index_REGION2]
    Y1_REGION2 = Y1_REGION12[subindex_REGION2]
    Y2_REGION2 = Y2_REGION12[subindex_REGION2]
    Y3_REGION2 = Y_REGION2 + __FloatType__(3.0e0)
    
    WR_REGION2 = WR
    WI_REGION2 = WI

    WR_REGION2 = zeros(len(X_REGION2))
    ii = abs(X_REGION2) < __FloatType__(12.0e0)
    WR_REGION2[ii] = exp(-X_REGION2[ii]**2)
    WR_REGION2[~ii] = WR
    
    for I in range(6):
        R_REGION2 = X_REGION2 - T[I]
        R2_REGION2 = R_REGION2**2
        D_REGION2 = __FloatType__(1.0e0) / (R2_REGION2 + Y2_REGION2)
        D1_REGION2 = Y1_REGION2 * D_REGION2
        D2_REGION2 = R_REGION2 * D_REGION2
        WR_REGION2 = WR_REGION2 + Y_REGION2 * (U[I]*(R_REGION2*D2_REGION2 - 1.5e0*D1_REGION2) + 
                                               S[I]*Y3_REGION2*D2_REGION2)/(R2_REGION2 + 2.25e0)
        R_REGION2 = X_REGION2 + T[I]
        R2_REGION2 = R_REGION2**2                
        D_REGION2 = __FloatType__(1.0e0) / (R2_REGION2 + Y2_REGION2)
        D3_REGION2 = Y1_REGION2 * D_REGION2
        D4_REGION2 = R_REGION2 * D_REGION2
        WR_REGION2 = WR_REGION2 + Y_REGION2 * (U[I]*(R_REGION2*D4_REGION2 - 1.5e0*D3_REGION2) - 
                                               S[I]*Y3_REGION2*D4_REGION2)/(R2_REGION2 + 2.25e0)
        WI_REGION2 = WI_REGION2 + U[I]*(D2_REGION2 + D4_REGION2) + S[I]*(D1_REGION2 - D3_REGION2)

    # REGION3
    index_REGION1 = setdiff1d(array(index_REGION12),array(index_REGION2))
    X_REGION1 = X[index_REGION1]
    Y_REGION1 = X[index_REGION1]
    
    subindex_REGION1 = setdiff1d(array(arange(len(index_REGION12))),array(subindex_REGION2))
    Y1_REGION1 = Y1_REGION12[subindex_REGION1]
    Y2_REGION1 = Y2_REGION12[subindex_REGION1]
    
    WR_REGION1 = WR
    WI_REGION1 = WI  
    
    for I in range(6):
        R_REGION1 = X_REGION1 - T[I]
        D_REGION1 = __FloatType__(1.0e0) / (R_REGION1**2 + Y2_REGION1)
        D1_REGION1 = Y1_REGION1 * D_REGION1
        D2_REGION1 = R_REGION1 * D_REGION1
        R_REGION1 = X_REGION1 + T[I]
        D_REGION1 = __FloatType__(1.0e0) / (R_REGION1**2 + Y2_REGION1)
        D3_REGION1 = Y1_REGION1 * D_REGION1
        D4_REGION1 = R_REGION1 * D_REGION1
        
        WR_REGION1 = WR_REGION1 + U[I]*(D1_REGION1 + D3_REGION1) - S[I]*(D2_REGION1 - D4_REGION1)
        WI_REGION1 = WI_REGION1 + U[I]*(D2_REGION1 + D4_REGION1) + S[I]*(D1_REGION1 - D3_REGION1)

    # total result
    WR_TOTAL = zeros(len(X))
    WI_TOTAL = zeros(len(X))
    # REGION3
    WR_TOTAL[index_REGION3] = zsum_REGION3.real
    WI_TOTAL[index_REGION3] = zsum_REGION3.imag
    # REGION2
    WR_TOTAL[index_REGION2] = WR_REGION2
    WI_TOTAL[index_REGION2] = WI_REGION2
    # REGION1
    WR_TOTAL[index_REGION1] = WR_REGION1
    WI_TOTAL[index_REGION1] = WI_REGION1
    
    return WR_TOTAL,WI_TOTAL


hcpf = cpf # stub for initial cpf
    
# ------------------ Schreier CPF ------------------------

# "Optimized implementations of rational approximations 
#  for the Voigt and complex error function".
# Franz Schreier. JQSRT 112 (2011) 1010-10250
# doi:10.1016/j.jqsrt.2010.12.010

# Enable this if numpy.polyval doesn't perform well.
"""    
def polyval(p, x):
    y = zeros(x.shape, dtype=float)
    for i, v in enumerate(p):
        y *= x
        y += v
    return y
""";
    
def cef(x,y,N):
    # Computes the function w(z) = exp(-zA2) erfc(-iz) using a rational
    # series with N terms. It is assumed that Im(z) > 0 or Im(z) = 0.
    z = x + 1.0j*y
    M = 2*N; M2 = 2*M; k = arange(-M+1,M) #'; # M2 = no. of sampling points.
    L = sqrt(N/sqrt(2)); # Optimal choice of L.
    theta = k*pi/M; t = L*tan(theta/2); # Variables theta and t.
    #f = exp(-t.A2)*(LA2+t.A2); f = [0; f]; # Function to be transformed.
    f = zeros(len(t)+1); f[0] = 0
    f[1:] = exp(-t**2)*(L**2+t**2)
    #f = insert(exp(-t**2)*(L**2+t**2),0,0)
    a = real(fft(fftshift(f)))/M2; # Coefficients of transform.
    a = flipud(a[1:N+1]); # Reorder coefficients.
    Z = (L+1.0j*z)/(L-1.0j*z); p = polyval(a,Z); # Polynomial evaluation.
    w = 2*p/(L-1.0j*z)**2+(1/sqrt(pi))/(L-1.0j*z); # Evaluate w(z).
    return w

# weideman24 by default    
#weideman24 = lambda x,y: cef(x,y,24)
weideman = lambda x,y,n: cef(x,y,n)

def hum1_wei(x,y,n=24):
    t = y-1.0j*x
    cerf=1/sqrt(pi)*t/(0.5+t**2)
    """
    z = x+1j*y
    cerf = 1j*z/sqrt(pi)/(z**2-0.5)
    """
    mask = abs(x)+y<15.0
    if any(mask):
        w24 = weideman(x[mask],y[mask],n)
        place(cerf,mask,w24)
    return cerf.real,cerf.imag

VARIABLES['CPF'] = hum1_wei
#VARIABLES['CPF'] = cpf
    
# ------------------ Hartmann-Tran Profile (HTP) ------------------------
def pcqsdhc(sg0,GamD,Gam0,Gam2,Shift0,Shift2,anuVC,eta,sg):
    #-------------------------------------------------
    #      "pCqSDHC": partially-Correlated quadratic-Speed-Dependent Hard-Collision
    #      Subroutine to Compute the complex normalized spectral shape of an 
    #      isolated line by the pCqSDHC model
    #
    #      Reference:
    #      H. Tran, N.H. Ngo, J.-M. Hartmann.
    #      Efficient computation of some speed-dependent isolated line profiles.
    #      JQSRT, Volume 129, November 2013, Pages 199–203
    #      http://dx.doi.org/10.1016/j.jqsrt.2013.06.015
    #
    #      Input/Output Parameters of Routine (Arguments or Common)
    #      ---------------------------------
    #      T          : Temperature in Kelvin (Input).
    #      amM1       : Molar mass of the absorber in g/mol(Input).
    #      sg0        : Unperturbed line position in cm-1 (Input).
    #      GamD       : Doppler HWHM in cm-1 (Input)
    #      Gam0       : Speed-averaged line-width in cm-1 (Input).       
    #      Gam2       : Speed dependence of the line-width in cm-1 (Input).
    #      anuVC      : Velocity-changing frequency in cm-1 (Input).
    #      eta        : Correlation parameter, No unit (Input).
    #      Shift0     : Speed-averaged line-shift in cm-1 (Input).
    #      Shift2     : Speed dependence of the line-shift in cm-1 (Input)       
    #      sg         : Current WaveNumber of the Computation in cm-1 (Input).
    #
    #      Output Quantities (through Common Statements)
    #      -----------------
    #      LS_pCqSDHC_R: Real part of the normalized spectral shape (cm)
    #      LS_pCqSDHC_I: Imaginary part of the normalized spectral shape (cm)
    #
    #      Called Routines: 'CPF'      (Complex Probability Function)
    #      ---------------  'CPF3'      (Complex Probability Function for the region 3)
    #
    #      Called By: Main Program
    #      ---------
    #
    #     Double Precision Version
    #
    #-------------------------------------------------
    
    # sg is the only vector argument which is passed to function
    
    if type(sg) not in set([array,ndarray,list,tuple]):
        sg = array([sg])
    
    number_of_points = len(sg)
    Aterm_GLOBAL = zeros(number_of_points,dtype=__ComplexType__)
    Bterm_GLOBAL = zeros(number_of_points,dtype=__ComplexType__)

    cte=sqrt(log(2.0e0))/GamD
    rpi=sqrt(pi)
    iz = __ComplexType__(0.0e0 + 1.0e0j)

    c0 = __ComplexType__(Gam0 + 1.0e0j*Shift0)
    c2 = __ComplexType__(Gam2 + 1.0e0j*Shift2)
    c0t = __ComplexType__((1.0e0 - eta) * (c0 - 1.5e0 * c2) + anuVC)
    c2t = __ComplexType__((1.0e0 - eta) * c2)

    # PART1
    if abs(c2t) == 0.0e0:
        Z1 = (iz*(sg0 - sg) + c0t) * cte
        xZ1 = -Z1.imag
        yZ1 = Z1.real
        WR1,WI1 = VARIABLES['CPF'](xZ1,yZ1)
        Aterm_GLOBAL = rpi*cte*__ComplexType__(WR1 + 1.0e0j*WI1)
        index_Z1 = abs(Z1) <= 4.0e3
        index_NOT_Z1 = ~index_Z1
        if any(index_Z1):
            Bterm_GLOBAL = rpi*cte*((1.0e0 - Z1**2)*__ComplexType__(WR1 + 1.0e0j*WI1) + Z1/rpi)
        if any(index_NOT_Z1):
            Bterm_GLOBAL = cte*(rpi*__ComplexType__(WR1 + 1.0e0j*WI1) + 0.5e0/Z1 - 0.75e0/(Z1**3))
    else:
        # PART2, PART3 AND PART4   (PART4 IS A MAIN PART)

        # X - vector, Y - scalar
        X = (iz * (sg0 - sg) + c0t) / c2t
        Y = __ComplexType__(1.0e0 / ((2.0e0*cte*c2t))**2)
        csqrtY = (Gam2 - iz*Shift2) / (2.0e0*cte*(1.0e0-eta) * (Gam2**2 + Shift2**2))

        index_PART2 = abs(X) <= 3.0e-8 * abs(Y)
        index_PART3 = (abs(Y) <= 1.0e-15 * abs(X)) & ~index_PART2
        index_PART4 = ~ (index_PART2 | index_PART3)
        
        # PART4
        if any(index_PART4):
            X_TMP = X[index_PART4]
            Z1 = sqrt(X_TMP + Y) - csqrtY
            Z2 = Z1 + __FloatType__(2.0e0) * csqrtY
            xZ1 = -Z1.imag
            yZ1 =  Z1.real
            xZ2 = -Z2.imag
            yZ2 =  Z2.real
            SZ1 = sqrt(xZ1**2 + yZ1**2)
            SZ2 = sqrt(xZ2**2 + yZ2**2)
            DSZ = abs(SZ1 - SZ2)
            SZmx = maximum(SZ1,SZ2)
            SZmn = minimum(SZ1,SZ2)
            length_PART4 = len(index_PART4)
            WR1_PART4 = zeros(length_PART4)
            WI1_PART4 = zeros(length_PART4)
            WR2_PART4 = zeros(length_PART4)
            WI2_PART4 = zeros(length_PART4)
            index_CPF3 = (DSZ <= 1.0e0) & (SZmx > 8.0e0) & (SZmn <= 8.0e0)
            index_CPF = ~index_CPF3 # can be removed
            if any(index_CPF3):
                WR1,WI1 = cpf3(xZ1[index_CPF3],yZ1[index_CPF3])
                WR2,WI2 = cpf3(xZ2[index_CPF3],yZ2[index_CPF3])
                WR1_PART4[index_CPF3] = WR1
                WI1_PART4[index_CPF3] = WI1
                WR2_PART4[index_CPF3] = WR2
                WI2_PART4[index_CPF3] = WI2
            if any(index_CPF):
                WR1,WI1 = VARIABLES['CPF'](xZ1[index_CPF],yZ1[index_CPF])
                WR2,WI2 = VARIABLES['CPF'](xZ2[index_CPF],yZ2[index_CPF])
                WR1_PART4[index_CPF] = WR1
                WI1_PART4[index_CPF] = WI1
                WR2_PART4[index_CPF] = WR2
                WI2_PART4[index_CPF] = WI2
            
            Aterm = rpi*cte*(__ComplexType__(WR1_PART4 + 1.0e0j*WI1_PART4) - __ComplexType__(WR2_PART4+1.0e0j*WI2_PART4))
            Bterm = (-1.0e0 +
                      rpi/(2.0e0*csqrtY)*(1.0e0 - Z1**2)*__ComplexType__(WR1_PART4 + 1.0e0j*WI1_PART4)-
                      rpi/(2.0e0*csqrtY)*(1.0e0 - Z2**2)*__ComplexType__(WR2_PART4 + 1.0e0j*WI2_PART4)) / c2t
            Aterm_GLOBAL[index_PART4] = Aterm
            Bterm_GLOBAL[index_PART4] = Bterm

        # PART2
        if any(index_PART2):
            X_TMP = X[index_PART2]
            Z1 = (iz*(sg0 - sg[index_PART2]) + c0t) * cte
            Z2 = sqrt(X_TMP + Y) + csqrtY
            xZ1 = -Z1.imag
            yZ1 = Z1.real
            xZ2 = -Z2.imag
            yZ2 = Z2.real
            WR1_PART2,WI1_PART2 = VARIABLES['CPF'](xZ1,yZ1)
            WR2_PART2,WI2_PART2 = VARIABLES['CPF'](xZ2,yZ2) 
            Aterm = rpi*cte*(__ComplexType__(WR1_PART2 + 1.0e0j*WI1_PART2) - __ComplexType__(WR2_PART2 + 1.0e0j*WI2_PART2))
            Bterm = (-1.0e0 +
                      rpi/(2.0e0*csqrtY)*(1.0e0 - Z1**2)*__ComplexType__(WR1_PART2 + 1.0e0j*WI1_PART2)-
                      rpi/(2.0e0*csqrtY)*(1.0e0 - Z2**2)*__ComplexType__(WR2_PART2 + 1.0e0j*WI2_PART2)) / c2t
            Aterm_GLOBAL[index_PART2] = Aterm
            Bterm_GLOBAL[index_PART2] = Bterm
            
        # PART3
        if any(index_PART3):
            X_TMP = X[index_PART3]
            xZ1 = -sqrt(X_TMP + Y).imag
            yZ1 = sqrt(X_TMP + Y).real
            WR1_PART3,WI1_PART3 =  VARIABLES['CPF'](xZ1,yZ1) 
            index_ABS = abs(sqrt(X_TMP)) <= 4.0e3
            index_NOT_ABS = ~index_ABS
            Aterm = zeros(len(index_PART3),dtype=__ComplexType__)
            Bterm = zeros(len(index_PART3),dtype=__ComplexType__)
            if any(index_ABS):
                xXb = -sqrt(X).imag
                yXb = sqrt(X).real
                WRb,WIb = VARIABLES['CPF'](xXb,yXb)
                Aterm[index_ABS] = (2.0e0*rpi/c2t)*(1.0e0/rpi - sqrt(X_TMP[index_ABS])*__ComplexType__(WRb + 1.0e0j*WIb))
                Bterm[index_ABS] = (1.0e0/c2t)*(-1.0e0+
                                  2.0e0*rpi*(1.0e0 - X_TMP[index_ABS]-2.0e0*Y)*(1.0e0/rpi-sqrt(X_TMP[index_ABS])*__ComplexType__(WRb + 1.0e0j*WIb))+
                                  2.0e0*rpi*sqrt(X_TMP[index_ABS] + Y)*__ComplexType__(WR1_PART3 + 1.0e0j*WI1_PART3))
            if any(index_NOT_ABS):
                Aterm[index_NOT_ABS] = (1.0e0/c2t)*(1.0e0/X_TMP[index_NOT_ABS] - 1.5e0/(X_TMP[index_NOT_ABS]**2))
                Bterm[index_NOT_ABS] = (1.0e0/c2t)*(-1.0e0 + (1.0e0 - X_TMP[index_NOT_ABS] - 2.0e0*Y)*
                                        (1.0e0/X_TMP[index_NOT_ABS] - 1.5e0/(X_TMP[index_NOT_ABS]**2))+
                                         2.0e0*rpi*sqrt(X_TMP[index_NOT_ABS] + Y)*__ComplexType__(WR1 + 1.0e0j*WI1))
            Aterm_GLOBAL[index_PART3] = Aterm
            Bterm_GLOBAL[index_PART3] = Bterm
            
    # common part
    LS_pCqSDHC = (1.0e0/pi) * (Aterm_GLOBAL / (1.0e0 - (anuVC-eta*(c0-1.5e0*c2))*Aterm_GLOBAL + eta*c2*Bterm_GLOBAL))
    return LS_pCqSDHC.real,LS_pCqSDHC.imag



# ------------------  CROSS-SECTIONS, XSECT.PY --------------------------------

# set interfaces for profiles

def PROFILE_HT(sg0,GamD,Gam0,Gam2,Shift0,Shift2,anuVC,eta,sg):
    """
    #-------------------------------------------------
    #      "pCqSDHC": partially-Correlated quadratic-Speed-Dependent Hard-Collision
    #      Subroutine to Compute the complex normalized spectral shape of an 
    #      isolated line by the pCqSDHC model
    #
    #      References:
    #
    #      1) N.H. Ngo, D. Lisak, H. Tran, J.-M. Hartmann.
    #         An isolated line-shape model to go beyond the Voigt profile in 
    #         spectroscopic databases and radiative transfer codes.
    #         JQSRT, Volume 129, November 2013, Pages 89–100
    #         http://dx.doi.org/10.1016/j.jqsrt.2013.05.034
    #
    #      2) H. Tran, N.H. Ngo, J.-M. Hartmann.
    #         Efficient computation of some speed-dependent isolated line profiles.
    #         JQSRT, Volume 129, November 2013, Pages 199–203
    #         http://dx.doi.org/10.1016/j.jqsrt.2013.06.015
    #
    #      3) H. Tran, N.H. Ngo, J.-M. Hartmann.
    #         Erratum to “Efficient computation of some speed-dependent isolated line profiles”.
    #         JQSRT, Volume 134, February 2014, Pages 104
    #         http://dx.doi.org/10.1016/j.jqsrt.2013.10.015
    #
    #      Input/Output Parameters of Routine (Arguments or Common)
    #      ---------------------------------
    #      T       : Temperature in Kelvin (Input).
    #      amM1    : Molar mass of the absorber in g/mol(Input).
    #      sg0     : Unperturbed line position in cm-1 (Input).
    #      GamD    : Doppler HWHM in cm-1 (Input)
    #      Gam0    : Speed-averaged line-width in cm-1 (Input).       
    #      Gam2    : Speed dependence of the line-width in cm-1 (Input).
    #      anuVC   : Velocity-changing frequency in cm-1 (Input).
    #      eta     : Correlation parameter, No unit (Input).
    #      Shift0  : Speed-averaged line-shift in cm-1 (Input).
    #      Shift2  : Speed dependence of the line-shift in cm-1 (Input)       
    #      sg      : Current WaveNumber of the Computation in cm-1 (Input).
    #
    #      The function has two outputs:
    #      -----------------
    #      (1): Real part of the normalized spectral shape (cm)
    #      (2): Imaginary part of the normalized spectral shape (cm)
    #
    #      Called Routines: 'CPF'       (Complex Probability Function)
    #      ---------------  'CPF3'      (Complex Probability Function for the region 3)
    #
    #      Based on a double precision Fortran version
    #
    #-------------------------------------------------
    """
    return pcqsdhc(sg0,GamD,Gam0,Gam2,Shift0,Shift2,anuVC,eta,sg)

PROFILE_HTP = PROFILE_HT # stub for backwards compatibility

def PROFILE_SDRAUTIAN(sg0,GamD,Gam0,Gam2,Shift0,Shift2,anuVC,sg):
    """
    # Speed dependent Rautian profile based on HTP.
    # Input parameters:
    #      sg0     : Unperturbed line position in cm-1 (Input).
    #      GamD    : Doppler HWHM in cm-1 (Input)
    #      Gam0    : Speed-averaged line-width in cm-1 (Input).       
    #      Gam2    : Speed dependence of the line-width in cm-1 (Input).
    #      anuVC   : Velocity-changing frequency in cm-1 (Input).
    #      Shift0  : Speed-averaged line-shift in cm-1 (Input).
    #      Shift2  : Speed dependence of the line-shift in cm-1 (Input)       
    #      sg      : Current WaveNumber of the Computation in cm-1 (Input).
    """
    return pcqsdhc(sg0,GamD,Gam0,Gam2,Shift0,Shift2,anuVC,cZero,sg)

def PROFILE_RAUTIAN(sg0,GamD,Gam0,Shift0,anuVC,eta,sg):
    """
    # Rautian profile based on HTP.
    # Input parameters:
    #      sg0     : Unperturbed line position in cm-1 (Input).
    #      GamD    : Doppler HWHM in cm-1 (Input)
    #      Gam0    : Speed-averaged line-width in cm-1 (Input).       
    #      anuVC   : Velocity-changing frequency in cm-1 (Input).
    #      Shift0  : Speed-averaged line-shift in cm-1 (Input).
    #      sg      : Current WaveNumber of the Computation in cm-1 (Input).
    """
    return pcqsdhc(sg0,GamD,Gam0,cZero,Shift0,cZero,anuVC,cZero,sg)

def PROFILE_SDVOIGT(sg0,GamD,Gam0,Gam2,Shift0,Shift2,sg):
    """
    # Speed dependent Voigt profile based on HTP.
    # Input parameters:
    #      sg0     : Unperturbed line position in cm-1 (Input).
    #      GamD    : Doppler HWHM in cm-1 (Input)
    #      Gam0    : Speed-averaged line-width in cm-1 (Input).       
    #      Gam2    : Speed dependence of the line-width in cm-1 (Input).
    #      Shift0  : Speed-averaged line-shift in cm-1 (Input).
    #      Shift2  : Speed dependence of the line-shift in cm-1 (Input)       
    #      sg      : Current WaveNumber of the Computation in cm-1 (Input).
    """
    return pcqsdhc(sg0,GamD,Gam0,Gam2,Shift0,Shift2,cZero,cZero,sg)
    
def PROFILE_VOIGT(sg0,GamD,Gam0,sg):
    """
    # Voigt profile based on HTP.
    # Input parameters:
    #   sg0: Unperturbed line position in cm-1 (Input).
    #   GamD: Doppler HWHM in cm-1 (Input)
    #   Gam0: Speed-averaged line-width in cm-1 (Input).       
    #   sg: Current WaveNumber of the Computation in cm-1 (Input).
    """
    return PROFILE_HTP(sg0,GamD,Gam0,cZero,cZero,cZero,cZero,cZero,sg)

def PROFILE_LORENTZ(sg0,Gam0,sg):
    """
    # Lorentz profile.
    # Input parameters:
    #   sg0: Unperturbed line position in cm-1 (Input).
    #   Gam0: Speed-averaged line-width in cm-1 (Input).       
    #   sg: Current WaveNumber of the Computation in cm-1 (Input).
    """
    return Gam0/(pi*(Gam0**2+(sg-sg0)**2))

def PROFILE_DOPPLER(sg0,GamD,sg):
    """
    # Doppler profile.
    # Input parameters:
    #   sg0: Unperturbed line position in cm-1 (Input).
    #   GamD: Doppler HWHM in cm-1 (Input)
    #   sg: Current WaveNumber of the Computation in cm-1 (Input).
    """
    return cSqrtLn2divSqrtPi*exp(-cLn2*((sg-sg0)/GamD)**2)/GamD

# Volume concentration of all gas molecules at the pressure p and temperature T
def volumeConcentration(p,T):
    return (p/9.869233e-7)/(cBolts*T) # CGS

# ------------------------------- PARAMETER DEPENDENCIES --------------------------------

# temperature dependence for intencities (HITRAN)
def EnvironmentDependency_Intensity(LineIntensityRef,T,Tref,SigmaT,SigmaTref,
                                    LowerStateEnergy,LineCenter):
    const = __FloatType__(1.4388028496642257)
    ch = exp(-const*LowerStateEnergy/T)*(1-exp(-const*LineCenter/T))
    zn = exp(-const*LowerStateEnergy/Tref)*(1-exp(-const*LineCenter/Tref))
    LineIntensity = LineIntensityRef*SigmaTref/SigmaT*ch/zn
    return LineIntensity

# environmental dependence for GammaD (HTP, Voigt)    # Tref/T ????
def EnvironmentDependency_GammaD(GammaD_ref,T,Tref):
    # Doppler parameters do not depend on pressure!
    return GammaD_ref*sqrt(T/Tref)

# environmental dependence for Gamma0 (HTP, Voigt)
def EnvironmentDependency_Gamma0(Gamma0_ref,T,Tref,p,pref,TempRatioPower):
    return Gamma0_ref*p/pref*(Tref/T)**TempRatioPower

# environmental dependence for Gamma2 (HTP)
def EnvironmentDependency_Gamma2(Gamma2_ref,T,Tref,p,pref,TempRatioPower):
    return Gamma2_ref*p/pref*(Tref/T)**TempRatioPower

# environmental dependence for Delta0 (HTP)
def EnvironmentDependency_Delta0(Delta0_ref,p,pref):
    return Delta0_ref*p/pref

# environmental dependence for Delta2 (HTP)
def EnvironmentDependency_Delta2(Delta2_ref,p,pref):
    return Delta2_ref*p/pref

# environmental dependence for anuVC (HTP)
def EnvironmentDependency_anuVC(anuVC_ref,T,Tref,p,pref):
    return anuVC_ref*Tref/T*p/pref

# ------------------------------- /PARAMETER DEPENDENCIES --------------------------------

# ------------------------------- BINGINGS --------------------------------

# default parameter bindings
DefaultParameterBindings = {}

# default temperature dependencies
DefaultEnvironmentDependencyBindings = {}

# ------------------------------- /BINGINGS --------------------------------

# default values for intensity threshold
DefaultIntensityThreshold = 0. # cm*molec

# default value for omega wing in halfwidths (from center)
DefaultOmegaWingHW = 50. # cm-1    HOTW default


# check and argument for being a tuple or list
# this is connected with a "bug" that in Python
# (val) is not a tuple, but (val,) is a tuple
def listOfTuples(a):
    if type(a) not in set([list,tuple]):
        a = [a]
    return a


# determine default parameters from those which are passed to absorptionCoefficient_...
def getDefaultValuesForXsect(Components,SourceTables,Environment,OmegaRange,
                             OmegaStep,OmegaWing,IntensityThreshold,Format):
    if SourceTables[0] == None:
        SourceTables = ['__BUFFER__',]
    if Environment == None:
        Environment = {'T':296., 'p':1.}
    if Components == [None]:
        CompDict = {}
        for TableName in SourceTables:
            # check table existance
            if TableName not in LOCAL_TABLE_CACHE.keys():
                raise Exception('%s: no such table. Check tableList() for more info.' % TableName)
            mol_ids = LOCAL_TABLE_CACHE[TableName]['data']['molec_id']
            iso_ids = LOCAL_TABLE_CACHE[TableName]['data']['local_iso_id']
            if len(mol_ids) != len(iso_ids):
                raise Exception('Lengths if mol_ids and iso_ids differ!')
            MI_zip = zip(mol_ids,iso_ids)
            MI_zip = set(MI_zip)
            for mol_id,iso_id in MI_zip:
                CompDict[(mol_id,iso_id)] = None
        Components = CompDict.keys()
    if OmegaRange == None:
        omega_min = float('inf')
        omega_max = float('-inf')
        for TableName in SourceTables:
            nu = LOCAL_TABLE_CACHE[TableName]['data']['nu']
            numin = min(nu)
            numax = max(nu)
            if omega_min > numin:
                omega_min = numin
            if omega_max < numax:
                omega_max = numax
        OmegaRange = (omega_min,omega_max)
    if OmegaStep == None:
        OmegaStep = 0.01 # cm-1
    if OmegaWing == None:
        OmegaWing = 0.0 # cm-1
    if not Format:
        """
        Infinitesimal = 1e-14 # put this to header in next version!
        min_number_of_digits = 4 # minimal number of digits after dec. pnt.
        last_digit_pos = 0
        while modf(OmegaStep * 10**last_digit_pos)[0] > Infinitesimal:
            last_digit_pos += 1
        actual_number_of_digits = max(min_number_of_digits,last_digit_pos)
        Format = '%%.%df %%e' % actual_number_of_digits
        """
        Format = '%.12f %e'
    return Components,SourceTables,Environment,OmegaRange,\
           OmegaStep,OmegaWing,IntensityThreshold,Format


# save numpy arrays to file
# arrays must have same dimensions
def save_to_file(fname,fformat,*arg):
    f = open(fname,'w')
    for i in range(len(arg[0])):
        argline = []
        for j in range(len(arg)):
            argline.append(arg[j][i])
        f.write((fformat+'\n') % tuple(argline))
    f.close()

# ==========================================================================================
# =========================== NEW ABSORPTION COEFFICIENT ===================================
# ==========================================================================================




def absorptionCoefficient_HT(Components=None,SourceTables=None,partitionFunction=PYTIPS2017,
                                Environment=None,OmegaRange=None,OmegaStep=None,OmegaWing=None,
                                IntensityThreshold=DefaultIntensityThreshold,
                                OmegaWingHW=DefaultOmegaWingHW,
                                GammaL='gamma_air', HITRAN_units=True, LineShift=True,
                                File=None, Format=None, OmegaGrid=None,
                                WavenumberRange=None,WavenumberStep=None,WavenumberWing=None,
                                WavenumberWingHW=None,WavenumberGrid=None,
                                Diluent={},EnvDependences=None):
    """
    INPUT PARAMETERS: 
        Components:  list of tuples [(M,I,D)], where
                        M - HITRAN molecule number,
                        I - HITRAN isotopologue number,
                        D - relative abundance (optional)
        SourceTables:  list of tables from which to calculate cross-section   (optional)
        partitionFunction:  pointer to partition function (default is PYTIPS) (optional)
        Environment:  dictionary containing thermodynamic parameters.
                        'p' - pressure in atmospheres,
                        'T' - temperature in Kelvin
                        Default={'p':1.,'T':296.}
        WavenumberRange:  wavenumber range to consider.
        WavenumberStep:   wavenumber step to consider. 
        WavenumberWing:   absolute wing for calculating a lineshape (in cm-1) 
        WavenumberWingHW:  relative wing for calculating a lineshape (in halfwidths)
        IntensityThreshold:  threshold for intensities
        GammaL:  specifies broadening parameter ('gamma_air' or 'gamma_self')
        HITRAN_units:  use cm2/molecule (True) or cm-1 (False) for absorption coefficient
        File:   write output to file (if specified)
        Format:  c-format of file output (accounts for significant digits in WavenumberStep)
    OUTPUT PARAMETERS: 
        Wavenum: wavenumber grid with respect to parameters WavenumberRange and WavenumberStep
        Xsect: absorption coefficient calculated on the grid
    ---
    DESCRIPTION:
        Calculate absorption coefficient using HT profile.
        Absorption coefficient is calculated at arbitrary temperature and pressure.
        User can vary a wide range of parameters to control a process of calculation.
        The choise of these parameters depends on properties of a particular linelist.
        Default values are a sort of guess which gives a decent precision (on average) 
        for a reasonable amount of cpu time. To increase calculation accuracy,
        user should use a trial and error method.
    ---
    EXAMPLE OF USAGE:
        nu,coef = absorptionCoefficient_HT(((2,1),),'co2',WavenumberStep=0.01,
                                              HITRAN_units=False,GammaL='gamma_self')
    ---
    """
      
    # Parameters OmegaRange,OmegaStep,OmegaWing,OmegaWingHW, and OmegaGrid
    # are deprecated and given for backward compatibility with the older versions.
    if WavenumberRange:  OmegaRange=WavenumberRange
    if WavenumberStep:   OmegaStep=WavenumberStep
    if WavenumberWing:   OmegaWing=WavenumberWing
    if WavenumberWingHW: OmegaWingHW=WavenumberWingHW
    if WavenumberGrid:   OmegaGrid=WavenumberGrid

    # "bug" with 1-element list
    Components = listOfTuples(Components)
    SourceTables = listOfTuples(SourceTables)
    
    # determine final input values
    Components,SourceTables,Environment,OmegaRange,OmegaStep,OmegaWing,\
    IntensityThreshold,Format = \
       getDefaultValuesForXsect(Components,SourceTables,Environment,OmegaRange,
                                OmegaStep,OmegaWing,IntensityThreshold,Format)
    
    # warn user about too large omega step
    if OmegaStep>0.1: warn('Big wavenumber step: possible accuracy decline')

    # get uniform linespace for cross-section
    #number_of_points = (OmegaRange[1]-OmegaRange[0])/OmegaStep + 1
    #Omegas = linspace(OmegaRange[0],OmegaRange[1],number_of_points)
    if OmegaGrid is not None:
        Omegas = npsort(OmegaGrid)
    else:
        #Omegas = arange(OmegaRange[0],OmegaRange[1],OmegaStep)
        Omegas = arange_(OmegaRange[0],OmegaRange[1],OmegaStep) # fix
    number_of_points = len(Omegas)
    Xsect = zeros(number_of_points)
       
    # reference temperature and pressure
    Tref = __FloatType__(296.) # K
    pref = __FloatType__(1.) # atm
    
    # actual temperature and pressure
    T = Environment['T'] # K
    p = Environment['p'] # atm
       
    # Find reference temperature
    TRanges = [(0,100),(100,200),(200,400),(400,float('inf'))]
    Trefs = [50.,150.,296.,700.]
    for TRange,TrefHT in zip(TRanges,Trefs):
        if T >= TRange[0] and T < TRange[1]:
            break
    if VARIABLES['DEBUG']: print('absorptionCoefficient_HT: TrefHT=%f'%TrefHT)

    # create dictionary from Components
    ABUNDANCES = {}
    NATURAL_ABUNDANCES = {}
    for Component in Components:
        M = Component[0]
        I = Component[1]
        if len(Component) >= 3:
            ni = Component[2]
        else:
            try:
                ni = ISO[(M,I)][ISO_INDEX['abundance']]
            except KeyError:
                raise Exception('cannot find component M,I = %d,%d.' % (M,I))
        ABUNDANCES[(M,I)] = ni
        NATURAL_ABUNDANCES[(M,I)] = ISO[(M,I)][ISO_INDEX['abundance']]
        
    # precalculation of volume concentration
    if HITRAN_units:
        factor = __FloatType__(1.0)
    else:
        factor = volumeConcentration(p,T)
    if VARIABLES['DEBUG']: print('absorptionCoefficient_HT: factor=%f'%factor)        
        
    # setup the default empty environment dependence function
    if not EnvDependences:
        EnvDependences = lambda ENV,LINE:{}
    Env = Environment.copy()
    Env['Tref'] = Tref
    Env['pref'] = pref
  
    # setup the Diluent variable
    GammaL = GammaL.lower()
    if not Diluent:
        if GammaL == 'gamma_air':
            Diluent = {'air':1.}
        elif GammaL == 'gamma_self':
            Diluent = {'self':1.}
        else:
            raise Exception('Unknown GammaL value: %s' % GammaL)
    if VARIABLES['DEBUG']: print('absorptionCoefficient_HT: Diluent=%s'%Diluent)
        
    # Simple check
    print(Diluent)  # Added print statement # CHANGED RJH 23MAR18  # Simple check
    for key in Diluent:
        val = Diluent[key]
        if val < 0 or val > 1: # if val < 0 and val > 1:# CHANGED RJH 23MAR18
            raise Exception('Diluent fraction must be in [0,1]')
    
    # SourceTables contain multiple tables
    for TableName in SourceTables:

        # get the number of rows
        nline = LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']
        
        # get parameter names for each table
        parnames = LOCAL_TABLE_CACHE[TableName]['data'].keys()
        
        # loop through line centers (single stream)
        for RowID in range(nline):
            
            # Get the custom environment dependences
            Line = {}
            for parname in parnames:
                Line[parname] = LOCAL_TABLE_CACHE[TableName]['data'][parname][RowID]
            CustomEnvDependences = EnvDependences(Env,Line)
            
            # get basic line parameters (lower level)
            LineCenterDB = LOCAL_TABLE_CACHE[TableName]['data']['nu'][RowID]
            LineIntensityDB = LOCAL_TABLE_CACHE[TableName]['data']['sw'][RowID]
            LowerStateEnergyDB = LOCAL_TABLE_CACHE[TableName]['data']['elower'][RowID]
            MoleculeNumberDB = LOCAL_TABLE_CACHE[TableName]['data']['molec_id'][RowID]
            IsoNumberDB = LOCAL_TABLE_CACHE[TableName]['data']['local_iso_id'][RowID]
            
            # filter by molecule and isotopologue
            if (MoleculeNumberDB,IsoNumberDB) not in ABUNDANCES: continue
            
            # partition functions for T and Tref
            SigmaT = partitionFunction(MoleculeNumberDB,IsoNumberDB,T)
            SigmaTref = partitionFunction(MoleculeNumberDB,IsoNumberDB,Tref)
            
            # get all environment dependences from voigt parameters
            
            #   intensity
            if 'sw' in CustomEnvDependences:
                LineIntensity = CustomEnvDependences['sw']
            else:
                LineIntensity = EnvironmentDependency_Intensity(LineIntensityDB,T,Tref,SigmaT,SigmaTref,
                                                                LowerStateEnergyDB,LineCenterDB)
            
            #   FILTER by LineIntensity: compare it with IntencityThreshold
            if LineIntensity < IntensityThreshold: continue
            
            #   doppler broadening coefficient (GammaD)
            cMassMol = 1.66053873e-27 # hapi
            m = molecularMass(MoleculeNumberDB,IsoNumberDB) * cMassMol * 1000
            GammaD = sqrt(2*cBolts*T*log(2)/m/cc**2)*LineCenterDB
            
            #   pressure broadening coefficient
            Gamma0 = 0.; Shift0 = 0.; Gamma2 = 0.; Shift2 = 0.; NuVC = 0.; EtaNumer = 0.;
            for species in Diluent:
                species_lower = species # species_lower = species.lower() # CHANGED RJH 23MAR18
                
                abun = Diluent[species]
                
                # Search for broadening HWHM.
                try:
                    # search for HT-style name
                    Gamma0DB = LOCAL_TABLE_CACHE[TableName]['data']['gamma_HT_0_%s_%d'%(species_lower,TrefHT)][RowID]
                    if Gamma0DB == 0.: raise KeyError
                    if VARIABLES['DEBUG']: print('absorptionCoefficient_HT: Gamma0DB=%f (found as %s)'%(Gamma0DB,'gamma_HT_0_%s_%d'%(species_lower,TrefHT)))
                except KeyError:
                    try:
                        # search for Voigt-style name
                        Gamma0DB = LOCAL_TABLE_CACHE[TableName]['data']['gamma_%s'%species_lower][RowID]
                        if VARIABLES['DEBUG']: print('absorptionCoefficient_HT: Gamma0DB=%f (found as %s)'%(Gamma0DB,'gamma_%s'%species_lower))
                    except KeyError:
                        Gamma0DB = 0.0
                        if VARIABLES['DEBUG']: print('absorptionCoefficient_HT: Gamma0DB=%f (not found in database)'%Gamma0DB)
                
                # Search for temperature exponent for broadening HWHM.
                try:
                    # search for HT-style name
                    TempRatioPowerDB = LOCAL_TABLE_CACHE[TableName]['data']['n_HT_%s_%d'%(species_lower,TrefHT)][RowID]
                    if TempRatioPowerDB == 0.: raise KeyError
                    Tref = TrefHT
                    if VARIABLES['DEBUG']: print('absorptionCoefficient_HT: TempRatioPowerDB=%f (found as %s)'%(TempRatioPowerDB,'n_HT_%s_%d'%(species_lower,TrefHT)))
                except KeyError:
                    Tref = 296.
                    try:
                        # search for Voigt-style name
                        TempRatioPowerDB = LOCAL_TABLE_CACHE[TableName]['data']['n_%s'%species_lower][RowID]
                        if VARIABLES['DEBUG']: print('absorptionCoefficient_HT: TempRatioPowerDB=%f (found as %s). Tref is set to 296K.'%(TempRatioPowerDB,'n_%s'%species_lower))
                        if species_lower == 'self' and TempRatioPowerDB == 0.:
                            TempRatioPowerDB = LOCAL_TABLE_CACHE[TableName]['data']['n_air'][RowID] # same for self as for air
                            if VARIABLES['DEBUG']: print('absorptionCoefficient_HT: using n_air for self species because n_self=0.0')
                    except KeyError:
                        #print('TempRatioPowerDB is set to zero')
                        #TempRatioPowerDB = 0                    
                        TempRatioPowerDB = LOCAL_TABLE_CACHE[TableName]['data']['n_air'][RowID]
                        if VARIABLES['DEBUG']: print('absorptionCoefficient_HT: TempRatioPowerDB=%f (found as n_air). Tref is set to 296K.'%TempRatioPowerDB)
                
                # Add to the final Gamma0
                Gamma0T = CustomEnvDependences.get('gamma_HT_0_%s_%d'%(species_lower,TrefHT),
                           CustomEnvDependences.get('gamma_%s'%species_lower, 
                            EnvironmentDependency_Gamma0(Gamma0DB,T,Tref,p,pref,TempRatioPowerDB)))
                Gamma0 += abun*Gamma0T

                # Search for shift.
                try:
                    # search for HT-style name
                    Shift0DB = LOCAL_TABLE_CACHE[TableName]['data']['delta_HT_0_%s_%d'%(species_lower,TrefHT)][RowID]
                    if Shift0DB == 0.: raise KeyError
                    if VARIABLES['DEBUG']: print('absorptionCoefficient_HT: Shift0DB=%f (found as %s)'%(Shift0DB,'delta_HT_0_%s_%d'%(species_lower,TrefHT)))
                except KeyError:
                    try:
                        # search for Voigt-style name
                        Shift0DB = LOCAL_TABLE_CACHE[TableName]['data']['delta_%s'%species_lower][RowID]
                        if VARIABLES['DEBUG']: print('absorptionCoefficient_HT: Shift0DB=%f (found as %s)'%(Shift0DB,'delta_%s'%species_lower))
                    except KeyError:
                        Shift0DB = 0.0
                        if VARIABLES['DEBUG']: print('absorptionCoefficient_HT: Shift0DB=%f (not found in database)'%Shift0DB)
                
                # Search for temperature dependence for shift.
                try:
                    # search for HT-style name
                    deltap = LOCAL_TABLE_CACHE[TableName]['data']['deltap_HT_%s_%d'%(species_lower,TrefHT)][RowID]
                    if deltap ==0.: raise KeyError
                    Tref = TrefHT
                    if VARIABLES['DEBUG']: print('absorptionCoefficient_HT: deltap=%f (found as %s)'%(deltap,'deltap_HT_%s_%d'%(species_lower,TrefHT)))
                except KeyError:
                    Tref = 296.
                    try:
                        # search for Voigt-style name
                        deltap = LOCAL_TABLE_CACHE[TableName]['data']['deltap_%s'%species_lower][RowID]
                        if VARIABLES['DEBUG']: print('absorptionCoefficient_HT: deltap=%f (found as %s). Tref is set to 296K.'%(deltap,'deltap_%s'%species_lower))
                    except KeyError:
                        deltap = 0.0
                        if VARIABLES['DEBUG']: print('absorptionCoefficient_HT: deltap=%f (not found in database)'%deltap)

                Shift0T = CustomEnvDependences.get('deltap_HT_%s_%d'%(species_lower,TrefHT),
                                CustomEnvDependences.get('deltap_%s'%species_lower,
                                 ((Shift0DB + deltap*(T-Tref))*p/pref)))
                Shift0 += abun*Shift0T
                
                # Search for speed dependence for HWHM.
                try:
                    Gamma2DB = LOCAL_TABLE_CACHE[TableName]['data']['gamma_HT_2_%s_%d'%(species_lower,TrefHT)][RowID]
                    if Gamma2DB ==0.: raise KeyError
                    if VARIABLES['DEBUG']: print('absorptionCoefficient_HT: Gamma2DB=%f (found as %s)'%(Gamma2DB,'gamma_HT_2_%s_%d'%(species_lower,TrefHT)))
                except KeyError:
                    try:
                        SDDB = LOCAL_TABLE_CACHE[TableName]['data']['SD_%s'%species_lower][RowID]
                        Gamma2DB = SDDB*Gamma0DB
                        if VARIABLES['DEBUG']: print('absorptionCoefficient_HT: SDDB=%f (found as %s)'%(SDDB,'SD_%s'%species_lower))
                        if VARIABLES['DEBUG']: print('absorptionCoefficient_HT: Gamma2DB = SDDB*Gamma0DB')
                    except KeyError:
                        Gamma2DB = 0.0
                        if VARIABLES['DEBUG']: print('absorptionCoefficient_HT: Gamma2DB=%f (not found in database)'%Gamma2DB)

                Gamma2 += abun*CustomEnvDependences.get('gamma_HT_2_%s_%d'%(species_lower,TrefHT),Gamma2DB*(p/pref))
                
                # Search for speed dependence for shift.
                try:
                    Shift2DB = LOCAL_TABLE_CACHE[TableName]['data']['delta_HT_2_%s_%d'%(species_lower,TrefHT)][RowID]
                    if VARIABLES['DEBUG']: print('absorptionCoefficient_HT: Shift2DB=%f (found as %s)'%(Shift2DB,'delta_HT_2_%s_%d'%(species_lower,TrefHT)))
                except KeyError:
                    Shift2DB = 0.
                    if VARIABLES['DEBUG']: print('absorptionCoefficient_HT: Shift2DB=%f (not found in database)'%Shift2DB)
                
                Shift2 += abun*CustomEnvDependences.get('delta_HT_2_%s_%d'%(species_lower,TrefHT),
                                Shift2DB*p/pref)
                
                # Search for frequency of VC
                try:
                    NuVCDB = LOCAL_TABLE_CACHE[TableName]['data']['nu_HT_%s'%species_lower][RowID]
                    if VARIABLES['DEBUG']: print('absorptionCoefficient_HT: NuVCDB=%f (found as %s)'%(NuVCDB,'nu_HT_%s'%species_lower))
                except KeyError:
                    NuVCDB = 0.
                    if VARIABLES['DEBUG']: print('absorptionCoefficient_HT: NuVCDB=%f (not found in database)'%NuVCDB)
                
                # Search for temperature exponent for frequency of VC
                try:
                    KappaDB = LOCAL_TABLE_CACHE[TableName]['data']['kappa_HT_%s'%species_lower][RowID]
                    if VARIABLES['DEBUG']: print('absorptionCoefficient_HT: KappaDB=%f (found as %s)'%(KappaDB,'kappa_HT_%s'%species_lower))
                except KeyError:
                    KappaDB = 0.
                    if VARIABLES['DEBUG']: print('absorptionCoefficient_HT: KappaDB=%f (not found in database)'%KappaDB)
                    
                NuVC += abun*CustomEnvDependences.get('nu_HT_%s'%species_lower,
                             NuVCDB*(Tref/T)**KappaDB*p)
                             
                # Setup correlation parameter
                try:
                    EtaDB = LOCAL_TABLE_CACHE[TableName]['data']['eta_HT_%s'%species_lower][RowID]
                    if VARIABLES['DEBUG']: print('absorptionCoefficient_HT: EtaDB=%f (found as %s)'%(EtaDB,'eta_HT_%s'%species_lower))
                except KeyError:
                    EtaDB = 0.
                    if VARIABLES['DEBUG']: print('absorptionCoefficient_HT: EtaDB=%f (not found in database)'%EtaDB)
                
                EtaNumer += EtaDB*abun*(Gamma0T+1j*Shift0T)
                
            Eta = EtaNumer/(Gamma0 + 1j*Shift0)
                    
            #   get final wing of the line according to Gamma0, OmegaWingHW and OmegaWing
            OmegaWingF = max(OmegaWing,OmegaWingHW*Gamma0,OmegaWingHW*GammaD)

            BoundIndexLower = bisect(Omegas,LineCenterDB-OmegaWingF)
            BoundIndexUpper = bisect(Omegas,LineCenterDB+OmegaWingF)
            lineshape_vals = PROFILE_HT(LineCenterDB,GammaD,Gamma0,Gamma2,Shift0,Shift2,NuVC,Eta,Omegas[BoundIndexLower:BoundIndexUpper])[0]
            Xsect[BoundIndexLower:BoundIndexUpper] += factor / NATURAL_ABUNDANCES[(MoleculeNumberDB,IsoNumberDB)] * \
                                                      ABUNDANCES[(MoleculeNumberDB,IsoNumberDB)] * \
                                                      LineIntensity * lineshape_vals
   
    if File: save_to_file(File,Format,Omegas,Xsect)
    return Omegas,Xsect
    

def absorptionCoefficient_SDVoigt(Components=None,SourceTables=None,partitionFunction=PYTIPS,
                                Environment=None,OmegaRange=None,OmegaStep=None,OmegaWing=None,
                                IntensityThreshold=DefaultIntensityThreshold,
                                OmegaWingHW=DefaultOmegaWingHW,
                                GammaL='gamma_air', HITRAN_units=True, LineShift=True,
                                File=None, Format=None, OmegaGrid=None,
                                WavenumberRange=None,WavenumberStep=None,WavenumberWing=None,
                                WavenumberWingHW=None,WavenumberGrid=None,
                                Diluent={},EnvDependences=None):
    """
    INPUT PARAMETERS:
        Components:  list of tuples [(M,I,D)], where
                        M - HITRAN molecule number,
                        I - HITRAN isotopologue number,
                        D - relative abundance (optional)
        SourceTables:  list of tables from which to calculate cross-section   (optional)
        partitionFunction:  pointer to partition function (default is PYTIPS) (optional)
        Environment:  dictionary containing thermodynamic parameters.
                        'p' - pressure in atmospheres,
                        'T' - temperature in Kelvin
                        Default={'p':1.,'T':296.}
        WavenumberRange:  wavenumber range to consider.
        WavenumberStep:   wavenumber step to consider.
        WavenumberWing:   absolute wing for calculating a lineshape (in cm-1)
        WavenumberWingHW:  relative wing for calculating a lineshape (in halfwidths)
        IntensityThreshold:  threshold for intensities
        GammaL:  specifies broadening parameter ('gamma_air' or 'gamma_self')
        HITRAN_units:  use cm2/molecule (True) or cm-1 (False) for absorption coefficient
        File:   write output to file (if specified)
        Format:  c-format of file output (accounts for significant digits in WavenumberStep)
    OUTPUT PARAMETERS:
        Wavenum: wavenumber grid with respect to parameters WavenumberRange and WavenumberStep
        Xsect: absorption coefficient calculated on the grid
    ---
    DESCRIPTION:
        Calculate absorption coefficient using SDVoigt profile.
        Absorption coefficient is calculated at arbitrary temperature and pressure.
        User can vary a wide range of parameters to control a process of calculation.
        The choise of these parameters depends on properties of a particular linelist.
        Default values are a sort of guess which gives a decent precision (on average)
        for a reasonable amount of cpu time. To increase calculation accuracy,
        user should use a trial and error method.
    ---
    EXAMPLE OF USAGE:
        nu,coef = absorptionCoefficient_SDVoigt(((2,1),),'co2',WavenumberStep=0.01,
                                              HITRAN_units=False,GammaL='gamma_self')
    ---
    """

    # warn('To get the most up-to-date version of SDVoigt please check http://hitran.org/hapi. This version is customized by Yang et al 2018')

    # Paremeters OmegaRange,OmegaStep,OmegaWing,OmegaWingHW, and OmegaGrid
    # are deprecated and given for backward compatibility with the older versions.
    if WavenumberRange:  OmegaRange=WavenumberRange
    if WavenumberStep:   OmegaStep=WavenumberStep
    if WavenumberWing:   OmegaWing=WavenumberWing
    if WavenumberWingHW: OmegaWingHW=WavenumberWingHW
    if WavenumberGrid:   OmegaGrid=WavenumberGrid

    # "bug" with 1-element list
    Components = listOfTuples(Components)
    SourceTables = listOfTuples(SourceTables)

    # determine final input values
    Components,SourceTables,Environment,OmegaRange,OmegaStep,OmegaWing,\
    IntensityThreshold,Format = \
       getDefaultValuesForXsect(Components,SourceTables,Environment,OmegaRange,
                                OmegaStep,OmegaWing,IntensityThreshold,Format)

    # warn user about too large omega step
    if OmegaStep>0.1: warn('Big wavenumber step: possible accuracy decline')

    # get uniform linespace for cross-section
    #number_of_points = (OmegaRange[1]-OmegaRange[0])/OmegaStep + 1
    #Omegas = linspace(OmegaRange[0],OmegaRange[1],number_of_points)
    if OmegaGrid is not None:
        Omegas = npsort(OmegaGrid)
    else:
        #Omegas = arange(OmegaRange[0],OmegaRange[1],OmegaStep)
        Omegas = arange_(OmegaRange[0],OmegaRange[1],OmegaStep) # fix
    number_of_points = len(Omegas)
    Xsect = zeros(number_of_points)

    # reference temperature and pressure
    Tref = __FloatType__(296.) # K
    pref = __FloatType__(1.) # atm

    # actual temperature and pressure
    T = Environment['T'] # K
    p = Environment['p'] # atm

    # create dictionary from Components
    ABUNDANCES = {}
    NATURAL_ABUNDANCES = {}
    for Component in Components:
        M = Component[0]
        I = Component[1]
        if len(Component) >= 3:
            ni = Component[2]
        else:
            try:
                ni = ISO[(M,I)][ISO_INDEX['abundance']]
            except KeyError:
                raise Exception('cannot find component M,I = %d,%d.' % (M,I))
        ABUNDANCES[(M,I)] = ni
        NATURAL_ABUNDANCES[(M,I)] = ISO[(M,I)][ISO_INDEX['abundance']]

    # precalculation of volume concentration
    if HITRAN_units:
        factor = __FloatType__(1.0)
    else:
        factor = volumeConcentration(p,T)

    # setup the default empty environment dependence function
    if not EnvDependences:
        EnvDependences = lambda ENV,LINE:{}
    Env = Environment.copy()
    Env['Tref'] = Tref
    Env['pref'] = pref

    # setup the Diluent variable
    GammaL = GammaL.lower()
    if not Diluent:
        if GammaL == 'gamma_air':
            Diluent = {'air':1.}
        elif GammaL == 'gamma_self':
            Diluent = {'self':1.}
        else:
            raise Exception('Unknown GammaL value: %s' % GammaL)

    # Simple check
    for key in Diluent:
        val = Diluent[key]
        if val < 0 and val > 1:
            raise Exception('Diluent fraction must be in [0,1]')

    # SourceTables contain multiple tables
    for TableName in SourceTables:

        # get the number of rows
        nline = LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']

        # get parameter names for each table
        parnames = LOCAL_TABLE_CACHE[TableName]['data'].keys()

        # loop through line centers (single stream)
        for RowID in range(nline):

            # Get the custom environment dependences
            Line = {}
            for parname in parnames:
                Line[parname] = LOCAL_TABLE_CACHE[TableName]['data'][parname][RowID]
            CustomEnvDependences = EnvDependences(Env,Line)

            # get basic line parameters (lower level)
            LineCenterDB = LOCAL_TABLE_CACHE[TableName]['data']['nu'][RowID]
            LineIntensityDB = LOCAL_TABLE_CACHE[TableName]['data']['sw'][RowID]
            LowerStateEnergyDB = LOCAL_TABLE_CACHE[TableName]['data']['elower'][RowID]
            MoleculeNumberDB = LOCAL_TABLE_CACHE[TableName]['data']['molec_id'][RowID]
            IsoNumberDB = LOCAL_TABLE_CACHE[TableName]['data']['local_iso_id'][RowID]

            # filter by molecule and isotopologue
            if (MoleculeNumberDB,IsoNumberDB) not in ABUNDANCES: continue

            # partition functions for T and Tref
            SigmaT = partitionFunction(MoleculeNumberDB,IsoNumberDB,T)
            SigmaTref = partitionFunction(MoleculeNumberDB,IsoNumberDB,Tref)

            # get all environment dependences from voigt parameters

            #   intensity
            if 'sw' in CustomEnvDependences:
                LineIntensity = CustomEnvDependences['sw']
            else:
                LineIntensity = EnvironmentDependency_Intensity(LineIntensityDB,T,Tref,SigmaT,SigmaTref,
                                                                LowerStateEnergyDB,LineCenterDB)

            #   FILTER by LineIntensity: compare it with IntencityThreshold
            if LineIntensity < IntensityThreshold: continue

            #   doppler broadening coefficient (GammaD)
            cMassMol = 1.66053873e-27 # hapi
            m = molecularMass(MoleculeNumberDB,IsoNumberDB) * cMassMol * 1000
            GammaD = sqrt(2*cBolts*T*log(2)/m/cc**2)*LineCenterDB

            #   pressure broadening coefficient
            Gamma0 = 0.; Shift0 = 0.; Gamma2 = 0.; Shift2 = 0.
            for species in Diluent:
                species_lower = species.lower()

                abun = Diluent[species]

                gamma_name = 'gamma_' + species_lower
                try:
                    Gamma0DB = LOCAL_TABLE_CACHE[TableName]['data'][gamma_name][RowID]
                except:
                    Gamma0DB = 0.0

                n_name = 'n_' + species_lower
                try:
                    TempRatioPowerDB = LOCAL_TABLE_CACHE[TableName]['data'][n_name][RowID]
                    if species_lower == 'self' and TempRatioPowerDB == 0.:
                        TempRatioPowerDB = LOCAL_TABLE_CACHE[TableName]['data']['n_air'][RowID] # same for self as for air
                except:
                    #TempRatioPowerDB = 0
                    TempRatioPowerDB = LOCAL_TABLE_CACHE[TableName]['data']['n_air'][RowID]

                # Add to the final Gamma0
                Gamma0 += abun*CustomEnvDependences.get(gamma_name, # default ->
                          EnvironmentDependency_Gamma0(Gamma0DB,T,Tref,p,pref,TempRatioPowerDB))

                delta_name = 'delta_' + species_lower
                try:
                    Shift0DB = LOCAL_TABLE_CACHE[TableName]['data'][delta_name][RowID]
                except:
                    Shift0DB = 0.0

                # Nate Malarich pld_update 06/06/2019, select linear or power-law shift model
                deltap_name = 'deltap_' + species_lower
                # try:
                #     deltap = LOCAL_TABLE_CACHE[TableName]['data'][deltap_name][RowID]
                # except:
                #     deltap = 0.0

                deltap = 0.0
                try:
                    deltap = LOCAL_TABLE_CACHE[TableName]['data'][deltap_name][RowID]
                    power_law_shift = False
                except KeyError:
                    power_law_shift = True

                # For lineshift consistent with Labfit
                # If deltap information not available, get custom n_delta_air (default 1 or 0?)
                if power_law_shift is False:
                    Shift0 += abun*CustomEnvDependences.get(delta_name, # default ->
                            ((Shift0DB + deltap*(T-Tref))*p/pref))
                else:
                    # PARAMETER_META doesn't have any keys for shift temperature-exponents, stuck with hardcode
                    try:
                        n_delta = LOCAL_TABLE_CACHE[TableName]['data']['n_delta_' + species_lower][RowID]
                    except:
                        n_delta = 1
                    Shift0 += abun*CustomEnvDependences.get(delta_name,
                                (Shift0DB * (Tref/T)**n_delta * p))
                # End pld_update

                SD_name = 'sd_' + species_lower
                try:
                    SDDB = LOCAL_TABLE_CACHE[TableName]['data'][SD_name][RowID]
                except:
                    SDDB = 0.0

                # pld_update 06/06/2019 Nate Malarich
                # add temperature-scaling to speed-dependence
                Gamma2 += abun*CustomEnvDependences.get(SD_name,
                           SDDB * EnvironmentDependency_Gamma0(Gamma0DB,T,Tref,p,pref,TempRatioPowerDB))
                # end pld_update

            #   get final wing of the line according to Gamma0, OmegaWingHW and OmegaWing
            OmegaWingF = max(OmegaWing,OmegaWingHW*Gamma0,OmegaWingHW*GammaD)

            BoundIndexLower = bisect(Omegas,LineCenterDB-OmegaWingF)
            BoundIndexUpper = bisect(Omegas,LineCenterDB+OmegaWingF)
            try:
                lineshape_vals = PROFILE_SDVOIGT(LineCenterDB,GammaD,Gamma0,Gamma2,Shift0,Shift2,Omegas[BoundIndexLower:BoundIndexUpper])[0]
            except IndexError:
                lineshape_vals = PROFILE_SDVOIGT(LineCenterDB,GammaD,Gamma0,Gamma2,Shift0,Shift2,Omegas[BoundIndexLower:BoundIndexUpper])[0]
            Xsect[BoundIndexLower:BoundIndexUpper] += factor / NATURAL_ABUNDANCES[(MoleculeNumberDB,IsoNumberDB)] * \
                                                      ABUNDANCES[(MoleculeNumberDB,IsoNumberDB)] * \
                                                      LineIntensity * lineshape_vals

    if File: save_to_file(File,Format,Omegas,Xsect)
    return Omegas,Xsect

# Want to have verbose=False as optional parameter
# then if verbose: look through all relevant parameters, see whether they exist
# and if they exist, if the value is ever not zero.
# Do this outside the line-by-line loop, so you only write once.
def absorptionCoefficient_Voigt(Components=None,SourceTables=None,partitionFunction=PYTIPS,
                                Environment=None,OmegaRange=None,OmegaStep=None,OmegaWing=None,
                                IntensityThreshold=DefaultIntensityThreshold,
                                OmegaWingHW=DefaultOmegaWingHW,
                                GammaL='gamma_air', HITRAN_units=True, LineShift=True,
                                File=None, Format=None, OmegaGrid=None,
                                WavenumberRange=None,WavenumberStep=None,WavenumberWing=None,
                                WavenumberWingHW=None,WavenumberGrid=None,
                                Diluent={},EnvDependences=None):
    """
    INPUT PARAMETERS:
        Components:  list of tuples [(M,I,D)], where
                        M - HITRAN molecule number,
                        I - HITRAN isotopologue number,
                        D - relative abundance (optional)
        SourceTables:  list of tables from which to calculate cross-section   (optional)
        partitionFunction:  pointer to partition function (default is PYTIPS) (optional)
        Environment:  dictionary containing thermodynamic parameters.
                        'p' - pressure in atmospheres,
                        'T' - temperature in Kelvin
                        Default={'p':1.,'T':296.}
        WavenumberRange:  wavenumber range to consider.
        WavenumberStep:   wavenumber step to consider.
        WavenumberWing:   absolute wing for calculating a lineshape (in cm-1)
        WavenumberWingHW:  relative wing for calculating a lineshape (in halfwidths)
        GammaL:  specifies broadening parameter ('gamma_air' or 'gamma_self')
        HITRAN_units:  use cm2/molecule (True) or cm-1 (False) for absorption coefficient
        File:   write output to file (if specified)
        Format:  c-format of file output (accounts for significant digits in WavenumberStep)
    OUTPUT PARAMETERS:
        Wavenum: wavenumber grid with respect to parameters WavenumberRange and WavenumberStep
        Xsect: absorption coefficient calculated on the grid
    ---
    DESCRIPTION:
        Calculate absorption coefficient using Voigt profile.
        Absorption coefficient is calculated at arbitrary temperature and pressure.
        User can vary a wide range of parameters to control a process of calculation.
        The choise of these parameters depends on properties of a particular linelist.
        Default values are a sort of guess which gives a decent precision (on average)
        for a reasonable amount of cpu time. To increase calculation accuracy,
        user should use a trial and error method.
    ---
    EXAMPLE OF USAGE:
        nu,coef = absorptionCoefficient_Voigt(((2,1),),'co2',WavenumberStep=0.01,
                                              HITRAN_units=False,GammaL='gamma_self')
    ---
    """

    # Paremeters OmegaRange,OmegaStep,OmegaWing,OmegaWingHW, and OmegaGrid
    # are deprecated and given for backward compatibility with the older versions.
    if WavenumberRange:  OmegaRange=WavenumberRange
    if WavenumberStep:   OmegaStep=WavenumberStep
    if WavenumberWing:   OmegaWing=WavenumberWing
    if WavenumberWingHW: OmegaWingHW=WavenumberWingHW
    if WavenumberGrid:   OmegaGrid=WavenumberGrid

    # "bug" with 1-element list
    Components = listOfTuples(Components)
    SourceTables = listOfTuples(SourceTables)

    # determine final input values
    Components,SourceTables,Environment,OmegaRange,OmegaStep,OmegaWing,\
    IntensityThreshold,Format = \
       getDefaultValuesForXsect(Components,SourceTables,Environment,OmegaRange,
                                OmegaStep,OmegaWing,IntensityThreshold,Format)

    # warn user about too large omega step
    if OmegaStep>0.1: warn('Big wavenumber step: possible accuracy decline')

    # get uniform linespace for cross-section
    #number_of_points = (OmegaRange[1]-OmegaRange[0])/OmegaStep + 1
    #Omegas = linspace(OmegaRange[0],OmegaRange[1],number_of_points)
    if OmegaGrid is not None:
        Omegas = npsort(OmegaGrid)
    else:
        #Omegas = arange(OmegaRange[0],OmegaRange[1],OmegaStep)
        Omegas = arange_(OmegaRange[0],OmegaRange[1],OmegaStep) # fix
    number_of_points = len(Omegas)
    Xsect = zeros(number_of_points)

    # reference temperature and pressure
    Tref = __FloatType__(296.) # K
    pref = __FloatType__(1.) # atm

    # actual temperature and pressure
    T = Environment['T'] # K
    p = Environment['p'] # atm

    # create dictionary from Components
    ABUNDANCES = {}
    NATURAL_ABUNDANCES = {}
    for Component in Components:
        M = Component[0]
        I = Component[1]
        if len(Component) >= 3:
            ni = Component[2]
        else:
            try:
                ni = ISO[(M,I)][ISO_INDEX['abundance']]
            except KeyError:
                raise Exception('cannot find component M,I = %d,%d.' % (M,I))
        ABUNDANCES[(M,I)] = ni
        NATURAL_ABUNDANCES[(M,I)] = ISO[(M,I)][ISO_INDEX['abundance']]

    # precalculation of volume concentration
    if HITRAN_units:
        factor = __FloatType__(1.0)
    else:
        factor = volumeConcentration(p,T)

    # setup the default empty environment dependence function
    if not EnvDependences:
        EnvDependences = lambda ENV,LINE:{}
    Env = Environment.copy()
    Env['Tref'] = Tref
    Env['pref'] = pref

    # setup the Diluent variable
    GammaL = GammaL.lower()
    if not Diluent:
        if GammaL == 'gamma_air':
            Diluent = {'air':1.}
        elif GammaL == 'gamma_self':
            Diluent = {'self':1.}
        else:
            raise Exception('Unknown GammaL value: %s' % GammaL)

    # Simple check
    for key in Diluent:
        val = Diluent[key]
        if val < 0 and val > 1:
            raise Exception('Diluent fraction must be in [0,1]')

    # SourceTables contain multiple tables
    for TableName in SourceTables:

        # get the number of rows
        nline = LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']

        # get parameter names for each table
        parnames = LOCAL_TABLE_CACHE[TableName]['data'].keys()

        # loop through line centers (single stream)
        for RowID in range(nline):

            # Get the custom environment dependences
            Line = {}
            for parname in parnames:
                Line[parname] = LOCAL_TABLE_CACHE[TableName]['data'][parname][RowID]
            CustomEnvDependences = EnvDependences(Env,Line)

            # get basic line parameters (lower level)
            LineCenterDB = LOCAL_TABLE_CACHE[TableName]['data']['nu'][RowID]
            LineIntensityDB = LOCAL_TABLE_CACHE[TableName]['data']['sw'][RowID]
            LowerStateEnergyDB = LOCAL_TABLE_CACHE[TableName]['data']['elower'][RowID]
            MoleculeNumberDB = LOCAL_TABLE_CACHE[TableName]['data']['molec_id'][RowID]
            IsoNumberDB = LOCAL_TABLE_CACHE[TableName]['data']['local_iso_id'][RowID]

            # filter by molecule and isotopologue
            if (MoleculeNumberDB,IsoNumberDB) not in ABUNDANCES: continue

            # partition functions for T and Tref
            SigmaT = partitionFunction(MoleculeNumberDB,IsoNumberDB,T)
            SigmaTref = partitionFunction(MoleculeNumberDB,IsoNumberDB,Tref)

            # get all environment dependences from voigt parameters

            #   intensity
            if 'sw' in CustomEnvDependences:
                LineIntensity = CustomEnvDependences['sw']
            else:
                LineIntensity = EnvironmentDependency_Intensity(LineIntensityDB,T,Tref,SigmaT,SigmaTref,
                                                                LowerStateEnergyDB,LineCenterDB)

            #   FILTER by LineIntensity: compare it with IntencityThreshold
            if LineIntensity < IntensityThreshold: continue

            #   doppler broadening coefficient (GammaD)
            cMassMol = 1.66053873e-27 # hapi
            m = molecularMass(MoleculeNumberDB,IsoNumberDB) * cMassMol * 1000
            GammaD = sqrt(2*cBolts*T*log(2)/m/cc**2)*LineCenterDB

            #   pressure broadening coefficient
            Gamma0 = 0.; Shift0 = 0.;
            for species in Diluent:
                species_lower = species.lower()

                abun = Diluent[species]

                gamma_name = 'gamma_' + species_lower
                try:
                    Gamma0DB = LOCAL_TABLE_CACHE[TableName]['data'][gamma_name][RowID]
                except:
                    Gamma0DB = 0.0

                n_name = 'n_' + species_lower
                try:
                    TempRatioPowerDB = LOCAL_TABLE_CACHE[TableName]['data'][n_name][RowID]
                    if species_lower == 'self' and TempRatioPowerDB == 0.:
                        TempRatioPowerDB = LOCAL_TABLE_CACHE[TableName]['data']['n_air'][RowID] # same for self as for air
                except:
                    #TempRatioPowerDB = 0
                    TempRatioPowerDB = LOCAL_TABLE_CACHE[TableName]['data']['n_air'][RowID]

                # Add to the final Gamma0
                Gamma0 += abun*CustomEnvDependences.get(gamma_name, # default ->
                          EnvironmentDependency_Gamma0(Gamma0DB,T,Tref,p,pref,TempRatioPowerDB))

                delta_name = 'delta_' + species_lower
                try:
                    Shift0DB = LOCAL_TABLE_CACHE[TableName]['data'][delta_name][RowID]
                except:
                    Shift0DB = 0.0


                # pld_update 06/06/2019, select linear or power-law shift model
                deltap_name = 'deltap_' + species_lower
                # try:
                #     deltap = LOCAL_TABLE_CACHE[TableName]['data'][deltap_name][RowID]
                # except:
                #     deltap = 0.0

                deltap = 0.0
                try:
                    deltap = LOCAL_TABLE_CACHE[TableName]['data'][deltap_name][RowID]
                    power_law_shift = False
                except KeyError:
                    power_law_shift = True

                # For lineshift consistent with Labfit
                # If deltap information not available, get custom n_delta_air (default 1 or 0?)
                if power_law_shift is False:
                    Shift0 += abun*CustomEnvDependences.get(delta_name, # default ->
                            ((Shift0DB + deltap*(T-Tref))*p/pref))
                else:
                    # PARAMETER_META doesn't have any keys for shift temperature-exponents, stuck with hardcode
                    try:
                        n_delta = LOCAL_TABLE_CACHE[TableName]['data']['n_delta_' + species_lower][RowID]
                    except:
                        n_delta = 1
                    Shift0 += abun*CustomEnvDependences.get(delta_name,
                                (Shift0DB * (Tref/T)**n_delta * p))
                # End pld_update


            #   get final wing of the line according to Gamma0, OmegaWingHW and OmegaWing
            OmegaWingF = max(OmegaWing,OmegaWingHW*Gamma0,OmegaWingHW*GammaD)

            BoundIndexLower = bisect(Omegas,LineCenterDB-OmegaWingF)
            BoundIndexUpper = bisect(Omegas,LineCenterDB+OmegaWingF)
            lineshape_vals = PROFILE_VOIGT(LineCenterDB+Shift0,GammaD,Gamma0,Omegas[BoundIndexLower:BoundIndexUpper])[0]
            Xsect[BoundIndexLower:BoundIndexUpper] += factor / NATURAL_ABUNDANCES[(MoleculeNumberDB,IsoNumberDB)] * \
                                                      ABUNDANCES[(MoleculeNumberDB,IsoNumberDB)] * \
                                                      LineIntensity * lineshape_vals

    if File: save_to_file(File,Format,Omegas,Xsect)
    return Omegas,Xsect

def absorptionCoefficient_Lorentz(Components=None,SourceTables=None,partitionFunction=PYTIPS2017,
                                Environment=None,OmegaRange=None,OmegaStep=None,OmegaWing=None,
                                IntensityThreshold=DefaultIntensityThreshold,
                                OmegaWingHW=DefaultOmegaWingHW,
                                GammaL='gamma_air', HITRAN_units=True, LineShift=True,
                                File=None, Format=None, OmegaGrid=None,
                                WavenumberRange=None,WavenumberStep=None,WavenumberWing=None,
                                WavenumberWingHW=None,WavenumberGrid=None,
                                Diluent={},EnvDependences=None):
    """
    INPUT PARAMETERS: 
        Components:  list of tuples [(M,I,D)], where
                        M - HITRAN molecule number,
                        I - HITRAN isotopologue number,
                        D - relative abundance (optional)
        SourceTables:  list of tables from which to calculate cross-section   (optional)
        partitionFunction:  pointer to partition function (default is PYTIPS) (optional)
        Environment:  dictionary containing thermodynamic parameters.
                        'p' - pressure in atmospheres,
                        'T' - temperature in Kelvin
                        Default={'p':1.,'T':296.}
        WavenumberRange:  wavenumber range to consider.
        WavenumberStep:   wavenumber step to consider. 
        WavenumberWing:   absolute wing for calculating a lineshape (in cm-1) 
        WavenumberWingHW:  relative wing for calculating a lineshape (in halfwidths)
        IntensityThreshold:  threshold for intensities
        GammaL:  specifies broadening parameter ('gamma_air' or 'gamma_self')
        HITRAN_units:  use cm2/molecule (True) or cm-1 (False) for absorption coefficient
        File:   write output to file (if specified)
        Format:  c-format of file output (accounts for significant digits in WavenumberStep)
    OUTPUT PARAMETERS: 
        Wavenum: wavenumber grid with respect to parameters WavenumberRange and WavenumberStep
        Xsect: absorption coefficient calculated on the grid
    ---
    DESCRIPTION:
        Calculate absorption coefficient using Lorentz profile.
        Absorption coefficient is calculated at arbitrary temperature and pressure.
        User can vary a wide range of parameters to control a process of calculation.
        The choise of these parameters depends on properties of a particular linelist.
        Default values are a sort of guess which gives a decent precision (on average) 
        for a reasonable amount of cpu time. To increase calculation accuracy,
        user should use a trial and error method.
    ---
    EXAMPLE OF USAGE:
        nu,coef = absorptionCoefficient_Lorentz(((2,1),),'co2',WavenumberStep=0.01,
                                              HITRAN_units=False,GammaL='gamma_self')
    ---
    """
   
    # Paremeters OmegaRange,OmegaStep,OmegaWing,OmegaWingHW, and OmegaGrid
    # are deprecated and given for backward compatibility with the older versions.
    if WavenumberRange:  OmegaRange=WavenumberRange
    if WavenumberStep:   OmegaStep=WavenumberStep
    if WavenumberWing:   OmegaWing=WavenumberWing
    if WavenumberWingHW: OmegaWingHW=WavenumberWingHW
    if WavenumberGrid:   OmegaGrid=WavenumberGrid

    # "bug" with 1-element list
    Components = listOfTuples(Components)
    SourceTables = listOfTuples(SourceTables)
    
    # determine final input values
    Components,SourceTables,Environment,OmegaRange,OmegaStep,OmegaWing,\
    IntensityThreshold,Format = \
       getDefaultValuesForXsect(Components,SourceTables,Environment,OmegaRange,
                                OmegaStep,OmegaWing,IntensityThreshold,Format)
    
    # warn user about too large omega step
    if OmegaStep>0.1: warn('Big wavenumber step: possible accuracy decline')

    # get uniform linespace for cross-section
    #number_of_points = (OmegaRange[1]-OmegaRange[0])/OmegaStep + 1
    #Omegas = linspace(OmegaRange[0],OmegaRange[1],number_of_points)
    if OmegaGrid is not None:
        Omegas = npsort(OmegaGrid)
    else:
        #Omegas = arange(OmegaRange[0],OmegaRange[1],OmegaStep)
        Omegas = arange_(OmegaRange[0],OmegaRange[1],OmegaStep) # fix
    number_of_points = len(Omegas)
    Xsect = zeros(number_of_points)
       
    # reference temperature and pressure
    Tref = __FloatType__(296.) # K
    pref = __FloatType__(1.) # atm
    
    # actual temperature and pressure
    T = Environment['T'] # K
    p = Environment['p'] # atm
       
    # create dictionary from Components
    ABUNDANCES = {}
    NATURAL_ABUNDANCES = {}
    for Component in Components:
        M = Component[0]
        I = Component[1]
        if len(Component) >= 3:
            ni = Component[2]
        else:
            try:
                ni = ISO[(M,I)][ISO_INDEX['abundance']]
            except KeyError:
                raise Exception('cannot find component M,I = %d,%d.' % (M,I))
        ABUNDANCES[(M,I)] = ni
        NATURAL_ABUNDANCES[(M,I)] = ISO[(M,I)][ISO_INDEX['abundance']]
        
    # precalculation of volume concentration
    if HITRAN_units:
        factor = __FloatType__(1.0)
    else:
        factor = volumeConcentration(p,T) 
        
    # setup the default empty environment dependence function
    if not EnvDependences:
        EnvDependences = lambda ENV,LINE:{}
    Env = Environment.copy()
    Env['Tref'] = Tref
    Env['pref'] = pref
  
    # setup the Diluent variable
    GammaL = GammaL.lower()
    if not Diluent:
        if GammaL == 'gamma_air':
            Diluent = {'air':1.}
        elif GammaL == 'gamma_self':
            Diluent = {'self':1.}
        else:
            raise Exception('Unknown GammaL value: %s' % GammaL)
        
    # Simple check
    print(Diluent)  # Added print statement # CHANGED RJH 23MAR18  # Simple check
    for key in Diluent:
        val = Diluent[key]
        if val < 0 or val > 1: # if val < 0 and val > 1:# CHANGED RJH 23MAR18
            raise Exception('Diluent fraction must be in [0,1]')
    
    # SourceTables contain multiple tables
    for TableName in SourceTables:

        # get the number of rows
        nline = LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']
        
        # get parameter names for each table
        parnames = LOCAL_TABLE_CACHE[TableName]['data'].keys()
        
        # loop through line centers (single stream)
        for RowID in range(nline):
            
            # Get the custom environment dependences
            Line = {}
            for parname in parnames:
                Line[parname] = LOCAL_TABLE_CACHE[TableName]['data'][parname][RowID]
            CustomEnvDependences = EnvDependences(Env,Line)
            
            # get basic line parameters (lower level)
            LineCenterDB = LOCAL_TABLE_CACHE[TableName]['data']['nu'][RowID]
            LineIntensityDB = LOCAL_TABLE_CACHE[TableName]['data']['sw'][RowID]
            LowerStateEnergyDB = LOCAL_TABLE_CACHE[TableName]['data']['elower'][RowID]
            MoleculeNumberDB = LOCAL_TABLE_CACHE[TableName]['data']['molec_id'][RowID]
            IsoNumberDB = LOCAL_TABLE_CACHE[TableName]['data']['local_iso_id'][RowID]
            
            # filter by molecule and isotopologue
            if (MoleculeNumberDB,IsoNumberDB) not in ABUNDANCES: continue
            
            # partition functions for T and Tref
            SigmaT = partitionFunction(MoleculeNumberDB,IsoNumberDB,T)
            SigmaTref = partitionFunction(MoleculeNumberDB,IsoNumberDB,Tref)
            
            # get all environment dependences from voigt parameters
            
            #   intensity
            if 'sw' in CustomEnvDependences:
                LineIntensity = CustomEnvDependences['sw']
            else:
                LineIntensity = EnvironmentDependency_Intensity(LineIntensityDB,T,Tref,SigmaT,SigmaTref,
                                                                LowerStateEnergyDB,LineCenterDB)
            
            #   FILTER by LineIntensity: compare it with IntencityThreshold
            if LineIntensity < IntensityThreshold: continue
                       
            #   pressure broadening coefficient
            Gamma0 = 0.; Shift0 = 0.;
            for species in Diluent:
                species_lower = species # species_lower = species.lower() # CHANGED RJH 23MAR18
                
                abun = Diluent[species]
                
                gamma_name = 'gamma_' + species_lower
                try:
                    Gamma0DB = LOCAL_TABLE_CACHE[TableName]['data'][gamma_name][RowID]
                except:
                    Gamma0DB = 0.0
                
                n_name = 'n_' + species_lower
                try:
                    TempRatioPowerDB = LOCAL_TABLE_CACHE[TableName]['data'][n_name][RowID]
                    if species_lower == 'self' and TempRatioPowerDB == 0.:
                        TempRatioPowerDB = LOCAL_TABLE_CACHE[TableName]['data']['n_air'][RowID] # same for self as for air
                except:
                    #TempRatioPowerDB = 0                    
                    TempRatioPowerDB = LOCAL_TABLE_CACHE[TableName]['data']['n_air'][RowID]
                
                # Add to the final Gamma0
                Gamma0 += abun*CustomEnvDependences.get(gamma_name, # default ->
                          EnvironmentDependency_Gamma0(Gamma0DB,T,Tref,p,pref,TempRatioPowerDB))

                delta_name = 'delta_' + species_lower
                try:
                    Shift0DB = LOCAL_TABLE_CACHE[TableName]['data'][delta_name][RowID]
                except:
                    Shift0DB = 0.0
                
                deltap_name = 'deltap_' + species_lower
                try:
                    deltap = LOCAL_TABLE_CACHE[TableName]['data'][deltap_name][RowID]
                except:
                    deltap = 0.0

                Shift0 += abun*CustomEnvDependences.get(delta_name, # default ->
                          ((Shift0DB + deltap*(T-Tref))*p/pref))
            
            #   get final wing of the line according to Gamma0, OmegaWingHW and OmegaWing
            OmegaWingF = max(OmegaWing,OmegaWingHW*Gamma0)

            BoundIndexLower = bisect(Omegas,LineCenterDB-OmegaWingF)
            BoundIndexUpper = bisect(Omegas,LineCenterDB+OmegaWingF)
            lineshape_vals = PROFILE_LORENTZ(LineCenterDB+Shift0,Gamma0,Omegas[BoundIndexLower:BoundIndexUpper])
            Xsect[BoundIndexLower:BoundIndexUpper] += factor / NATURAL_ABUNDANCES[(MoleculeNumberDB,IsoNumberDB)] * \
                                                      ABUNDANCES[(MoleculeNumberDB,IsoNumberDB)] * \
                                                      LineIntensity * lineshape_vals
    
    if File: save_to_file(File,Format,Omegas,Xsect)
    return Omegas,Xsect
    
# Alias for a profile selector
#absorptionCoefficient = absorptionCoefficient_HT
    
# ==========================================================================================
# =========================== /NEW ABSORPTION COEFFICIENT ===================================
# ==========================================================================================    

# calculate apsorption for Doppler profile
def absorptionCoefficient_Doppler(Components=None,SourceTables=None,partitionFunction=PYTIPS2017,
                                  Environment=None,OmegaRange=None,OmegaStep=None,OmegaWing=None,
                                  IntensityThreshold=DefaultIntensityThreshold,
                                  OmegaWingHW=DefaultOmegaWingHW,
                                  ParameterBindings=DefaultParameterBindings,
                                  EnvironmentDependencyBindings=DefaultEnvironmentDependencyBindings,
                                  GammaL='dummy', HITRAN_units=True, LineShift=True,
                                  File=None, Format=None, OmegaGrid=None,
                                  WavenumberRange=None,WavenumberStep=None,WavenumberWing=None,
                                  WavenumberWingHW=None,WavenumberGrid=None,Diluent=None):   
    """
    INPUT PARAMETERS: 
        Components:  list of tuples [(M,I,D)], where
                        M - HITRAN molecule number,
                        I - HITRAN isotopologue number,
                        D - abundance (optional)
        SourceTables:  list of tables from which to calculate cross-section   (optional)
        partitionFunction:  pointer to partition function (default is PYTIPS) (optional)
        Environment:  dictionary containing thermodynamic parameters.
                        'p' - pressure in atmospheres,
                        'T' - temperature in Kelvin
                        Default={'p':1.,'T':296.}
        WavenumberRange:  wavenumber range to consider.
        WavenumberStep:   wavenumber step to consider. 
        WavenumberWing:   absolute wing for calculating a lineshape (in cm-1) 
        WavenumberWingHW:  relative wing for calculating a lineshape (in halfwidths)
        IntensityThreshold:  threshold for intensities
        GammaL:  specifies broadening parameter ('gamma_air' or 'gamma_self')
        HITRAN_units:  use cm2/molecule (True) or cm-1 (False) for absorption coefficient
        File:   write output to file (if specified)
        Format:  c-format of file output (accounts for significant digits in WavenumberStep)
    OUTPUT PARAMETERS: 
        Wavenum: wavenumber grid with respect to parameters OmegaRange and OmegaStep
        Xsect: absorption coefficient calculated on the grid
    ---
    DESCRIPTION:
        Calculate absorption coefficient using Doppler (Gauss) profile.
        Absorption coefficient is calculated at arbitrary temperature and pressure.
        User can vary a wide range of parameters to control a process of calculation.
        The choise of these parameters depends on properties of a particular linelist.
        Default values are a sort of guess which give a decent precision (on average) 
        for a reasonable amount of cpu time. To increase calculation accuracy,
        user should use a trial and error method.
    ---
    EXAMPLE OF USAGE:
        nu,coef = absorptionCoefficient_Doppler(((2,1),),'co2',WavenumberStep=0.01,
                                              HITRAN_units=False,GammaL='gamma_self')
    ---
    """

    if WavenumberRange:  OmegaRange=WavenumberRange
    if WavenumberStep:   OmegaStep=WavenumberStep
    if WavenumberWing:   OmegaWing=WavenumberWing
    if WavenumberWingHW: OmegaWingHW=WavenumberWingHW
    if WavenumberGrid:   OmegaGrid=WavenumberGrid
    
    # "bug" with 1-element list
    Components = listOfTuples(Components)
    SourceTables = listOfTuples(SourceTables)
    
    # determine final input values
    Components,SourceTables,Environment,OmegaRange,OmegaStep,OmegaWing,\
    IntensityThreshold,Format = \
       getDefaultValuesForXsect(Components,SourceTables,Environment,OmegaRange,
                                OmegaStep,OmegaWing,IntensityThreshold,Format)
    # special for Doppler case: set OmegaStep to a smaller value
    if not OmegaStep: OmegaStep = 0.001
                
    # warn user about too large omega step
    if OmegaStep>0.005: warn('Big wavenumber step: possible accuracy decline')

    # get uniform linespace for cross-section
    #number_of_points = (OmegaRange[1]-OmegaRange[0])/OmegaStep + 1
    #Omegas = linspace(OmegaRange[0],OmegaRange[1],number_of_points)
    if OmegaGrid is not None:
        Omegas = npsort(OmegaGrid)
    else:
        #Omegas = arange(OmegaRange[0],OmegaRange[1],OmegaStep)
        Omegas = arange_(OmegaRange[0],OmegaRange[1],OmegaStep) # fix
    number_of_points = len(Omegas)
    Xsect = zeros(number_of_points)
       
    # reference temperature and pressure
    Tref = __FloatType__(296.) # K
    pref = __FloatType__(1.) # atm
    
    # actual temperature and pressure
    T = Environment['T'] # K
    p = Environment['p'] # atm
       
    # create dictionary from Components
    ABUNDANCES = {}
    NATURAL_ABUNDANCES = {}
    for Component in Components:
        M = Component[0]
        I = Component[1]
        if len(Component) >= 3:
            ni = Component[2]
        else:
            try:
                ni = ISO[(M,I)][ISO_INDEX['abundance']]
            except KeyError:
                raise Exception('cannot find component M,I = %d,%d.' % (M,I))
        ABUNDANCES[(M,I)] = ni
        NATURAL_ABUNDANCES[(M,I)] = ISO[(M,I)][ISO_INDEX['abundance']]
        
    # precalculation of volume concentration
    if HITRAN_units:
        factor = __FloatType__(1.0)
    else:
        factor = volumeConcentration(p,T) 
        
    # SourceTables contain multiple tables
    for TableName in SourceTables:

        # get line centers
        nline = LOCAL_TABLE_CACHE[TableName]['header']['number_of_rows']
        
        # loop through line centers (single stream)
        for RowID in range(nline):
            
            # get basic line parameters (lower level)
            LineCenterDB = LOCAL_TABLE_CACHE[TableName]['data']['nu'][RowID]
            LineIntensityDB = LOCAL_TABLE_CACHE[TableName]['data']['sw'][RowID]
            LowerStateEnergyDB = LOCAL_TABLE_CACHE[TableName]['data']['elower'][RowID]
            MoleculeNumberDB = LOCAL_TABLE_CACHE[TableName]['data']['molec_id'][RowID]
            IsoNumberDB = LOCAL_TABLE_CACHE[TableName]['data']['local_iso_id'][RowID]
            if LineShift:
                Shift0DB = LOCAL_TABLE_CACHE[TableName]['data']['delta_air'][RowID]
            else:
                Shift0DB = 0
            
            # filter by molecule and isotopologue
            if (MoleculeNumberDB,IsoNumberDB) not in ABUNDANCES: continue
            
            # partition functions for T and Tref
            # TODO: optimize
            SigmaT = partitionFunction(MoleculeNumberDB,IsoNumberDB,T)
            SigmaTref = partitionFunction(MoleculeNumberDB,IsoNumberDB,Tref)
            
            # get all environment dependences from voigt parameters
            
            #   intensity
            LineIntensity = EnvironmentDependency_Intensity(LineIntensityDB,T,Tref,SigmaT,SigmaTref,
                                                            LowerStateEnergyDB,LineCenterDB)
            
            #   FILTER by LineIntensity: compare it with IntencityThreshold
            # TODO: apply wing narrowing instead of filtering, this would be more appropriate
            if LineIntensity < IntensityThreshold: continue
            
            cMassMol = 1.66053873e-27
            fSqrtMass = sqrt(molecularMass(MoleculeNumberDB,IsoNumberDB))
            cc_ = 2.99792458e8
            cBolts_ = 1.3806503e-23
            GammaD = (cSqrt2Ln2/cc_)*sqrt(cBolts_/cMassMol)*sqrt(T) * LineCenterDB/fSqrtMass
                        
            #   get final wing of the line according to GammaD, OmegaWingHW and OmegaWing
            OmegaWingF = max(OmegaWing,OmegaWingHW*GammaD)

            #   shift coefficient
            Shift0 = Shift0DB*p/pref

            BoundIndexLower = bisect(Omegas,LineCenterDB-OmegaWingF)
            BoundIndexUpper = bisect(Omegas,LineCenterDB+OmegaWingF)
            lineshape_vals = PROFILE_DOPPLER(LineCenterDB+Shift0,GammaD,Omegas[BoundIndexLower:BoundIndexUpper])
            Xsect[BoundIndexLower:BoundIndexUpper] += factor / NATURAL_ABUNDANCES[(MoleculeNumberDB,IsoNumberDB)] * \
                                                      ABUNDANCES[(MoleculeNumberDB,IsoNumberDB)] * \
                                                      LineIntensity * lineshape_vals

    if File: save_to_file(File,Format,Omegas,Xsect)
    return Omegas,Xsect

# -------------------------------------------------------------------------------
# UNIFIED INTERFACE FOR THE ABSORPTION COEFFICIENT AND CROSS-SECTION CALCULATIONS
# -------------------------------------------------------------------------------
PROFILE_MAP = {
    'Voigt': absorptionCoefficient_Voigt,
    'Lorentz': absorptionCoefficient_Lorentz,
    'Doppler': absorptionCoefficient_Doppler,
    'SDV': absorptionCoefficient_SDVoigt,
    'HT': absorptionCoefficient_HT,
}
def absorptionCrossSection(profile='HT',**argv):
    argv['HITRAN_units'] = True
    return PROFILE_MAP[profile](**argv)
    
def absorptionCoefficient(profile='HT',**argv):
    argv['HITRAN_units'] = False
    return PROFILE_MAP[profile](**argv)    
    
# ---------------------------------------------------------------------------
# SHORTCUTS AND ALIASES FOR ABSORPTION COEFFICIENTS
# ---------------------------------------------------------------------------

absorptionCoefficient_Gauss = absorptionCoefficient_Doppler

def abscoef_HT(table=None,step=None,grid=None,env={'T':296.,'p':1.},file=None):
    return absorptionCoefficient_HT(SourceTables=table,OmegaStep=step,OmegaGrid=grid,Environment=env,File=file)

def abscoef_Voigt(table=None,step=None,grid=None,env={'T':296.,'p':1.},file=None):
    return absorptionCoefficient_Voigt(SourceTables=table,OmegaStep=step,OmegaGrid=grid,Environment=env,File=file)
    
def abscoef_Lorentz(table=None,step=None,grid=None,env={'T':296.,'p':1.},file=None):
    return absorptionCoefficient_Lorentz(SourceTables=table,OmegaStep=step,OmegaGrid=grid,Environment=env,File=file)

def abscoef_Doppler(table=None,step=None,grid=None,env={'T':296.,'p':1.},file=None):
    return absorptionCoefficient_Doppler(SourceTables=table,OmegaStep=step,OmegaGrid=grid,Environment=env,File=file)

abscoef_Gauss = abscoef_Doppler
    
def abscoef(table=None,step=None,grid=None,env={'T':296.,'p':1.},file=None): # default
    return absorptionCoefficient_Lorentz(SourceTables=table,OmegaStep=step,OmegaGrid=grid,Environment=env,File=file)
    
# ---------------------------------------------------------------------------
    
def transmittanceSpectrum(Omegas,AbsorptionCoefficient,Environment={'l':100.},
                          File=None, Format='%e %e', Wavenumber=None):
    """
    INPUT PARAMETERS: 
        Wavenumber/Omegas:   wavenumber grid                    (required)
        AbsorptionCoefficient:  absorption coefficient on grid  (required)
        Environment:  dictionary containing path length in cm.
                      Default={'l':100.}
        File:         name of the output file                 (optional) 
        Format: c format used in file output, default '%e %e' (optional)
    OUTPUT PARAMETERS: 
        Wavenum: wavenumber grid
        Xsect:  transmittance spectrum calculated on the grid
    ---
    DESCRIPTION:
        Calculate a transmittance spectrum (dimensionless) based
        on previously calculated absorption coefficient.
        Transmittance spectrum is calculated at an arbitrary
        optical path length 'l' (1 m by default)
    ---
    EXAMPLE OF USAGE:
        nu,trans = transmittanceSpectrum(nu,coef)
    ---
    """
    # compatibility with older versions
    if Wavenumber: Omegas=Wavenumber
    l = Environment['l']
    Xsect = exp(-AbsorptionCoefficient*l)
    if File: save_to_file(File,Format,Omegas,Xsect)
    return Omegas,Xsect

def absorptionSpectrum(Omegas,AbsorptionCoefficient,Environment={'l':100.},
                       File=None, Format='%e %e',Wavenumber=None):
    """
    INPUT PARAMETERS: 
        Wavenumber/Omegas:   wavenumber grid                    (required)
        AbsorptionCoefficient:  absorption coefficient on grid  (required)
        Environment:  dictionary containing path length in cm.
                      Default={'l':100.}
        File:         name of the output file                 (optional) 
        Format: c format used in file output, default '%e %e' (optional)
    OUTPUT PARAMETERS: 
        Wavenum: wavenumber grid
        Xsect:  absorption spectrum calculated on the grid
    ---
    DESCRIPTION:
        Calculate an absorption spectrum (dimensionless) based
        on previously calculated absorption coefficient.
        Absorption spectrum is calculated at an arbitrary
        optical path length 'l' (1 m by default)
    ---
    EXAMPLE OF USAGE:
        nu,absorp = absorptionSpectrum(nu,coef)
    ---
    """
    # compatibility with older versions
    if Wavenumber: Omegas=Wavenumber
    l = Environment['l']
    Xsect = 1-exp(-AbsorptionCoefficient*l)
    if File: save_to_file(File,Format,Omegas,Xsect)
    return Omegas,Xsect

def radianceSpectrum(Omegas,AbsorptionCoefficient,Environment={'l':100.,'T':296.},
                     File=None, Format='%e %e', Wavenumber=None):
    """
    INPUT PARAMETERS: 
        Wavenumber/Omegas:   wavenumber grid                   (required)
        AbsorptionCoefficient:  absorption coefficient on grid (required)
        Environment:  dictionary containing path length in cm.
                      and temperature in Kelvin.
                      Default={'l':100.,'T':296.}
        File:         name of the output file                 (optional) 
        Format: c format used in file output, default '%e %e' (optional)
    OUTPUT PARAMETERS: 
        Wavenum: wavenumber grid
        Xsect:  radiance spectrum calculated on the grid
    ---
    DESCRIPTION:
        Calculate a radiance spectrum (in W/sr/cm^2/cm-1) based
        on previously calculated absorption coefficient.
        Radiance spectrum is calculated at an arbitrary
        optical path length 'l' (1 m by default) and 
        temperature 'T' (296 K by default). For obtaining a
        physically meaningful result 'T' must be the same 
        as a temperature which was used in absorption coefficient.
    ---
    EXAMPLE OF USAGE:
        nu,radi = radianceSpectrum(nu,coef)
    ---
    """
    # compatibility with older versions
    if Wavenumber: Omegas=Wavenumber
    l = Environment['l']
    T = Environment['T']
    Alw = 1-exp(-AbsorptionCoefficient*l)
    LBBTw = 2*hh*cc**2*Omegas**3 / (exp(hh*cc*Omegas/(cBolts*T)) - 1) * 1.0E-7
    Xsect = Alw*LBBTw # W/sr/cm**2/cm**-1
    if File: save_to_file(File,Format,Omegas,Xsect)
    return Omegas,Xsect


# GET X,Y FOR FINE PLOTTING OF A STICK SPECTRUM
def getStickXY(TableName):
    """
    Get X and Y for fine plotting of a stick spectrum.
    Usage: X,Y = getStickXY(TableName).
    """
    cent,intens = getColumns(TableName,('nu','sw'))
    n = len(cent)
    cent_ = zeros(n*3)
    intens_ = zeros(n*3)
    for i in range(n):
        intens_[3*i] = 0
        intens_[3*i+1] = intens[i]
        intens_[3*i+2] = 0
        cent_[(3*i):(3*i+3)] = cent[i]
    return cent_,intens_
# /GET X,Y FOR FINE PLOTTING OF A STICK SPECTRUM


# LOW-RES SPECTRA (CONVOLUTION WITH APPARATUS FUNCTION)

# /LOW-RES SPECTRA (CONVOLUTION WITH APPARATUS FUNCTION)

# /----------------------------------------------------------------------------


# ------------------  HITRAN-ON-THE-WEB COMPATIBILITY -------------------------

def read_hotw(filename):
    """
    Read cross-section file fetched from HITRAN-on-the-Web.
    The format of the file line must be as follows: 
      nu, coef
    Other lines are omitted.
    """
    import sys
    f = open(filename,'r')
    nu = []
    coef = []
    for line in f:
        pars = line.split()
        try:
            nu.append(float(pars[0]))
            coef.append(float(pars[1]))
        except:
            if False:
                print(sys.exc_info())
            else:
                pass    
    return array(nu),array(coef)

# alias for read_hotw for backwards compatibility
read_xsect = read_hotw
    
# /----------------------------------------------------------------------------

# ------------------  SPECTRAL CONVOLUTION -------------------------

# rectangular slit function
def SLIT_RECTANGULAR(x,g):
    """
    Instrumental (slit) function.
    B(x) = 1/γ , if |x| ≤ γ/2 & B(x) = 0, if |x| > γ/2,
    where γ is a slit width or the instrumental resolution.
    """
    index_inner = abs(x) <= g/2
    index_outer = ~index_inner
    y = zeros(len(x))
    y[index_inner] = 1/g
    y[index_outer] = 0
    return y

# triangular slit function
def SLIT_TRIANGULAR(x,g):
    """
    Instrumental (slit) function.
    B(x) = 1/γ*(1-|x|/γ), if |x| ≤ γ & B(x) = 0, if |x| > γ,
    where γ is the line width equal to the half base of the triangle.
    """
    index_inner = abs(x) <= g
    index_outer = ~index_inner
    y = zeros(len(x))
    y[index_inner] = 1/g * (1 - abs(x[index_inner])/g)
    y[index_outer] = 0
    return y

# gaussian slit function
def SLIT_GAUSSIAN(x,g):
    """
    Instrumental (slit) function.
    B(x) = sqrt(ln(2)/pi)/γ*exp(-ln(2)*(x/γ)**2),
    where γ/2 is a gaussian half-width at half-maximum.
    """
    g /= 2
    return sqrt(log(2))/(sqrt(pi)*g)*exp(-log(2)*(x/g)**2)

# dispersion slit function
def SLIT_DISPERSION(x,g):
    """
    Instrumental (slit) function.
    B(x) = γ/pi/(x**2+γ**2),
    where γ/2 is a lorentzian half-width at half-maximum.
    """
    g /= 2
    return g/pi/(x**2+g**2)

# cosinus slit function
def SLIT_COSINUS(x,g):
    return (cos(pi/g*x)+1)/(2*g)

# diffraction slit function
def SLIT_DIFFRACTION(x,g):
    """
    Instrumental (slit) function.
    """
    y = zeros(len(x))
    index_zero = x==0
    index_nonzero = ~index_zero
    dk_ = pi/g
    x_ = dk_*x[index_nonzero]
    w_ = sin(x_)
    r_ = w_**2/x_**2
    y[index_zero] = 1
    y[index_nonzero] = r_/g
    return y

# apparatus function of the ideal Michelson interferometer
def SLIT_MICHELSON(x,g):
    """
    Instrumental (slit) function.
    B(x) = 2/γ*sin(2pi*x/γ)/(2pi*x/γ) if x!=0 else 1,
    where 1/γ is the maximum optical path difference.
    """
    y = zeros(len(x))
    index_zero = x==0
    index_nonzero = ~index_zero
    dk_ = 2*pi/g
    x_ = dk_*x[index_nonzero]
    y[index_zero] = 1
    y[index_nonzero] = 2/g*sin(x_)/x_
    return y

# spectral convolution with an apparatus (slit) function
def convolveSpectrum(Omega,CrossSection,Resolution=0.1,AF_wing=10.,
                     SlitFunction=SLIT_RECTANGULAR,Wavenumber=None):
    """
    INPUT PARAMETERS: 
        Wavenumber/Omega:    wavenumber grid                     (required)
        CrossSection:  high-res cross section calculated on grid (required)
        Resolution:    instrumental resolution γ                 (optional)
        AF_wing:       instrumental function wing                (optional)
        SlitFunction:  instrumental function for low-res spectra calculation (optional)
    OUTPUT PARAMETERS: 
        Wavenum: wavenumber grid
        CrossSection: low-res cross section calculated on grid
        i1: lower index in Omega input
        i2: higher index in Omega input
        slit: slit function calculated over grid [-AF_wing; AF_wing]
                with the step equal to instrumental resolution. 
    ---
    DESCRIPTION:
        Produce a simulation of experimental spectrum via the convolution 
        of a “dry” spectrum with an instrumental function.
        Instrumental function is provided as a parameter and
        is calculated in a grid with the width=AF_wing and step=Resolution.
    ---
    EXAMPLE OF USAGE:
        nu_,radi_,i,j,slit = convolveSpectrum(nu,radi,Resolution=2.0,AF_wing=10.0,
                                                SlitFunction=SLIT_MICHELSON)
    ---
    """    
    # compatibility with older versions
    if Wavenumber: Omega=Wavenumber
    step = Omega[1]-Omega[0]
    if step>=Resolution: raise Exception('step must be less than resolution')
    #x = arange(-AF_wing,AF_wing+step,step)
    x = arange_(-AF_wing,AF_wing+step,step) # fix
    slit = SlitFunction(x,Resolution)
    slit /= sum(slit)*step # simple normalization
    left_bnd = int(len(slit)/2) # new versions of Numpy don't support float indexing
    right_bnd = len(Omega) - int(len(slit)/2) # new versions of Numpy don't support float indexing
    CrossSectionLowRes = convolve(CrossSection,slit,mode='same')*step
    return Omega[left_bnd:right_bnd],CrossSectionLowRes[left_bnd:right_bnd],left_bnd,right_bnd,slit

# spectral convolution with an apparatus (slit) function
def convolveSpectrumSame(Omega,CrossSection,Resolution=0.1,AF_wing=10.,
                         SlitFunction=SLIT_RECTANGULAR,Wavenumber=None):
    """
    Convolves cross section with a slit function with given parameters.
    """
    # compatibility with older versions
    if Wavenumber: Omega=Wavenumber
    step = Omega[1]-Omega[0]
    if step>=Resolution: raise Exception('step must be less than resolution')
    #x = arange(-AF_wing,AF_wing+step,step)
    x = arange_(-AF_wing,AF_wing+step,step) # fix
    slit = SlitFunction(x,Resolution)
    slit /= sum(slit)*step # simple normalization
    left_bnd = 0
    right_bnd = len(Omega)
    CrossSectionLowRes = convolve(CrossSection,slit,mode='same')*step
    return Omega[left_bnd:right_bnd],CrossSectionLowRes[left_bnd:right_bnd],left_bnd,right_bnd,slit

def convolveSpectrumFull(Omega,CrossSection,Resolution=0.1,AF_wing=10.,SlitFunction=SLIT_RECTANGULAR):
    """
    Convolves cross section with a slit function with given parameters.
    """
    step = Omega[1]-Omega[0]
    x = arange(-AF_wing,AF_wing+step,step)
    slit = SlitFunction(x,Resolution)
    print('step=')
    print(step)
    print('x=')
    print(x)
    print('slitfunc=')
    print(SlitFunction)
    CrossSectionLowRes = convolve(CrossSection,slit,mode='full')*step
    return Omega,CrossSectionLowRes,None,None

# ------------------------------------------------------------------