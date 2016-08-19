#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from ast import literal_eval as evil
from functools import wraps
from datetime import datetime
import exceptions
import time
import string

# WARNING: No local module imports!

ALPHANUMERIC = string.letters + string.digits

# Character to unicode
CTU = {'K': u'♔', 'Q': u'♕', 'R': u'♖', 'B': u'♗', 'N': u'♘', 'P': u'♙',
       'k': u'♚', 'q': u'♛', 'r': u'♜', 'b': u'♝', 'n': u'♞', 'p': u'♟'}

class BadInputWarn(exceptions.Warning):
    """Bad user input."""
    pass

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
