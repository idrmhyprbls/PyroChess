#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Logging setup"""
from __future__ import absolute_import

import logging
from logging.handlers import RotatingFileHandler

from pyrochess.metadata import PROGRAM as _PROGRAM

_FMAT = r'%(asctime)s.%(msecs)-3d | ' + \
       r'%(levelname)-8s | ' + \
       r'{0:12s} | ' + \
       r'%(filename)-15s | ' + \
       r'%(lineno)-5d | ' + \
       r'%(funcName)-20s | ' + \
       r'%(message)s'
_FTIME = r'%y-%m-%d %H:%M:%S'

def set_log_level(settings):
    """Sets root stream logging level"""

    if settings.quiet:
        level = logging.ERROR
    elif settings.debug:
        level = logging.DEBUG
    elif settings.verbose:
        level = logging.INFO
    else:
        level = logging.WARN

    logger = logging.getLogger(_PROGRAM)
    logger.handlers[0].setLevel(level)

def _add_file_handler(settings):
    formatter = logging.Formatter(_FMAT.format(settings.env.user), _FTIME)
    fh = RotatingFileHandler(settings.log,
                             maxBytes=1024**2,
                             backupCount=3)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger = logging.getLogger(_PROGRAM)
    logger.addHandler(fh)

def init_logging(settings):

    formatter = logging.Formatter(_FMAT.format(settings.env.user), _FTIME)
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger = logging.getLogger(_PROGRAM)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    set_log_level(settings)
    if settings.log:
        _add_file_handler(settings)
