# Non-uniform Temperature Fitting (NTfit)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7109070.svg)](https://doi.org/10.5281/zenodo.7109070)
[![License](https://img.shields.io/badge/License-BSD%203-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![PyPI](https://badge.fury.io/py/ntfit.svg)](https://badge.fury.io/py/ntfit)

Nonuniform-temperature fitting code, to extract spatial temperature variations along a laser path. For high-temperature gas diagnostics.

In support of the 2-part paper series N.A. Malarich and G.B. Rieker, "Resolving nonuniform temperature distributions with single-beam absorption spectroscopy"

Nonuniform-temperature fitting is a two-step process. 
The Python package ntfit has sub-packages for each step.
1) `ntfit.spectrafit`: Extract linestrengths from broadband spectrum with E"-binning.
2) `ntfit.tdist`: Fit temperature distribution from linestrength fit in (1) with Tikhonov regularization.

For help running the fits, check out `examples/Example_td.py`, or the associated .ipynb (Jupyter Notebook) file.


## Package requirements
Your computer must already have the following Python packages:
```
python3.x
numpy
matplotlib
scipy
```
NTfit also includes [HAPI](https://github.com/hitranonline/hapi), available under MIT license. 
NTfit changed HAPI version 1.1.0.9.6 lineshape equations (power-law temperature dependence) from original HAPI to improve high-temperature acuracy.
See `ntfit/hapi/hapi_combustion.py` docstring for details.
Partition functions are calculated using TIPS2017.



## References
If you use this package, please cite the following articles.
for E"-bin fitting with `HAPI`:

* R.V. Kochanov, I.E. Gordon, L.S. Rothman, P. Wcislo, C. Hill, J.S. Wilzewski, 
   HITRAN Application Programming Interface (HAPI): A comprehensive approach to working 
   with spectroscopic data, J. Quant. Spectrosc. Radiat. Transfer 177, 15-30 (2016) 
   DOI: [10.1016/j.jqsrt.2016.03.005](https://www.doi.org/10.1016/j.jqsrt.2016.03.005).

* N.A. Malarich and G.B. Rieker, "Resolving nonuniform temperature distributions with single-beam absorption spectroscopy. Part II: Implementation from broadband spectra" JQSRT (2021) 
DOI: [10.1016/j.jqsrt.2021.107805](https://www.doi.org/10.1016/j.jqsrt.2021.107805)

* (time-domain fitting) R.K. Cole, A.S. Makowiecki, Z. Hoghooghi, G.B. Rieker, "Baseline-free Quantitative Absorption Spectroscopy Based on Cepstral Analysis" Optics Express 27 (2019) 
DOI: [10.1364/OE.27.037920](https://www.doi.org/10.1364/OE.27.037920).

for `ntfit.tdist`:

* N.A. Malarich and G.B. Rieker, "Resolving nonuniform temperature distributions with single-beam absorption spectroscopy. Part I: Theoretical capabilities and limitations" JQSRT (2021) 
DOI: [10.1016/j.jqsrt.2020.107455](https://www.doi.org/10.1016/j.jqsrt.2020.107455)


##  Author

[Nathan Malarich](https://nam5312.gitlab.io/personal_website/) (<nathan.malarich@colorado.edu>)