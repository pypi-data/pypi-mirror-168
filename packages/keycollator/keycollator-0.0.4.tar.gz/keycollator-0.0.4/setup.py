from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='keycollator',
    version='0.0.4',
    long_description=long_description,
    py_modules=[
        'cli',
        'extractonator'
    ],
    install_requires=[
        'click',
        'progressbar',
        'verboselogs',
        'nltk',
        'fuzzywuzzy',
        'python-Levenshtein',
        'halo',
        'termtables',
        'datetime',
        'pytest'
    ],
    entry_points='''
        [console_scripts]
        keycollator=keycollator:main
    '''
)
