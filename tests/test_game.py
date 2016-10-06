#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

import unittest
import logging

from pyrochess import *

from pyrochess.config import SETTINGS
from pyrochess.metadata import PROGRAM
from pyrochess.game import Game

LOG = logging.getLogger(PROGRAM)

class TestModule(unittest.TestCase):
    """Nose test class."""

    @classmethod
    def setUpClass(self):
        SETTINGS.testing = True

    @classmethod
    def tearDownClass(self):
        pass

    def setUp(self):
        """Sets up the test."""
        LOG.debug(SETTINGS)
        LOG.debug(__name__)

    def tearDown(self):
        """Tears down the test."""
        pass

    def testGame(self):
        """Test call to game."""
        f = Game.parse_move_str
        f('00')
        # f('0000')
        # f('o')
        # f('o0')
        # f('o0-0')
        # f('o0-O-o')
