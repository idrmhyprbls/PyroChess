#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Board class"""
from __future__ import absolute_import, division

import logging

from pyrochess.config import SETTINGS
from pyrochess.square import Square
from pyrochess.piece import King, Queen, Rook, Bishop, Knight, Pawn
from pyrochess.metadata import PROGRAM
from pyrochess import utils

LOG = logging.getLogger(PROGRAM)

class Board(object):

    def __init__(self):
        """New game board."""
        self.squares = [
            Square(idx) for idx in range(
                SETTINGS.dnum *
                SETTINGS.dnum)]

        self.white = []
        self.black = []

        self.add('w', King, ('e', 1))
        self.add('w', Queen, ('d', 1))
        self.add('w', Rook, ('a', 1))
        self.add('w', Rook, ('h', 1))
        self.add('w', Bishop, ('c', 1))
        self.add('w', Bishop, ('f', 1))
        self.add('w', Knight, ('b', 1))
        self.add('w', Knight, ('g', 1))
        for file in 'abcdefgh':
            self.add('w', Pawn, (file, 2))
        self.add('b', King, ('e', 8))
        self.add('b', Queen, ('d', 8))
        self.add('b', Rook, ('a', 8))
        self.add('b', Rook, ('h', 8))
        self.add('b', Bishop, ('c', 8))
        self.add('b', Bishop, ('f', 8))
        self.add('b', Knight, ('b', 8))
        self.add('b', Knight, ('g', 8))
        for file in 'abcdefgh':
            self.add('b', Pawn, (file, 7))

    def lookup(self, pos):
        idx = Square.lookup(pos)
        return self.squares[idx] if idx is not None else None

    def place(self, piece, pos):
        square = self.lookup(pos)
        if square:
            if piece.square is not None:  # If not assembling board
                if square not in piece.valid_moves(
                        self.squares):  # Check for valid move...TODO NO, do this is game, board should just be dumb
                    return None
                piece.square.piece = None  # Remove last location
            square.clear()  # Capture any piece on square
            square.piece = piece
            piece.square = square
            return piece
        else:
            return None

    def occupied(self, pos):
        square = self.lookup(pos)
        return square and square.occupied()

    def add(self, team, cpiece, pos):
        (file, rank) = pos
        if team == 'w':
            piece = cpiece(team)
            self.white.append(piece)
            self.place(piece, (file, rank))
        else:
            piece = cpiece(team)
            self.black.append(piece)
            self.place(piece, (file, rank))

    def move(self, fpos, tpos):
        fsquare = self.lookup(fpos)
        tsquare = self.lookup(tpos)
        if fsquare is None:
            return None
        if tsquare is None:
            return None
        if not fsquare.occupied():
            return None
        return self.place(fsquare.piece, tsquare)

    def update(self):
        # Update contended squares TODO needed?
        pass

    def __str__(self):
        """"""
        rtn = u'   {}\n'.format(u' '.join(SETTINGS.file))
        for rank in reversed(SETTINGS.rank):
            rtn += u'{0: 2d} '.format(rank)
            for file in SETTINGS.file:
                if SETTINGS.unicode:
                    rtn += utils.ctu(str(self.lookup((file, rank))))
                else:
                    rtn += str(self.lookup((file, rank)))
                rtn += u' '
            rtn += u'{0:d}\n'.format(rank)
        rtn += u'   {}'.format(' '.join(SETTINGS.file))
        return rtn
