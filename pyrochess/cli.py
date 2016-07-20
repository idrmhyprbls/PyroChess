from __future__ import print_function, with_statement, division

from datetime import datetime
DATE = datetime.isoformat(datetime.today())
import os
USER = os.getlogin()

import logging
import sys

# Third party
import click

# Internal
from .main import mainloop
import config

@click.command(context_settings=dict(help_option_names=['-h','--help']))
@click.option('-v','--verbose', is_flag=True, default=False, help='Log at info level')
@click.option('-d','--debug', is_flag=True, default=False, help='Log at debug level')
@click.option('-u','--unicode', is_flag=True, default=False, help='Display unicode pieces')
@click.option('--game', default='normal', type=click.Choice(['normal']), help='Select game type')
def main(verbose, debug, unicode, game):
    config.settings.verbose = verbose
    config.settings.debug = debug
    config.settings.unicode = unicode
    config.settings.set_game(game)

    # Configure logger
    fmat = r'%(asctime)s.%(msecs)-3d | ' + \
           r'%(levelname)-8s | ' + \
           r'{0:12s} | '.format(USER) + \
           r'%(filename)-15s | ' + \
           r'%(lineno)-5d | ' + \
           r'%(funcName)-20s | ' + \
           r'%(message)s'
    ftime = r'%y-%m-%d %H:%M:%S'
    if config.settings.debug:
        logging.basicConfig(level=logging.DEBUG, format=fmat, datefmt=ftime)
    elif config.settings.verbose:
        logging.basicConfig(level=logging.INFO, format=fmat, datefmt=ftime)
    else:
        logging.basicConfig(level=logging.WARN, format=fmat, datefmt=ftime)
    log = logging.getLogger(__name__)
    log.debug("{} begun at: {}".format(__package__, DATE))

    # Main loop
    mainloop()
