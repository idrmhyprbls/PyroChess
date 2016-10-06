#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Command Line Interface"""
from __future__ import absolute_import, print_function

import os
import pwd
import sys

import click

from pyrochess.mainloop import mainloop
from pyrochess import config
from pyrochess import logger
from pyrochess import metadata

@click.command(context_settings=dict(help_option_names=['-h', '--help']),
               help=metadata.__doc__)
@click.option('-q', '--quiet',
              default=None, is_flag=True, help='Stream log at error level.')
@click.option('-v', '--verbose',
              default=None, is_flag=True, help='Stream log at info level.')
@click.option('-d', '--debug',
              default=None, is_flag=True, help='Stream log at debug level.')
@click.option('-u', '--unicode',
              default=None, is_flag=True, help='Display unicode pieces.')
@click.option('-V', '--version',
              default=None, is_flag=True, help='Display version.')
@click.option('--conf',
              default=None, type=str, help='.ini conf file location [~/.pyrochess].')
@click.option('--log',
              default=None, type=str, help='Log file location.')
@click.option('--game',
              default=None, type=click.Choice(['normal']),
              help='Select game type.')
def main(quiet, verbose, debug, unicode, version, conf, log, game):
         
    # Version info ('help' is handled by click)
    if version:
        from pyrochess import VERSION  # , VERSION_INFO
        print("{}".format(VERSION))
        # print("{}".format(VERSION_INFO))
        return

    # Reload config file
    if conf is not None:
        config.SETTINGS.load_config(conf)

    # Verbosity
    if quiet is not None:
        config.SETTINGS.quiet = True
        config.SETTINGS.debug = False
        config.SETTINGS.verbose = False
    elif debug is not None:
        config.SETTINGS.quiet = False
        config.SETTINGS.debug = True
        config.SETTINGS.verbose = False
    elif verbose is not None:
        config.SETTINGS.quiet = False
        config.SETTINGS.debug = False
        config.SETTINGS.verbose = True
    logger.set_log_level(config.SETTINGS)

    # Game options
    if unicode is not None:
        config.SETTINGS.unicode = True
    if game is not None:
        config.SETTINGS.set_game(game)

    # Update logging
    if log is not None:
        config.SETTINGS.log = log
        logger.add_file_handler(config.SETTINGS)

    # Main loop
    mainloop()
