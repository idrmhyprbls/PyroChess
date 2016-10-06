#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Config class to create global SETTINGS"""
from __future__ import absolute_import

import ConfigParser
import string
import os

from pyrochess import utils

class Settings(object):

    games = {'': 0, 'normal': 8}
    imported = True
    env = utils.Env()

    def __init__(self):
        # Configurable
        self.quiet = False
        self.verbose = False
        self.debug = False
        self.unicode = False
        self.testing = False
        self.log = ''
        self.game = ''

        # Non-configurable
        self.config = ''
        self.dnum = 0
        self.rank = []
        self.file = ''

        # Load default configs
        self.set_game(self.game)
        self.load_config()

    def set_game(self, game):
        if not self.game:
            self.game = 'normal'
        self.dnum = self.games[self.game]  # 8, 16, ..
        self.rank = xrange(1, self.dnum + 1)  # 1, 2, ..
        self.file = string.lowercase[:self.dnum]  # a, b, ..

    def find_cfile(self, cfile):
        if cfile:
            self.config = cfile
        else:
            cfile = os.path.abspath(os.path.expanduser('~/.pyrochess'))
            if os.path.isfile(cfile):
                self.config = cfile
            else:
                cfile = os.path.abspath(os.path.expanduser('~/.pyrochess.ini'))
                if os.path.isfile(cfile):
                    self.config = cfile
                else:
                    cfile = os.path.abspath(
                        os.path.expanduser('~/pyrochess.ini'))
                    if os.path.isfile(cfile):
                        self.config = cfile
                    else:
                        cfile = '.pyrochess.ini'
                        if os.path.isfile(cfile):
                            self.config = cfile

    def load_config(self, cfile=None):
        self.find_cfile(cfile)

        if not self.config:
            return

        parser = ConfigParser.ConfigParser(allow_no_value=False)
        confirm = parser.read(self.config)
        if len(confirm) > 0 and self.config in confirm[0]:
            for sec in parser.sections():
                if sec.lower() != 'pyrochess':
                    continue
                try:
                    for key, val in parser.items(sec):
                        if key in self.__dict__.keys():
                            val = utils.auto_cast(val)
                            setattr(self, key, val)
                except ConfigParser.InterpolationMissingOptionError:
                    raise
        else:
            raise ConfigParser.Error(
                "Issue reading config file '{}'".format(self.config))

    def __repr__(self):
        return "Settings(" + ", ".join(["{}={}".format(k, v)
                                        for k, v in self.__dict__.iteritems()]) + ")"

SETTINGS = Settings()
