# Change Log

All notable changes to this project will be documented in this file

The format is based on [Keep a Changelog](http://keepachangelog.com)
and this project adheres to [Semantic Versioning](http://semver.org)

## v0.2.0 - 2016-03-27

### Added
- Fully functioning `trace_simexp_execute`
- Documentation on `trace_simexp_execute` command line interface

### Changed
- `get_executable()` function is now used to check and get provided 
  executables whether they are in PATH or specified in a path, to 
  reduce clutter.
- `get_name()` function is now used to get either directory name 
  or filename specified in path, either relative or absolute.
- `os.path.split()` is now used in place of parsing manually delimiter
   "/" or "\"

## v0.1.0 - 2016-03-25

### Added
- Fully functioning `trace_simexp_prepro`
