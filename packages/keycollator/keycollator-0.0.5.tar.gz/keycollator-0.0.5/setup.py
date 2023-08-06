from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='keycollator',
    version='0.0.5',
    long_description=long_description,
    url="https://github.com/davidprush/keycollator",
    author="David Rush",
    author_email="davidprush@gmail.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Topic :: Office/Business",
        "Topic :: Software Development :: Testing",
        "Topic :: Text Processing",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    py_modules=[
        'cli',
        'extractonator'
    ],
    install_requires=[
        'click>=8.0.2',
        'datetime>=4.7',
        'fuzzywuzzy>=0.18.0',
        'halo>=0.0.31',
        'nltk>=3.7',
        'python-Levenshtein>=0.12.2',
        'termtables>=0.2.4'
    ],
    entry_points='''
        [console_scripts]
        keycollator=keycollator:main
    '''
)
