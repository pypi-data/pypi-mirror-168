# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).


## [In Development] - Unreleased


## [0.1.0-alpha.19] - 2022-09-18

### Changed

- Dashboard error message replaced with Django message API
- Internal improvements


## [0.1.0-alpha.18] - 2022-08-23

### Added

- `related_name` to `fleet_commander` in model

### Changed

- CSS moved to bundled HTML template
- Logger messages changed to f-strings
- Using `allianceauth-app-utils` for logging
- Task ESI error handling improved
- Moved constants to their own file
- `related_name` for group restrictions in model to prevent conflicts with other
  modules. The name was too generic.
- Minimum Requirements
  - Alliance Auth >= 3.0.0
  - Python >= 3.8

### Removed

- Unused code


## [0.1.0-alpha.17] - 2022-07-11

### Changed

- Switch to f-strings for formatted strings
- Templates cleaned up


## [0.1.0-alpha.16] - 2022-06-24

### Added

- Versioned static template tag

### Removed

- AVOID_CDN setting, we serve always locally (GDPR)


## [0.1.0-alpha.15] - 2022-03-02

### Added

- Test suite for AA 3.x and Django 4

### Removed

- Deprecated settings

### Changed

- Minimum dependencies:
  - Alliance Auth>=2.11.0 (as last stable of the 2.x branch for now)


## [0.1.0-alpha.14] - 2022-03-01

### Removed

- `setup.py` as it is no longer required

### Changed

- Makefile updated


## [0.1.0-alpha.13] - 2022-03-01

### Added

- Package discovery to `setup.cfg` (hopefully)


## [0.1.0-alpha.12] - 2022-03-01

### Fixed

- Classifiers in `setup.cfg`


## [0.1.0-alpha.11] - 2022-03-01

### Changed

- Switched to `setup.cfg` instead of `setup.py`


## [0.1.0-alpha.10] - 2022-02-28

### Fixed

- [Compatibility] AA 3.x / Django 4 :: ImportError: cannot import name
  'ugettext_lazy' from 'django.utils.translation'


## [0.1.0-alpha.9] - 2022-02-02

### Added

- Tests for Python 3.11

### Changed

- Using `path` in URL config instead of soon-to-be removed `url`
- Minimum requirements
  - Alliance Auth v2.9.4


## [0.1.0-alpha.8] - 2021-11-30

### Changed

- Minimum requirements
  - Python 3.7
  - Alliance Auth v2.9.3


## [0.1.0-alpha.7] - 2021-11-15

### Added

- Basic test suite


## [0.1.0-alpha.6] - 2021-07-08

### Changed

- Compatibility with Python 3.9 and Django 3.2


## [0.1.0-alpha.5] - 2021-01-25

### Added

- ESI error hardening

### Changed

- Fleet table on dashboard is now loaded via ajax and refreshed every 30 seconds


## [0.1.0-alpha.4] - 2021-01-12

### Removed

- Django 2 support


## [0.1.0-alpha.3] - 2021-01-05

### Fixed

- Permission to create fleets


## [0.1.0-alpha.2] - 2021-01-05

### Changed

- Datatables in fleet details view set up properly
- UI in fleet details view re-done
- Fleet details are nor refreshed every 15 seconds via Datatables reload


## [0.1.0-alpha.1] - 2020-12-30

App forked from [Dreadbomb/aa-fleet](https://github.com/Dreadbomb/aa-fleet)

### Fixed

- HTML errors
- Datatable erors
- Import order
- Code issues cleaned up
- General model and permissions

### Changed

- Fleet commander transformed into EveCharacter model
- Automatic page reload in fleet details view deactivated (was causing troubles)
- Datatable for dashboard configured properly
- Migrations reset
