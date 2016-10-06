#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Game class"""
from __future__ import absolute_import, division, print_function

import logging
import re

from pyrochess.config import SETTINGS
from pyrochess.piece import King, Queen, Rook, Bishop, Knight, Pawn
from pyrochess.board import Board
from pyrochess.square import Square
from pyrochess.metadata import PROGRAM
from pyrochess.utils import ALPHANUMERIC, BadInputWarn

LOG = logging.getLogger(PROGRAM)

class Game(object):

    def __init__(self):
        """"""
        self.board = Board()
        self.moveno = 0  # Even = White
        self.time_tot = None
        self.time_black = None
        self.time_white = None
        self.since_capture = None
        self.moves = [[], []]

    @property
    def turn(self):
        return 'b' if self.moveno % 2 else 'w'

    def score(self):
        """"""
        score = [0., 0.]
        for piece in self.board.white:
            score[0] += piece.point
        for piece in self.board.black:
            score[1] -= piece.point
        return sum(score)

    def to_json(self):
        """"""
        pass

    def to_fen(self):
        """"""
        fen = {}
        fen['lines'] = []
        repeat = 0
        for rank in reversed(SETTINGS.rank):
            line = ''
            repeat = 0
            for file in SETTINGS.file:
                square = self.board.lookup((file, rank))
                if square.occupied():
                    if repeat != 0:
                        line += str(repeat)
                        repeat = 0
                    line += str(square)
                else:
                    repeat += 1
            if repeat != 0:
                line += str(repeat)
                repeat = 0
            line = line
            fen['lines'].append(line)
        fen['turn'] = self.turn
        fen['castle'] = 'KQkq'
        fen['enpassant'] = '-'
        fen['capture'] = '0'
        fen['moves'] = '1'  # Full moves

        return ' '.join(['/'.join(fen['lines']),
                         fen['turn'], fen['castle'], fen['enpassant'],
                         fen['capture'], fen['moves']])

    def to_pgn(self):
        """"""
        pass

    def is_draw(self):
        """
        1. Draw offer
        2. Stalemate with no moves possible
        3. Too few pieces (k vs K)
        4. 50-moves consecutive without a capture
        5. 3-move repitition, need not be consecutive
        """
        pass

    def get_move(self, rinput=None):
        if rinput:
            move_input = rinput
        else:
            move_input = raw_input("Enter move: ")
        try:
            echelon, from_str, to_str = Game.parse_move_str(move_input)
        except BadInputWarn as err:
            LOG.warning("Syntax error in move: \"{}\"".format(err))
        except EOFError as err:
            LOG.info("Abort requested")
            raise SystemExit
        else:
            return self.turn, echelon, from_str, to_str

    def move(self, team, echelon, from_str, to_str):
        """TODO"""
        if to_str == '0':
            pass
        elif to_str == '00':
            pass
        else:
            to_sq = Square.lookup(to_str)
        if from_str:
            pass
        else:
            pass
        return from_str, to_str
        pass

    def run(self):
        if not SETTINGS.imported:
            while True:
                print(self.to_fen())
                print('Score: {}'.format(self.score()))
                # print('Last move: {}'.format(move_input))
                if SETTINGS.unicode:
                    print(unicode(self.board))
                else:
                    print(self.board)
                while True:
                    try:
                        move = self.get_move()
                        if move is not None:
                            self.move(*move)
                    except SystemExit:
                        try:
                            if not SETTINGS.testing:
                                ans = raw_input("\nExit, really ([Y]/n)? ")
                            else:
                                ans = 'y'
                        except EOFError:
                            raise SystemExit
                        if not ans or ans[0] in 'yY':
                            raise SystemExit
                # self.board.update()
                # for each in self.board.white:
                #     print(each)
                print('Turn {}{}: '.format(self.turn // 2 + 1, 'b' if self.turn % 2
                                        else 'w'), end='')
                # self.turn += 1
                break

    @staticmethod
    def parse_move_str(movestr):
        """

        Pass: Bb3, Bxb3, Bba3, B3b2, Bbxa3, b3, cxb3, b1b3, o-o, O-O-O
        Fail: Ab3, a3a, 3a, 3a3, a33a, a3a3, a2a1, a333, a3a33, a3z3, a3z, 000, ad
        TODO: Check above

        """
        # Cleanup
        movestr = movestr.strip()
        movestr = movestr.replace('?', '').replace('!', '')
        movestr = movestr.replace('+', '').replace(' ', '-')
        movestr = movestr.replace('X', 'x')

        # No space
        if not movestr or not all([each in (ALPHANUMERIC + '-')
                for each in movestr]):
            raise BadInputWarn(movestr)

        LOG.debug("Filtered move input: " + movestr)

        # Parse string
        from_str, to_str = '', ''
        if '-' in movestr:
            # *-*, *-*-*
            dash = movestr.split('-')
            if len(dash) == 2:
                if dash[0][0] in 'oO0':
                    from_str = '0'
                    to_str = '0'
                else:
                    from_str, to_str = dash
            elif len(dash) == 3 and dash[0][0] in 'oO0':
                from_str = '0'
                to_str = '00'
            else:
                raise BadInputWarn(movestr)
        elif 'x' in movestr:
            # *x*
            from_str, to_str = movestr.split('x')
        else:
            castle = re.findall('[0oO]+', movestr)
            if len(castle)==1 and 2<=len(castle[0])<=3:
                # oo, 000
                if len(castle[0]) == 2:
                    from_str = '0'
                    to_str = '0'
                else:
                    from_str = '0'
                    to_str = '00'
            else:
                nums = re.findall('[0-9]+', movestr)
                if len(nums) > 1:
                    # *#
                    idx = movestr.find(nums[0]) + len(nums[0])
                    from_str = movestr[:idx]
                    to_str = movestr[idx:]
                else:
                    alph = re.findall('[a-z]+', movestr)
                    if len(alph) and len(alph[0]) == 1:
                        # **#
                        idx = movestr.find(alph[0])
                        from_str = movestr[:idx]
                        to_str = movestr[idx:]
                    else:
                        lowr = re.findall('[a-z]', movestr)
                        if len(lowr) == 1:
                            idx = movestr.find(lowr[0])
                            from_str = movestr[:idx]
                            to_str = movestr[idx:]
                        else:
                            idx = movestr.find(lowr[0]) + len(lowr[0])
                            if idx >= 0:
                                from_str = movestr[:idx]
                                to_str = movestr[idx:]
                            else:
                                raise BadInputWarn(movestr)
        if not from_str and not to_str:
            raise BadInputWarn(movestr)
        LOG.debug("Move from, to: {}, {}".format(from_str, to_str))

        # Determine echelon
        echelon = None  # Castling
        if not from_str:
            echelon = Pawn
        else:
            char = from_str[0]
            if char == 'K':
                echelon = King
            elif char == 'Q':
                echelon = Queen
            elif char == 'N':
                echelon = Knight
            elif char == 'B':
                echelon = Bishop
            elif char == 'R':
                echelon = Rook
        LOG.debug("Echelon is " + str(echelon))

        return echelon, from_str, to_str

        # Get entities, find row/col

        # file = move[0] in FILE

        # m1 = re.findall('[a-zA-Z]+', move)
        # if not m1 or len(m1) < 2:
        #     return (None, None), (None, None)
        # ffile = m1[0]
        # tfile = m1[1]
        # m2 = re.findall('[0-9]+', move)
        # if not m2 or len(m2) < 2:
        #     return (None, None), (None, None)
        # frank = int(m2[0])
        # trank = int(m2[1])

        # return (ffile, frank), (tfile, trank)

    '''
    def parse_box(box):
        match = re.match('[a-zA-Z]+', box)
        if not match:
            return None, None
        file = match.group()
        match = re.search('[0-9]+', box)
        if not match:
            return None, None
        rank = int(match.group())
        return tuple([file, rank])
    '''

