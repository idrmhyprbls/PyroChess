#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""{}, v{}
{}

{}

Created {}, {}.

LICENSE

{}

REPO

{}

USAGE

{}

WARNING

{}

NOTES

{}

"""

from __future__ import with_statement

# Manual entry, dynamic

CONTRIBUTORS = [
        "Matt Busby",
        ]

PYTHON = "2.7.11"

USAGE = """\
`python %.py`
`./%.py # if executable`
`nosetests %.py`"""

WARNING = "N/a"

NOTES = "Run all modules through pyflakes, pylint, & pydoc"

# Manual entry, static

PROGRAM = "PyroChess"
PROJECT = "https://github.com/idrmhyprbls/PyroChess"
BRIEF = "A shi**y chess engine forged in the fires of Python awesomeness."
OS = "Fedora Linux 24, 64bit"
CREATOR = "Matt Busby"
EMAIL = "@idrmhyprbls"
CREATED = "1 June, 2015"

# Autogenerated

AUTHOR = "{} {}".format(CREATOR, EMAIL)
CREDITS = CONTRIBUTORS

VERSION = "?.?.?"
DATE = "??/????"
try:
    # Version info MUST be in ./RELEASE.md !!
    with open('./RELEASE.md') as ifile:
        import re
        for each in ifile:
            match = re.search(
                    '([0-9]{1,2}\.){2}[0-9]{1,2}\s+[0-9]{1,2}/[0-9]{2,4}',
                    each)
            if match:
                VERSION, DATE = match.group().split()
                break
        del re
except:
    pass
else:
    del ifile

LICENSE = "BSD-3-Clause"
try:
    # License and Copyright MUST be update in ../LICENSE !!
    with open('./LICENSE') as ifile:
        LICENSE = "".join(ifile.readlines())
except:
    pass
else:
    del ifile

COPYRIGHT = "Matt Busby @MrMattBusby"
for line in LICENSE.split('\n'):
    if 'copyright' in line.lower():
        COPYRIGHT = line.strip()
        break
del line

# Docstring

__doc__ = __doc__.format(PROGRAM,
        VERSION,
        '=' * (3 + len(PROGRAM) + len(VERSION)),
        BRIEF,
        CREATOR,
        CREATED,
        LICENSE,
        PROJECT,
        USAGE,
        WARNING,
        NOTES)
