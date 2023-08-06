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

    usage: keycollator.py [-h] [-c CSV_FILE] [-d DICTIONARY_FILE] [-f COUNT] 
                          [-i IN_FILE] [-l] [-o OUT_FILE] [-v] [--version]

      App takes two files, a dictionary file and a and a text file, and counts 
      how many times each line in the dictionary file appears in the text file.
      The app can output the results to the console and/or csv/text file. 
      Matching will use fuzzy matching to get desired results.

    optional arguments:
      -h, --help            show this help message and exit
      -c CSV_FILE, --csv-file CSV_FILE
                            Change the csv output file name (defautl is results.csv)
      -d DICTIONARY_FILE, --dictionary-file DICTIONARY_FILE
                            Change the dictionary file name (default is dictionary.txt)
      -f COUNT, --fuzzy COUNT
                            Select a value for fuzzyness 1-99, 1 for decresed accuracy, 99 for increased
                            accuracy, default is set to 95
      -i IN_FILE, --in-file IN_FILE
                            Change the input file name (default is text.txt)
      -l, --logging         Set flag to True for logging.
      -o OUT_FILE, --out-file OUT_FILE
                            Change the output file name (default is results.txt)
      -v, --verbose         Verbosity (-v, -vv, etc)
      --version             show version number and exit


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
