"""PyroChess: A shi**y chess engine forged in the fires of Python awesomeness.

{}
"""

# Import metadata
with open('./pyrochess/metadata.py') as infile:
    exec(compile(infile.read(), "./pyrochess/metadata.py", 'exec'))
try:
    del infile
except NameError:
    pass

__doc__ = __doc__.format(__license__)
