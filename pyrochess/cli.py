#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

import os
import pwd
import sys

import click

from pyrochess import config

from pyrochess.mainloop import mainloop
from pyrochess import logger
from pyrochess import metadata

@click.command(context_settings=dict(help_option_names=['-h', '--help']),
               help=metadata.__doc__)
@click.option('-q', '--quiet',
              default=None, is_flag=True, help='Stream log at error level')
@click.option('-v', '--verbose',
              default=None, is_flag=True, help='Stream log at info level')
@click.option('-d', '--debug',
              default=None, is_flag=True, help='Stream log at debug level')
@click.option('-u', '--unicode',
              default=None, is_flag=True, help='Display unicode pieces')
@click.option('--conf',
              default=None, type=str, help='.ini conf file location [~/.pyrochess]')
@click.option('--log',
              default=None, type=str, help='Log file location')
@click.option('--game',
              default=None, type=click.Choice(['normal']),
              help='Select game type')
def main(quiet, verbose, debug, unicode, conf, log, game):
         

    # Reload config file
    if conf is not None:
        config.settings.load_config(conf)

    # Verbosity
    if quiet is not None:
        config.settings.quiet = True
        config.settings.debug = False
        config.settings.verbose = False
    elif debug is not None:
        config.settings.quiet = False
        config.settings.debug = True
        config.settings.verbose = False
    elif verbose is not None:
        config.settings.quiet = False
        config.settings.debug = False
        config.settings.verbose = True
    logger.set_log_level(config.settings)

    # Game options
    if unicode is not None:
        config.settings.unicode = True
    if game is not None:
        config.settings.set_game(game)

    # Update logging
    if log is not None:
        config.settings.log = log
        logger.add_file_handler(config.settings)

    # Main loop
    from pyrochess.metadata import program
    # print(loggr.__dict__)
    # print(loggr.handlers[1].__dict__)
    # loggr.setLevel(logging.DEBUG)
    mainloop()
