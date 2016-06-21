# -*- coding: utf-8 -*-

from functools import wraps
import logging
import exceptions
import time

LOG = logging.getLogger(__name__)

# Character to unicode
CTU = {'K':u'♔', 'Q':u'♕', 'R':u'♖', 'B':u'♗', 'N':u'♘', 'P':u'♙',
       'k':u'♚', 'q':u'♛', 'r':u'♜', 'b':u'♝', 'n':u'♞', 'p':u'♟'}

def ctu(istr):
    """Convert select ascii characters in string to unicode (image)"""
    ostr = unicode(istr)
    for ch,un in CTU.iteritems():
        ostr = ostr.replace(ch, un)
    return ostr

def entry_exit(func):
    """Decorator for funciton entry/exit."""
    def log_final_time(func, t_i):
        """Log final function execution time."""
        t_f = time.time()
        LOG.debug("Exiting {} after: {:.3f} sec".format(func, t_f - t_i))

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Replacement function."""
        LOG.debug("Entering {}".format(func.__name__))
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

class BadInputWarn(exceptions.Warning):
    """Bad user input."""
    pass
