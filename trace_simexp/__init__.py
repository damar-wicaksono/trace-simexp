# -*- coding: utf-8 -*-
"""
    trace_simexp
    *************

    Module with utilities to carry out simulation experiment in TRACE code.
    The experiment is divided into three steps and for each, user interacts
    through the available command line interface

    1. pre-processing
    2. execute
    3. post-processing
"""
from . import prepro
from . import execute
from . import postpro
from . import reset
from . import cmdln_args
from . import info_file
from . import util
from . import template
from . import tracin_util
from ._version import __version__

__author__ = "Damar Wicaksono"
