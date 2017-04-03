#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Portable utilities"""
from ast import literal_eval as evil
from functools import wraps
from datetime import datetime
import struct
import sys
import platform
import exceptions
import pwd
import time
import string
import os
import pdb
import inspect

# WARNING: No local module imports!

ALPHANUMERIC = string.letters + string.digits

# Character to unicode
CTU = {'K': u'♔', 'Q': u'♕', 'R': u'♖', 'B': u'♗', 'N': u'♘', 'P': u'♙',
       'k': u'♚', 'q': u'♛', 'r': u'♜', 'b': u'♝', 'n': u'♞', 'p': u'♟'}

trace = lambda: pdb.set_trace()

def lineno():
    """Return current line number."""
    return inspect.currentframe().f_back.f_lineno

class BadInputWarn(exceptions.Warning):
    """Bad user input."""
    pass

class Env(object):
    """System environment data"""
    @property
    def archp2(self):
        return platform.architecture()[0]  # Str (not reliable in OSX)
    @property
    def archp(self):
        return ("32bit", "64bit")[(struct.calcsize("P") == 8)]  # Str (for py)
    @property
    def cwd(self):
        return os.getcwd()  # Str
    @property
    def distro(self):
        return ' '.join(platform.linux_distribution())  # Str
    @property
    def ls(self):
        return os.listdir('.')  # List
    @property
    def home(self):
        return os.path.expanduser('~')  # Str
    @property
    def host(self):
        return platform.node()  # Str
    @property
    def mach(self):
        return platform.uname()[-2]  # Str
    @property
    def null(self):
        return '\0'  # Str
    @property
    def nul(self):
        return os.devnull  # Str (location of..)
    @property
    def os_(self):
        return os.uname()  # List
    @property
    def osname(self):
        return os.name.upper()  # Str
    @property
    def ostitl(self):
        return platform.uname()[0].title()  # Str
    @property
    def osver(self):
        return platform.uname()[2][:platform.uname()[2].find('-')].title()  # Str
    @property
    def plat(self):
        return sys.platform.upper()  # Str
    @property
    def proc(self):
        return platform.uname()[-1]  # Str
    @property
    def serr(self):
        return sys.stderr  # File object
    @property
    def sin(self):
        return sys.stdin  # File object
    @property
    def sout(self):
        return sys.stdout  # File object
    @property
    def ctime(self):
        return time.ctime()  # Str
    @property
    def localtime(self):
        return time.localtime()  # Time struct
    @property
    def isotime(self):
        return datetime.isoformat(datetime.today()) # Str
    @property
    def user(self):
        return pwd.getpwuid(os.getuid())[0]  # Str (getlogin can fail)
    @property
    def ver(self):
        return sys.version_info[0:3]  # List (python)
    @property
    def vers(self):
        return '.'.join(str(idx) for idx in self.ver)  # Str (python)

def ctu(istr):
    """Convert select ascii characters in string to unicode (image)"""
    ostr = unicode(istr)
    for ch, un in CTU.iteritems():
        ostr = ostr.replace(ch, un)
    return ostr

def auto_cast(string_):
    """Auto cast a field via pythonic syntax (eval)."""
    try:
        return evil(string_)
    except (ValueError, SyntaxError):
        return string_

def entry_exit(log):
    """Decorator for funciton entry/exit."""

    def decorator(func):
        """Actual decorator."""

        def log_final_time(func, t_i):
            """Log final function execution time."""
            t_f = time.time()
            log.debug("Exiting {} after: {:.3f} sec".format(func, t_f - t_i))

        @wraps(func)
        def wrapper(*args, **kwargs):
            """Replacement function."""
            date = datetime.isoformat(datetime.today())
            log.debug("Entering {} at: {}".format(func.__name__, date))
            t_i = time.time()
            try:
                rtn = func(*args, **kwargs)
            except:
                log_final_time(func.__name__, t_i)
                raise
            else:
                log_final_time(func.__name__, t_i)
            return rtn
        return wrapper

    return decorator
