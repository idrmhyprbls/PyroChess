#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Omit docstring, is set below from metadata
from __future__ import absolute_import

# 0. Start time
from datetime import datetime as _datetime
_DATE = _datetime.isoformat(_datetime.today())

# 1. Documentation
from pyrochess import metadata as _metadata

__doc__ = _metadata.__doc__
__date__ = _metadata.DATE
__author__ = _metadata.AUTHOR
__credits__ = _metadata.CREDITS
__package__ = _metadata.PROGRAM
__version__ = _metadata.VERSION

VERSION = _metadata.VERSION
if '?' not in VERSION:
    VERSION_INFO = tuple(int(each) for each in _metadata.VERSION.split('.'))
else:
    VERSION_INFO = tuple(_metadata.VERSION.split('.'))

# 2. Imports
__all__ = [
        'board',
        'config',
        'game',
        'logger',
        'mainloop',
        'metadata',
        'metadata',
        'piece',
        'square',
        'utils']

# 3. Configure settings
from pyrochess.config import SETTINGS

# 4. Configure logging
from logging import getLogger as _getLogger
from pyrochess.logger import init_logging as _init_logging
_init_logging(SETTINGS)
_log = _getLogger(_metadata.PROGRAM)
_log.debug("=== {} v{} begun at: {} ===".format(__package__,
                                                VERSION,
                                                _DATE))
# 5. Expose main and other chained imports
from pyrochess.cli import main

