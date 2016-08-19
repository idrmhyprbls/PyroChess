#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Omit docstring, is set below from metadata

from __future__ import absolute_import, division, print_function, with_statement

from datetime import datetime as _datetime
_DATE = _datetime.isoformat(_datetime.today())
from logging import getLogger as _getLogger

# 1. Documentation
from pyrochess import metadata as _metadata

__doc__ = _metadata.__doc__
__date__ = _metadata.DATE
__author__ = _metadata.AUTHOR
__credits__ = _metadata.CREDITS
__package__ = _metadata.PROGRAM
__version__ = _metadata.VERSION
VERSION = _metadata.VERSION
VERSION_INFO = tuple(_metadata.VERSION.split('.'))

# 2. Expose settings
from pyrochess.config import SETTINGS

# 3. Configure logging
from pyrochess.logger import init_logging as _init_logging
_init_logging(SETTINGS)

# Log Start
_log = _getLogger(_metadata.PROGRAM)
_log.debug("=== {} v{} begun at: {} ===".format(__package__, _metadata.VERSION,
                                                _DATE))
if __name__ != '__main__':
    from pyrochess.mainloop import mainloop
