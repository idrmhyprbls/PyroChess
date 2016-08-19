#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

import ConfigParser
import struct
import sys
import pwd
import string
import time
import platform
import os

from pyrochess import utils

class Settings(object):

    # System (snapshot!)
    # archp2 = platform.architecture()[0]  # Str (not reliable in OSX)
    # archp = ("32bit", "64bit")[(struct.calcsize("P") == 8)]  # Str (for python)
    # cwd = os.getcwd()  # Str
    # distro = ' '.join(platform.linux_distribution())  # Str
    # ls = os.listdir('.')  # List
    # home = os.path.expanduser('~')  # Str
    # host = platform.node()  # Str
    # mach = platform.uname()[-2]  # Str
    # null = '\0'  # Str
    # nul = os.devnull  # Str (location of..)
    # os_ = os.uname()  # List
    # osname = os.name.upper()  # Str
    # ostitl = platform.uname()[0].title()  # Str
    # osver = platform.uname()[2][:platform.uname()[2].find('-')].title()  # Str
    # plat = sys.platform.upper()  # Str
    # proc = platform.uname()[-1]  # Str
    # serr = sys.stderr  # File object
    # sin = sys.stdin  # File object
    # sout = sys.stdout  # File object
    # ctime = time.ctime()  # Str
    # ltime = time.localtime()  # Time struct
    user = pwd.getpwuid(os.getuid())[0]  # Str (getlogin can fail)
    # ver = sys.version_info[0:3]  # List (python)
    # vers = '.'.join(str(idx) for idx in ver)  # Str (python)

    # Game
    games = {'': 0, 'normal': 8}

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
                        cfile = 'pyrochess.ini'
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
