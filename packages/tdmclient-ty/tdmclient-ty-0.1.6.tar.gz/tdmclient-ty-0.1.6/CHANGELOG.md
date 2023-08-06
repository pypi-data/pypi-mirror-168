# Changelog

Notable changes of tdmclient-ty. Release versions refer to [https://pypi.org/project/tdmclient-ty/].

## [Unreleased]

## [0.1.6] - 2022-09-21

### Fixed

- No more error when TDM isn't running.

## [0.1.5] - 2022-06-29

### Fixed

- Connection to TDM is closed explicitly when quitting Thonny

## [0.1.4] - 2022-06-23

### Added

- Toolbar buttons for commands _Run on Thymio_ and _Stop Thymio_
- Robot panel (menu View > Thymio Robots)

## Changed

- Connection to local TDM instead of TDM advertised by zeroconf

## [0.1.3] - 2022-04-05

### Added

- Warnings for local variables which hide global variables (a declaration as global could be missing)
- `NameError` exceptions, raised by the transpiler e.g. if the Aseba dot syntax is used instead of names with underscores, are displayed in the Shell panel
- In error messages, code numbers are replaced by messages when their meaning is known
- Shortcut Control-Shift-T for menu command Tools>Transpile Program
- Menu commands moved to a separate "Thymio" menu
- Menu entry "Disconnect" disabled when the robot is not connected
- In error messages, hyperlink to select line

### Fixed

- Robot disconnections and reconnections

## [0.1.2] - 2022-02-23

### Added

- Line number in error messages
- Error message in the Shell panel when the program cannot be executed on the robot

## [0.1.1] - 2021-11-04

### Added

- Transpiler errors displayed in shell panel
- Code examples in documentation

## [0.1.0] - 2021-10-20

### Added

- First release on PyPI
