***
[![Pylint](https://github.com/davidprush/keycollator/actions/workflows/pylint.yml/badge.svg)](https://github.com/davidprush/keycollator/actions/workflows/pylint.yml)
[![Makefile CI](https://github.com/davidprush/keycollator/actions/workflows/makefile.yml/badge.svg)](https://github.com/davidprush/keycollator/actions/workflows/makefile.yml)
[![Python Version](https://img.shields.io/pypi/pyversions/keycollator.svg)](https://pypi.org/project/keycollator/)
[![License](https://img.shields.io/github/license/davidprush/keycollator)](https://github.com/davidprush/keycollator/blob/master/LICENSE)

```bash
┬┌─┌─┐┬ ┬┌─┐┌─┐┬  ┬  ┌─┐┌┬┐┌─┐┬─┐
├┴┐├┤ └┬┘│  │ ││  │  ├─┤ │ │ │├┬┘
┴ ┴└─┘ ┴ └─┘└─┘┴─┘┴─┘┴ ┴ ┴ └─┘┴└─
```
***

Compares text in a file to reference/glossary/key-items/dictionary.

🧱 Built by [David Rush](https://github.com/davidprush) fueled by ☕️ ℹ️ [info](#additional-information)

<https://pypi.org/project/keycollator/0.0.3/>

***

## 🗂️ Structure

```bash
.
│
├── assets
│   └── images
│       └── coverage.svg
│
├── docs
│   ├── cli.md
│   └── index.md
│
├── src
│   ├── __init__.py
│   ├── cli.py
│   ├── keycollator.py
│   ├── test_keycollator.py
│   ├── extractonator.py
│   ├── requirements.txt
│   └──data
│       ├── (placeholder)
│       └── (placeholder)
│
├── tests
│   └── test_keycollator
│       ├── __init__.py
│       └── test_keycollator.py
│
├── COD_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── make-venv.sh
├── Makefile
├── pyproject.toml
├── README.README
├── README.rst
├── setup.cfg
└── setup.py
```

## 🚀 Features

- Extract text from file to dictionary
- Extract keys from file to dictionary
- Find matches of keys in text file
- Apply fuzzy matching

## 🧰 Installation

### 🖥️ Install from **Pypi** using pip3

📦 <https://pypi.org/project/keycollator/>

```bash
pip3 install keycollator
```

## 📄 Documentation

Official documentation can be found here:

<https://github.com/davidprush/keycollator/tree/main/docs>

## 💪 Supported File Formats

- TXT/CSV files (Mac/Linux/Win)
- Plans to add PDF and JSON

## 📐 Usage

### 🖥️ Import _keycollator_ it into Python Projects

```
from keycollator import ZTimer, KeyKrawler
```

### 🖥️ CLI

keycollator uses the `CLI` to change default parameters and functions

```bash
python3 src/keycollator.py --help                         
Usage: keycollator.py [OPTIONS] COMMAND [ARGS]...

  keycollator is an app that finds occurances of keys in a text file

Options:
  -t, --text-file PATH            Path/file name of the text to be searched
                                  for against items in the key file
  -k, --key-file PATH             Path/file name of the key file containing a
                                  dictionary, key items, glossary, or
                                  reference list used to search the text file
  -O, --output-file PATH          Path/file name of the output file that
                                  will contain the results (CSV or TXT)
  -R, --limit-results INTEGER     Limit the number of results
  -f, --fuzzy-matching INTEGER RANGE
                                  Set the level of fuzzy matching (default=99)
                                  to validate matches using
                                  approximations/edit distances, uses
                                  acceptance ratios with integer values from 0
                                  to 99, where 99 is nearly identical and 0 is
                                  not similar  [0<=x<=99]
  -U, --ubound-limit INTEGER RANGE
                                  Ignores items from the results with matches
                                  greater than the upper boundary (upper-
                                  limit); reduce eroneous matches
                                  [1<=x<=99999]
  -L, --lbound-limit INTEGER RANGE
                                  Ignores items from the results with matches
                                  less than the lower boundary (lower-limit);
                                  reduce eroneous matches  [0<=x<=99999]
  -v, --set-verbose               Turn on verbose
  -l, --set-logging               Turn on logging
  -Z, --log-file PATH             Path/file name to be used for the log file
  --help                          Show this message and exit.
```

#### 🖥️ Turn on _verbose_ output

  >currently provides only one level for verbose, future versions will implement multiple levels (DEBUG, INFO, WARN, etc.)

```bash
keycollator --verbose
```

#### 🖥️ Apply _fuzzy matching_

  >_fuzzy matching_ uses approximate matches (edit distances) whereby 0 is the least strict and accepts nearly anything as a match and more strictly 99 accepts only nearly identical matches; by default the app uses level 99 only if regular matching finds no matches

```bash
keycollator --fuzzy-matching=[0-99]
```

#### 🖥️ Set the _key file_

  >each line of text represents a key which will be used to match with items in the _text file_

```bash
keycollator --key-file="/path/to/key/file/keys.txt"
```

#### 🖥️ Set the _text file_

  >text file whereby each line represents an item that will be compared with the items in the _keys file_

```bash
keycollator --text-file="/path/to/key/file/text.txt"
```

#### 🖥️ Specify the _output file_

  >currently uses CSV but will add additional file formats in future releases (PDF/JSON/DOCX)

```bash
keycollator --output-file="/path/to/results/result.csv"
```

#### 🖥️ Set _limit results_ for console and _output file_

  >Limit the number of results

```bash
keycollator --limit-results=30
```

#### 🖥️ Set _upper bound limit_

  >rejects items with matches over the integer value set, helps with eroneous matches when using fuzzy matching

```bash
keycollator --ubound-limit
```

#### 🖥️ Turn on _logging_:

  >turn on _logging_ whereby if no _log file_ is supplied by user it will create one using the default _log.log_

```bash
keycollator --set-logging
```

#### 🖥️ Create a _log file_

  >set the name of the _log file_ to be used by _logging_

```bash
keycollator --log-file="/path/to/log/file/log.log"
```

## Example Output

```bash
python3 src/keycollator.py --set-logging --limit-results=30
✔ Extracted text.txt items.[[0.16]seconds]
✔ Extracted keys.txt items.[[0.25]seconds]
✔ Matched keys.txt items to text.txt items.[[76.45]seconds]
✔ results.csv Complete.[[76.52]seconds]
╭─────┬───────────────┬───────╮
│ No. │ Key           │ Count │
├─────┼───────────────┼───────┤
│  1  │ manage        │  73   │
├─────┼───────────────┼───────┤
│  2  │ develop       │  62   │
├─────┼───────────────┼───────┤
│  3  │ report        │  58   │
├─────┼───────────────┼───────┤
│  4  │ support       │  46   │
├─────┼───────────────┼───────┤
│  5  │ process       │  43   │
├─────┼───────────────┼───────┤
│  6  │ analysis      │  36   │
├─────┼───────────────┼───────┤
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
├─────┼───────────────┼───────┤
│ 28  │ dashboards    │  11   │
├─────┼───────────────┼───────┤
│ 29  │ sales         │  10   │
├─────┼───────────────┼───────┤
│ 30  │ create        │  10   │
╰─────┴───────────────┴───────╯
╭─────────────┬────────╮
│ Statistic   │ Total  │
├─────────────┼────────┤
│ Keys        │  701   │
├─────────────┼────────┤
│ Text        │  695   │
├─────────────┼────────┤
│ Matches     │  1207  │
├─────────────┼────────┤
│ Comparisons │ 376855 │
├─────────────┼────────┤
│ Logs        │   0    │
├─────────────┼────────┤
│ Runtime     │ 76.60  │
╰─────────────┴────────╯
 ```

## 🎯 Todo 📌

```bash
    ❌ Update requirements.txt
    ❌ Add proper error handling
    ❌ Add CHANGELOG.md
    ❌ Update requirements.txt
    ❌ Add functions/methods to handle STOP_WORDS
    ❌ Verify python3 -m nltk.downloader punkt is properly immported
    ✅ Separating project into multiple files
    ✅ Add progress inicator using halo when extracting and comparing
    ✅ Create a logger class (for some reason logging is broken)
    ✅ KeyKrawler matching is broken
    ✅ Update README.md(.rst) with correct CLI
    ❌ Create method to KeyKrawler to select and _create missing files_
    ❌ Update CODE_OF_CONDUCT.md
    ❌ Update CONTRIBUTING.md
    ✅ Format KeyCrawler console results as a table
    ❌ Create ZLog class in extractonator.py (parse out __logit method)
    ❌ Cleanup verbose output (conflicts with halo)
    ❌ Update all comments
    ❌ Migrate click functionality to cli.py
    ✅ Refactor all methods and functions
    ❌ Test ALL CLI options
```

## 👔 Project Resource Acknowledgements

  1. [Creating a Python Package](https://betterscientificsoftware.github.io/python-for-hpc/tutorials/python-pypi-packaging/#creating-a-python-package)
  1. [javiertejero](https://gist.github.com/javiertejero/4585196)

## 💼 Deployment Features



## 📈 Releases

  >Currently stage: *_testing_*

## 🛡 License

[![License](https://img.shields.io/github/license/davidprush/keycollator)](https://github.com/davidprush/keycollator/blob/master/LICENSE)

This project is licensed under the terms of the **MIT** license. See [LICENSE](https://github.com/davidprush/keycollator/blob/master/LICENSE) for more details.

```bibtex
@misc{keycollator,
  author = {David Rush},
  title = {Compares text in a file to reference/glossary/key-items/dictionary file.},
  year = {2022},
  publisher = {Rush Solutions, LLC},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/davidprush/keycollator}}
}
```

***

#### Additional Information

1. _The latest version of this document can be found [here](https://github.com/davidprush/keycollator/blob/main/README.md); if you are viewing it there (via HTTPS), you can download the Markdown/reStructuredText source [here](https://github.com/davidprush/keycollator)._ 
2. _You can contact the author via [e-mail](davidprush@gmail.com)._
