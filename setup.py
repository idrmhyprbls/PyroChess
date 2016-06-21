from setuptools import setup, find_packages

# Import metadata
with open('./pyrochess/metadata.py') as infile:
    exec(compile(infile.read(), "./pyrochess/metadata.py", 'exec'))

# Grab license title
with open('./LICENSE') as infile:
    license = infile.readline().strip()

# Parse requirements
with open('./requirements.txt') as infile:
    recs = infile.readlines()

setup(
    name=__program__,
    version=__version__,
    url=__project__,
    license=license,
    author=__author__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=recs,
    entry_points='''
[console_scripts]
pyrochess=pyrochess.cli:main
''',
)
