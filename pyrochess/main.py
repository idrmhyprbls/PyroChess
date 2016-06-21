import logging
import sys

import utils
from .game import Game

IMPORT_ERRORS = []
try:
    import pudb as pdb
except ImportError:
    IMPORT_ERRORS.append("Can't import 'pudb', using 'pdb'!")
    import pdb

LOG = logging.getLogger(__name__)

@utils.entry_exit
def mainloop(): # cli=True):
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
        if 0: # TODO
            LOG.exception(err)
            pdb.post_mortem()  # 'e' to view
        else:
            raise
