keycollator
===========

::

    Compares text in a file to reference/glossary/key-items/dictionary file.

Built by 'David Rush <https://github.com/davidprush>'

---------------------

|Github| |Downloads| |Build Status|

****

The latest version of this document can be found at
<https://github.com/davidprush/keycollator/blob/main/README.rst>; 
if you are viewing it there (via HTTPS), you can download 
the Markdown/reStructuredText source at 
<https://github.com/davidprush/keycollator>. You can contact 
the author via e-mail at <davidprush@gmail.com>.

****

Features
========

- Extract text from file to dictionary
- Extract keys from file to dictionary
- Find matches of keys in text file
- Apply fuzzy matching

Installation
============

- Future plans to install as python package

.. code:: bash
    
    pip install keycollator

Documentation
=============

Official documentation can be found here:
https://github.com/davidprush


Supported File Formats
======================

- TXT files (Mac/Linux/Win)
- Plans to add PDF, CSV, and JSON

Usage
=====

- Import it into Python Projects

    from keycollator import extractionator

CLI
===

keycollator uses the CLI to change default parameters and functions

.. code:: bash

    Usage: keycollator.py [OPTIONS] COMMAND [ARGS]...

      keycollator is an app that finds occurances of keys in a text file

    Options:
      -v, --set-verbose               Turn on verbose
      -f, --fuzzy-matching INTEGER RANGE
                                      Find valid matches using edit distances or
                                      approximate matches, uses acceptance ratio
                                      of integer values from 0 to 99, where 99 is
                                      near identical  [0<=x<=99]
      -k, --key-file PATH             Path/file name of the key file containing a
                                      dictionary, key items, glossary, or
                                      reference list used to search the text file
      -t, --text-file PATH            Path/file name of the text to be searched
                                      for against items in the key file
      -o, --output-file PATH          Path/file name of the output file that
                                      will contain the results (CSV or TXT)
      -U, --ubound-limit INTEGER RANGE
                                      Ignores items from the results with matches
                                      greater than the upper boundary (upper-
                                      limit); reduce eroneous matches
                                      [1<=x<=99999]
      -L, --lbound-limit INTEGER RANGE
                                      Ignores items from the results with matches
                                      less than the lower boundary (lower-limit);
                                      reduce eroneous matches  [0<=x<=99999]
      -l, --set-logging               Turn on logging
      -Z, --log-file PATH             Path/file name to be used for the log file
      --help                          Show this message and exit.


- Applying fuzzy matching

    For fuzzy matching use

    .. code:: bash
        
        keycollator -f=[1-99]

- Setting the dictionary file (simple text file with items separated by line)

    Set the dictionary file

    .. code:: bash

        keycollator -d=/path/to/dictionary/directory/

- Create a log file

    To create a log file, execute

    .. code:: bash

      keycollator -l=/path/to/log_file/directory/

- Specify the CSV results file

    Specify the results csv file name, execute

    .. code:: bash

        keycollator -c=/path/to/results/file.csv

- Add verbosity

    Turn on verbose:

    .. code:: bash

        keycollator -v

- Add verbosity

    Turn on logging:

    .. code:: bash

        keycollator -l


****

Notes/Todo:
===========

   - Currently refactoring all code
   - Separating project into multiple files
   - Add progress bars when extracting and comparing

Project resource acknowledgements
=================================

    - https://betterscientificsoftware.github.io/python-for-hpc/tutorials/python-pypi-packaging/#creating-a-python-package

    - https://gist.github.com/javiertejero/4585196
