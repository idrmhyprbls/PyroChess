#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Omit docstring, is set below from metadata

from __future__ import absolute_import, division, print_function, with_statement

from datetime import datetime
_DATE = datetime.isoformat(datetime.today())
import logging

# Documentation
from pyrochess import metadata

__author__ = metadata.author
__credits__ = metadata.credits
__date__ = metadata.date
__doc__ = metadata.__doc__
__version__ = metadata.version
__package__ = metadata.program

# Expose settings
from pyrochess.config import settings

# Configure logging
from pyrochess.logger import init_logging as _init_logging
_init_logging(settings)

# Log Start
_log = logging.getLogger(metadata.program)
_log.debug("=== {} v{} begun at: {} ===".format(__package__, metadata.version,
                                                _DATE))
