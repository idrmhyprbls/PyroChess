#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

import logging

from pyrochess.config import SETTINGS
from pyrochess.square import Square
from pyrochess.metadata import PROGRAM

LOG = logging.getLogger(PROGRAM)

class Piece(object):
    point = 0.

    def __init__(self, team, square=None):
        """"""
        self.team = team
        self.square = square
        self.symbol = '?'
        self.en_passant = False

    def __str__(self):
        return '{}: {}({}) {}\n'.format(
            self.team,
            self.symbol,
            self.point,
            repr(self.square))

    def active(self):
        return self.square is not None

    def capture(self):
        self.square = None
        self.point = 0.

    def valid_move(self, pos):
        return True

    def valid_moves(self, squares):
        return squares

    def file_right(self):
        return SETTINGS.file[SETTINGS.file.find(self.square.file) + 1:]

    def file_left(self):
        return reversed(SETTINGS.file[:SETTINGS.file.find(self.square.file)])

    def rank_up(self):
        return SETTINGS.rank[self.square.rank:]

    def rank_down(self):
        return reversed(SETTINGS.rank[:self.square.rank - 1])

    def fr_ur(self):
        return zip(self.file_right(), self.rank_up())

    def fr_dr(self):
        return zip(self.file_right(), self.rank_down())

    def fr_dl(self):
        return zip(self.file_left(), self.rank_down())

    def fr_ul(self):
        return zip(self.file_left(), self.rank_up())


class King(Piece):
    point = 1000.  # 3.3 Attack

    def __init__(self, *args, **kwargs):
        """"""
        super(King, self).__init__(*args, **kwargs)
        self.symbol = 'k' if self.team == 'b' else 'K'

    def valid_moves(self, squares):
        idxs = []
        for file, rank in ((0, 1), (1, 1), (1, 0), (1, -1),
                           (0, -1), (-1, -1), (-1, 0), (-1, 1)):
            flu = chr(ord(self.square.file) + file)
            rlu = self.square.rank + rank
            idx = Square.lookup((flu, rlu))
            if idx:
                idxs.append(idx)
        moves = []
        for idx in idxs:
            square = squares[idx]
            if square.occupied() and square.piece.team == self.team:
                continue
            moves.append(square)
        return moves


class Queen(Piece):
    point = 9.

    def __init__(self, *args, **kwargs):
        """"""
        super(Queen, self).__init__(*args, **kwargs)
        self.symbol = 'q' if self.team == 'b' else 'Q'

    def valid_moves(self, squares):
        # TODO Probably not going to work
        return Rook(self.team, self.square).valid_moves(squares) + \
            Bishop(self.team, self.square).valid_moves(squares)


class Rook(Piece):
    point = 5.

    def __init__(self, *args, **kwargs):
        """"""
        super(Rook, self).__init__(*args, **kwargs)
        self.symbol = 'r' if self.team == 'b' else 'R'

    def valid_moves(self, squares):
        moves = []
        for method in (self.file_right, self.file_left):
            for file in method():
                square = squares[Square.lookup((file, self.square.rank))]
                if not square.occupied():
                    moves.append(square)
                elif square.piece.team != self.team:
                    moves.append(square)
                    break
                else:
                    break
        for method in (self.rank_up, self.rank_down):
            for rank in method():
                square = squares[Square.lookup((self.square.file, rank))]
                if not square.occupied():
                    moves.append(square)
                elif square.piece.team != self.team:
                    moves.append(square)
                    break
                else:
                    break
        return moves


class Bishop(Piece):
    point = 3.25

    def __init__(self, *args, **kwargs):
        """"""
        super(Bishop, self).__init__(*args, **kwargs)
        self.symbol = 'b' if self.team == 'b' else 'B'

    def valid_moves(self, squares):
        moves = []
        for method in (self.fr_ur, self.fr_dr, self.fr_dl, self.fr_ul):
            for file, rank in method():
                square = squares[Square.lookup((file, rank))]
                if not square.occupied():
                    moves.append(square)
                elif square.piece.team != self.team:
                    moves.append(square)
                    break
                else:
                    break
        return moves


class Knight(Piece):
    point = 3.

    def __init__(self, *args, **kwargs):
        """"""
        super(Knight, self).__init__(*args, **kwargs)
        self.symbol = 'n' if self.team == 'b' else 'N'

    def valid_moves(self, squares):
        # TODO Use an iterator
        idxs = []
        for file, rank in ((1, 2), (2, 1), (2, -1), (1, -2),
                           (-1, -2), (-2, -1), (-2, 1), (-1, 2)):
            flu = chr(ord(self.square.file) + file)
            rlu = self.square.rank + rank
            idx = Square.lookup((flu, rlu))
            if idx:
                idxs.append(idx)
        moves = []
        for idx in idxs:
            square = squares[idx]
            if square.occupied() and square.piece.team == self.team:
                continue
            moves.append(square)
        return moves


class Pawn(Piece):
    point = 1.

    def __init__(self, *args, **kwargs):
        """"""
        super(Pawn, self).__init__(*args, **kwargs)
        self.symbol = 'p' if self.team == 'b' else 'P'
        self.en_passant = False

    def valid_moves(self, squares):
        moves = []
        if self.team == 'w':
            step = 1
            base_rank = 2
        else:
            step = -1
            base_rank = SETTINGS.dnum - 1

        # Captures
        for file_dir in (-1, 1):
            idx = Square.lookup((chr(ord(self.square.file) + file_dir),
                                 self.square.rank + step))
            if idx:
                square = squares[idx]
                if square.occupied() and square.piece.team != self.team:
                    moves.append(square)

        # Forward single moves
        idx = Square.lookup((self.square.file, self.square.rank + step))
        if idx:
            square = squares[idx]
            if not square.occupied():
                moves.append(square)

        # Forward double move
        if self.square.rank == base_rank:
            idx = Square.lookup((self.square.file, self.square.rank +
                                 2 * step))
            if idx:
                square = squares[idx]
                if not square.occupied():
                    moves.append(square)
        return moves
