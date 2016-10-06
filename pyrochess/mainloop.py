#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Main update loop"""
from __future__ import absolute_import

import logging
import sys

IMPORT_ERRORS = []
try:
    import pudb as pdb
except ImportError:
    IMPORT_ERRORS.append("Can't import 'pudb', using 'pdb'!")
    import pdb

from pyrochess.config import SETTINGS
from pyrochess.game import Game
from pyrochess.metadata import PROGRAM
from pyrochess.utils import entry_exit

LOG = logging.getLogger(PROGRAM)

@entry_exit(LOG)
def mainloop():  # cli=True):
    if IMPORT_ERRORS:
        for each in IMPORT_ERRORS:
            LOG.warning("Import issue: {}".format(each))
    try:
        Game().run()
    except (KeyboardInterrupt, SystemExit):
        sys.stdout.flush()
        sys.stderr.flush()
    except Exception as err:
        # Unhandeld exception
        if 0:  # TODO
            LOG.exception(err)
            pdb.post_mortem()  # 'e' to view
        else:
            raise
