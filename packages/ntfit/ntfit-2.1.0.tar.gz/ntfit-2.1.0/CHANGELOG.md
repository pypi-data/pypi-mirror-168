# Change Log

## [2.1] - 2022-09-23
### Changed
- ntfit now a separate sub-package, compatible with pip install
- `hapi` sub-package has separate file for Q(T) tables
- Removed uniform_fit example, as lookup table is much more efficient way to fit temperature
- Tikhonov regularization module now `ntfit.tdist`
- E"-bin spectral-fitting now `ntfit.spectrafit`

## [2.0] - 2021-03-01
### Added
- E"-bin spectral fitting package with hapi