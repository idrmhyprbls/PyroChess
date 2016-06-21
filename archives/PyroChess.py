#!/usr/bin/env python2
# -*- encoding: utf-8 -*-
"""A pre-alpha chess engine forged in the fires of Python awesomeness.

COPYRIGHT & LICENSE
===================

  - See below

USAGE
=====

  - `$ python %.py`
  - `$ ./%.py # if executable`
  - `$ nosetests %.py`

WARNING
=======

  - N/a

NOTE
====

  - Run all modules through pyflakes, pylint, & pydoc

TODO
====

  - Still in alpha...

"""
from __future__ import print_function, with_statement, division

__creator__ = "Matt Busby"
__date__ = "1 June, 2015"  # Created
__email__ = "@idrmhyprbls"  # GitHub
__program__ = "PyroChess"  # Title
__version__ = "0.1.0a"  # Release
__project__ = "https://github.com/idrmhyprbls/"  # Website
__author__ = "{} {}".format(__creator__, __email__)
__credits__ = "N/a"  # References  '\n'-separated
__contributors__ = "N/a"  # '\n'-separated
__compiler__ = "N/a"  # Designed with
__os__ = "Fedora 21 Linux 64bit"  # Designed on
__copyright__ = "Copyright (c) {year}, {owner}. ".format(
    owner=__author__,
    year="2015-2016") + \
    "All rights reserved."
__licence__      = """\
        BSD 3-Clause License

        {copyright}

        Redistribution and use in source and binary forms, with or without
        modification, are permitted provided that the following conditions
        are met:

        1. Redistributions of source code must retain the above copyright
           notice, this list of conditions and the following disclaimer.

        2. Redistributions in binary form must reproduce the above copyright
           notice, this list of conditions and the following disclaimer in
           the documentation and/or other materials provided with the
           distribution.

        3. Neither the name of the copyright holder nor the names of its
           contributors may be used to endorse or promote products derived
           from this software without specific prior written permission.

        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
        "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
        LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
        FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
        COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
        INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
        BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
        LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
        CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
        LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
        WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
        POSSIBILITY OF SUCH DAMAGE.
        """.format(copyright=__copyright__)

IMPORT_ERRORS = []  # Import errors to log after opt parsing for a logger level

from datetime import datetime
from functools import wraps
import argparse
import logging
import nose
import nose.tools
import os
import platform
import re
import string
import struct
import sys
import time

try:
    import pudb as pdb
except ImportError:
    IMPORT_ERRORS.append("Can't import 'pudb', using 'pdb'!")
    import pdb

# System
ARCH = "64bit" if struct.calcsize("P") else "32bit"  # OS
ARCHP = platform.architecture()[0]  # Current python
DATE = datetime.isoformat(datetime.today())
HOME = os.path.expanduser('~')
OS = platform.system()  # Darwin, Windows, Linux
PLAT = sys.platform  # darwin, win32, linux/linux2
PWD = os.getcwd()
REL = platform.release()  # Windows release else kernel version
USER = os.getlogin()
VER = "{}.{}".format(sys.version_info[0], sys.version_info[1])

# Game
DEBUG = True
GAME_TYPE = 'normal'
DNUM = {'normal': 8}[GAME_TYPE]  # 8, 16, ..
RANK = range(1, DNUM + 1)        # 1, 2, ..
FILE = string.lowercase[:DNUM]   # a, b, ..


def entry_exit(func):
    """Decorator."""
    def log_final_time(func, t_i):
        """Log final function execution time."""
        t_f = time.time()
        logging.debug("Exiting {} after: {:.3f} sec".format(func, t_f - t_i))

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Replacement."""
        logging.debug("Entering {}".format(func.__name__))
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


class TestModule(object):
    """Nose test class."""

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def setup_class(cls):
        """Sets up the test."""

    @classmethod
    def teardown_class(cls):
        """Tears down the test."""
        pass

    def test_main(self):
        """Test call to main."""
        nose.tools.eq_(main(), None)


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
            if pos >= 0 and pos < DNUM * DNUM:
                idx = pos
        elif isinstance(pos, str):
            idx = Square.str_to_idx(pos)
        return idx

    @staticmethod
    def idx_to_fr(square):
        if square is None or square < 0 or square >= DNUM * DNUM:
            logging.warn('{}'.format(square))
            return None, None
        return FILE[square % DNUM], (square // DNUM) + 1

    @staticmethod
    def fr_to_idx(file, rank):
        if rank is None or rank not in RANK or file is None or file not in FILE:
            return None
        return FILE.find(file) + (rank - 1) * 8

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
        return FILE[FILE.find(self.square.file) + 1:]

    def file_left(self):
        return reversed(FILE[:FILE.find(self.square.file)])

    def rank_up(self):
        return RANK[self.square.rank:]

    def rank_down(self):
        return reversed(RANK[:self.square.rank - 1])

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
            base_rank = DNUM - 1

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


class Board(object):

    def __init__(self):
        """"""
        self.new_game()

    def lookup(self, pos):
        idx = Square.lookup(pos)
        return self.squares[idx] if idx is not None else None

    def place(self, piece, pos):
        square = self.lookup(pos)
        if square:
            if piece.square is not None:  # If not assembling board
                if square not in piece.valid_moves(
                        self.squares):  # Check for valid move...
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

    def new_game(self):
        self.squares = [Square(idx) for idx in range(DNUM * DNUM)]
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
        self.add('w', Pawn, ('a', 2))
        self.add('w', Pawn, ('b', 2))
        self.add('w', Pawn, ('c', 2))
        self.add('w', Pawn, ('d', 2))
        self.add('w', Pawn, ('e', 2))
        self.add('w', Pawn, ('f', 2))
        self.add('w', Pawn, ('g', 2))
        self.add('w', Pawn, ('h', 2))
        self.add('b', King, ('e', 8))
        self.add('b', Queen, ('d', 8))
        self.add('b', Rook, ('a', 8))
        self.add('b', Rook, ('h', 8))
        self.add('b', Bishop, ('c', 8))
        self.add('b', Bishop, ('f', 8))
        self.add('b', Knight, ('b', 8))
        self.add('b', Knight, ('g', 8))
        self.add('b', Pawn, ('a', 7))
        self.add('b', Pawn, ('b', 7))
        self.add('b', Pawn, ('c', 7))
        self.add('b', Pawn, ('d', 7))
        self.add('b', Pawn, ('e', 7))
        self.add('b', Pawn, ('f', 7))
        self.add('b', Pawn, ('g', 7))
        self.add('b', Pawn, ('h', 7))

    def add(self, team, echelon, pos):
        (file, rank) = pos
        if team == 'w':
            piece = echelon(team)
            self.white.append(piece)
            self.place(piece, (file, rank))
        elif team == 'b':
            piece = echelon(team)
            self.black.append(piece)
            self.place(piece, (file, rank))
        else:
            raise ValueError

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
        rtn = '   {}\n'.format(' '.join([file.upper() for file in FILE]))
        for rank in reversed(RANK):
            rtn += '{0: 2d} '.format(rank)
            for file in FILE:
                rtn += str(self.lookup((file, rank)))
                rtn += ' '
            rtn += '{0:d}\n'.format(rank)
        rtn += '   {}'.format(' '.join([file.upper() for file in FILE]))
        return rtn


class Game(object):

    def __init__(self):
        """"""
        self.board = Board()
        self.turn = 0  # Turn 1: 0/1, Turn 2: 2/3 ..
        self.time_tot = None
        self.time_black = None
        self.time_white = None
        self.since_capture = None
        self.moves = [[],[]]

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
        for rank in reversed(RANK):
            line = ''
            repeat = 0
            for file in FILE:
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
            fen['lines'].append(line)
        fen['turn'] = 'b' if self.turn % 2 else 'w'
        fen['castle'] = 'KQkq'
        fen['enpassant'] = '-'
        fen['capture'] = '0'
        fen['moves'] = '1'

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
        3. 50-moves consecutive without a capture
        4. 3-move repitition, need not be consecutive
        """
        pass

    @staticmethod
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

    @staticmethod
    def parse_move(movestr):
        """

        Nc3, Nxc3, Nac3, Naxc3, c3, bxc3, b1c3

        """
        # Cleanup
        move = movestr.strip()
        move = move.lower()
        move.replace('?', '').replace('!', '').replace('+', '')

        logging.debug("Filtered move input: " + move)

        if not move or ' ' in move:
            raise SyntaxError(movestr)

        if '-' in move:
            castle = move.split('-')
            if len(castle) <= 1:
                from_,to_ = 'o','o'
            else:
                from_, to_ = 'o','oo'
        elif 'x' in move:
            from_, to_ = move.split('x')
        else:
            nums = re.findall('[0-9]+', move)

            if len(nums) > 1:
                idx = move.find(nums[0]) + len(nums[0])
                from_ = move[:idx]
                to_ = move[idx:]
            else:
                idx

        logging.debug("Move from, to: {}, {}".format(from_, to_))

        if echelon:
            move = move[1:]
            capture = 'x' in move
        if capture:
            move.replace('x', '')
        else:
            move.k  # YAH
        file = move[0] in FILE

        m1 = re.findall('[a-zA-Z]+', move)
        if not m1 or len(m1) < 2:
            return (None, None), (None, None)
        ffile = m1[0]
        tfile = m1[1]
        m2 = re.findall('[0-9]+', move)
        if not m2 or len(m2) < 2:
            return (None, None), (None, None)
        frank = int(m2[0])
        trank = int(m2[1])
        return (ffile, frank), (tfile, trank)

    @staticmethod
    def request_move():
        while True:
            try:
                move_input = raw_input()
                from_, to_ = Game.parse_move(move_input)
            except SyntaxError as err:
                logging.warning("Syntax error in move: " + str(err))
            else:
                return from_, to_

    def run(self):
        while True:
            print("===================================")
            print(self.to_fen())
            print('Score: {}'.format(self.score()))
            # print('Last move: {}'.format(move_input))
            print(self.board)
            self.board.move(Game.request_move())
            print("===================================")
            # self.board.update()
            # for each in self.board.white:
            #     print(each)
            print('Turn {}{}: '.format(self.turn // 2 + 1, 'b' if self.turn % 2
                                       else 'w'), end='')
            # self.turn += 1
            break


def parse_argv():
    "Parse input arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true',
                        default=DEBUG, help='debug')
    parser.add_argument('-m', '--post_mortem', action='store_true',
                        default=False, help='enter port mortem on exception')
    parser.add_argument('arg', metavar='A', type=str, nargs='?',
                        default='', help='optional arg')
    opts = parser.parse_args()  # OR opts, _ = parser.parse_known_args()
    return {'arg': opts.arg,
            'debug': opts.debug,
            'post_mortem': opts.post_mortem}


@entry_exit
def main():
    """..."""
    game = Game()
    game.run()

if __name__ == '__main__':
    # Global options
    OPT = parse_argv()

    # Configure logger
    fmat = r'%(asctime)s.%(msecs)-3d | ' + \
           r'%(levelname)-8s | ' + \
           r'{0:12s} | '.format(USER) + \
           r'%(filename)-15s | ' + \
           r'%(lineno)-5d | ' + \
           r'%(funcName)-20s | ' + \
           r'%(message)s'
    ftime = r'%y-%m-%d %H:%M:%S'
    if OPT.get('debug'):
        logging.basicConfig(level=logging.DEBUG, format=fmat, datefmt=ftime)
    else:
        logging.basicConfig(level=logging.WARN, format=fmat, datefmt=ftime)
    logging.debug("Module loaded at: {}".format(DATE))

    # Print any import issues."""
    for each in IMPORT_ERRORS:
        logging.warn(each)
    del IMPORT_ERRORS

    # Clear screen on start
    if OPT.get('cls'):
        if 'win' in OS:
            os.system("cls")
        else:
            os.system("clear")
    try:
        main()
    except KeyboardInterrupt:
        sys.stdout.flush()
        sys.stderr.flush()
    except Exception as err:
        # Unhandeld exception
        if OPT.get('post_mortem'):
            logging.exception(err)
            pdb.post_mortem()  # 'e' to view
        else:
            raise
    else:
        # Wait for exit confirmation
        if OPT.get('pause'):
            raw_input("Press ENTER to continue...")
else:
    # If imported
    pass
