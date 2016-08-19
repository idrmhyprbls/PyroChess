#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

import logging

from pyrochess.config import SETTINGS
from pyrochess.metadata import PROGRAM

LOG = logging.getLogger(PROGRAM)

class Square(object):

    def __init__(self, idx):
        self.idx = idx
        self.file, self.rank = Square.idx_to_fr(idx)
        self.piece = None
        self.contended_black = []
        self.contended_white = []
        self.en_passant = False

    def __repr__(self):
        if self.occupied():
            return '{}{}:{}'.format(self.file, self.rank, self.piece.symbol)
        return '{}{}:-'.format(self.file, self.rank)

    def __str__(self):
        if self.occupied():
            return '{}'.format(self.piece.symbol)
        return '-'

    def occupied(self):
        return self.piece is not None

    def clear(self):
        if self.piece is not None:
            self.piece.capture()
            self.piece = None

    @staticmethod
    def lookup(pos):
        idx = None
        if isinstance(pos, Square):
            idx = pos.idx
        elif isinstance(pos, tuple):
            idx = Square.fr_to_idx(*pos)
        elif isinstance(pos, int):
            if pos >= 0 and pos < SETTINGS.dnum * SETTINGS.dnum:
                idx = pos
            else:
                LOG.warning("Invalid Square.lookup pos = {}".format(pos))
        elif isinstance(pos, str):
            idx = Square.str_to_idx(pos)
        return idx

    @staticmethod
    def idx_to_fr(square):
        if square is None or square < 0 or square >= SETTINGS.dnum * SETTINGS.dnum:
            LOG.warn('{}'.format(square))
            return None, None
        return SETTINGS.file[square %
                             SETTINGS.dnum], (square // SETTINGS.dnum) + 1

    @staticmethod
    def fr_to_idx(file, rank):
        if rank is None or rank not in SETTINGS.rank or file is None or file not in SETTINGS.file:
            return None
        return SETTINGS.file.find(file) + (rank - 1) * 8

    @staticmethod
    def box_to_fr(box):
        """E.g. 'h2'"""
        try:
            return box[0], int(box[1:])
        except:
            return None, None

    @staticmethod
    def str_to_idx(box):
        try:
            return Square.fr_to_idx(box[0], int(box[1:]))
        except:
            return None
