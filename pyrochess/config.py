# import struct
# import sys
import string
# import platform
# import os

# ARCH = "64bit" if struct.calcsize("P") else "32bit"  # OS
# ARCHP = platform.architecture()[0]  # Current python
# HOME = os.path.expanduser('~')
# OS = platform.system()  # Darwin, Windows, Linux
# PLAT = sys.platform  # darwin, win32, linux/linux2
# PWD = os.getcwd()
# REL = platform.release()  # Windows release else kernel version
# VER = "{}.{}".format(sys.version_info[0], sys.version_info[1])

class Settings(object):
    games = {'normal': 8}
    def __init__(self):
        self.verbose = False
        self.debug = False
        self.unicode = False
        self.game = 'normal'
        self.dnum = 0
        self.rank = []
        self.file = ''
    def set_game(self, game):
        self.game = game
        self.dnum = Settings.games[self.game]  # 8, 16, ..
        self.rank = xrange(1, self.dnum + 1) # 1, 2, ..
        self.file = string.lowercase[:self.dnum] # a, b, ..
    def __str__(self):
        return "Settings(" + ", ".join(["{}={}".format(k,v) for k,v in self.__dict__.iteritems()]) + ")"

settings = Settings()
