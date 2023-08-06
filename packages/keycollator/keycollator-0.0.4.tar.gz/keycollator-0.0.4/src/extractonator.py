# -*- coding: utf-8 -*-
"""
┌─┐─┐ ┬┌┬┐┬─┐┌─┐┌─┐┌┬┐┌─┐┌┐┌┌─┐┌┬┐┌─┐┬─┐
├┤ ┌┴┬┘ │ ├┬┘├─┤│   │ │ ││││├─┤ │ │ │├┬┘
└─┘┴ └─ ┴ ┴└─┴ ┴└─┘ ┴ └─┘┘└┘┴ ┴ ┴ └─┘┴└─

Copyright (C) 2022 Rush Solutions, LLC
Author: David Rush <davidprush@gmail.com>
License: MIT
Contains classes:
    1. ZLog
        └──usage:

    2. ZTimer
        └──usage:

    3. KeyKrawler
        └──usage:

Notes:
    -
Todo:
    ❌ Update requirements.txt
    ❌ Add CHANGELOG.md
    ❌ Update requirements.txt
    ❌ Add functions/methods to handle STOP_WORDS
    ❌ Verify python3 -m nltk.downloader punkt is properly immported
    ✅ Separating project into multiple files
    ✅ Add progress inicator using halo when extracting and comparing
    ✅Create a logger class (for some reason **logging** is broken)
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
"""
import sys
import time
import os.path
import string
import termtables as tt
from datetime import datetime
from halo import Halo
from fuzzywuzzy import fuzz
from collections import defaultdict
import nltk.data
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
# Requires:
#           python3 -m nltk.downloader punkt
#

# Default file names
LOGZ = "log.log"
TXTS = "text.txt"
REZF = "results.csv"
KEYZ = "keys.txt"

# Formatter constants
ENDL = "\n"
ADDED = ">>>"
SEPR = "::"
COMP = "<<<[]>>>"
FUZZ = "Fuzzy={0}"
NOMATCH = "*****[ NO MATCHES! ]******"
_MAIN = {
    'info': 'ℹ',
    'success': '✔',
    'warning': '⚠',
    'error': '✖'
}
_FALLBACKS = {
    'info': '¡',
    'success': 'v',
    'warning': '!!',
    'error': '×'
}
STOP_WORDS = [
    "a", "about", "above", "after", "again", "against", "all", "am",
    "an", "and", "any", "are", "as", "at", "be", "because", "been",
    "before", "being", "below", "between", "both", "but", "by", "can",
    "did", "do", "does", "doing", "don", "down", "during", "each",
    "few", "for", "from", "further", "had", "has", "have", "having",
    "he", "her", "here", "hers", "herself", "him", "himself", "his",
    "how", "i", "if", "in", "into", "is", "it", "its", "itself",
    "just", "me", "more", "most", "my", "myself", "no", "nor", "not",
    "now", "of", "off", "on", "once", "only", "or", "other", "our",
    "ours", "ourselves", "out", "over", "own", "s", "same", "she",
    "should", "so", "some", "such", "t", "than", "that", "the",
    "their", "theirs", "them", "themselves", "then", "there",
    "these", "they", "this", "those", "through", "to", "too",
    "under", "until", "up", "very", "was", "we", "were", "what",
    "when", "where", "which", "while", "who", "whom", "why",
    "will", "with", "you", "your", "yours", "yourself", "yourselves",
    "find", "help", "make", "take", "with", "work", "update", "post"
]


class ZLog:
    def __init__(
        self,
        name,
        filename
    ):
        pass


class ZTimer:
    def __init__(
        self,
        caller="ZTimer"
    ):
        """
        Constructs and starts the ZTimer object.
        Parameters
        ----------
        caller : str, optional
            name of process where instance is created
        """
        self.__tic = time.perf_counter()
        self.__caller = str(caller)
        self.__end_caller = caller
        self.__toc = self.__tic
        self.__tspan = time.perf_counter()
        self.__fspan = str(self.__tspan)
        self.__tstr = ""
        self.__sflag = False

    def __t2s(self):
        """
        Formats/strips __fspanas str with
        2 decimals and ensures caller is str
        """
        stime = str(f"{self.__tspan:0.2f}")
        self.__fspan = stime
        self.__caller = str(self.__caller)

    def __cupdate(self, c):
        """
        Updates __caller with new caller
        """
        if not self.__sflag:
            if c:
                c = str(c)
            if c != self.__caller:
                self.__end_caller = c

    def __tupdate(self):
        """        Updates __toc and calculates __span
        Condition
        ----------
        __sflag must be False
        """
        if not self.__sflag:
            self.__toc = time.perf_counter()
            self.__tspan = self.__toc - self.__tic
        self.__t2s()

    def __ftstr(self):
        """
        Creates a formatted str for console output.
        """
        self.__t2s()
        self.__fstr = "[{0}]seconds".format(
            self.__fspan
        )
        return self.__fstr

    def stopit(self, caller="stopit"):
        """
        Updates __toc and calculates __span
        Arguement
        ----------
        caller: str, optional
            can be anything to assign text to
            to the formatted str __sflag to give
            context to the timestamp
        """
        if not self.__sflag:
            self.__cupdate(caller)
            self.__tupdate()
            self.__t2s()
            self.__sflag = True

    def echo(self):
        """
        Updates __toc and calculates __span
        Condition
        ----------
        __sflag must be False
        """
        if not self.__sflag:
            self.__tupdate
        self.__t2s()
        print(self.__ftstr())

    def get_start(self):
        """
        Returns __tic which is the time the
            timer started
        """
        return self.__tic

    def get_stop(self):
        """
        Returns __toc which is the time the
            timer stopped
        """
        return self.__toc

    def timestamp(self, as_str=False):
        """
        Updates the timer and returns time
        as str or unformatted time str
        Arguement
        ----------
        as_str: bool, optional
        """
        self.__tupdate()
        if as_str:
            return str(self.__fspan)
        else:
            return self.__tspan

    def get_string(self):
        """
        Updates timer and returns formatted
        time in a string
        Arguement
        ----------
        as_str: bool, optional
            Updates the timer and returns time
            as str or unformatted time str
        """
        self.__tupdate()
        return self.__ftstr()


class KeyKrawler:
    def __init__(
        self,
        text_file=TXTS,
        key_file=KEYZ,
        result_file=REZF,
        limit_results=0,
        log_file=LOGZ,
        verbosity=False,
        ubound=99999,
        lbound=0,
        fuzzyness=99,
        set_logging=False
    ):
        """
        Constructs the KeyCrawler object.
        Parameters
        ----------
        text_file: str, optional
            Name of the text file to find keys.
            (default: TXTS)
        key_file: str, optional
            Name of file to read keys.
            (default: KEYZ)
        result_file str, optional
            Name of the file to write results.
            (default: REZF)
        limit_results: int, optional
            Sets the limit to the number (integer)
            of results where 0 is no limit and
            any number equal or above 1 implements
            a limit (default: 0)
        log_file: str, optional
            Name of the file to write logs
            (default: LOGZ)
        verbosity: bool, optional
            Verbosity flag where False is off
            and True is on. (default: False)
        ubound: int, optional
            Upper bound limit to reject key
            matches above the value.
            Helps eliminate eroneous results
            when using fuzzy matching.
            (default: 99999)
        lbound: int, optional
            Lower bound limit to reject key
            matches below the value.
            Helps eliminate eroneous results
            when using fuzzy matching. (default: 0)
        fuzzyness: int, optional
            Sets the level of fuzzy matching,
            range(0:99), where 0 accepts nearly
            everythong and 99 accepts nearly
            identical matches. (default: 99)
        set_logging: bool, optional
            Logging flag where False is off
            and True is on. (default: 0)
        """
        self.timer = ZTimer(sys._getframe().f_code.co_name)
        self.text_file = text_file
        self.key_file = key_file
        self.result_file = result_file
        self.log_file = log_file
        self.set_logging = set_logging
        self.__valid_files = False
        self.__keyd = defaultdict(int)
        self.__txtd = defaultdict(int)
        self.__rezd = defaultdict(int)
        self.__limr = limit_results
        self.__ulim = ubound
        self.__llim = lbound
        self.__fuzz = fuzzyness
        self.__v = verbosity
        self.__tcount = 0
        self.__kcount = 0
        self.__ccount = 0
        self.__fcount = 0
        self.__lcount = 0
        self.__mcount = 0
        self.__nomatch = True
        self.__ps = PorterStemmer()
        self.__sent_detector = nltk.data.load(
            'tokenizers/punkt/english.pickle')
        self.reset_log()
        self.itemize_text()
        self.itemize_keys()
        self.match_txt2keys()
        self.results2file()
        self.echo_results()
        self.echo_stats()
        self.timer.stopit(sys._getframe().f_code.co_name)

    def __sanitext(self, text):
        """
        Remove special chars, spaces, end line and
        convert to lowercase
        Parameters
        ----------
            text: str, required
        """
        if not isinstance(text, str):
            text = str(text)
        text = text.translate(text.maketrans(
            "",
            "",
            string.punctuation
        ))
        text = text.lower()
        text = text.rstrip(ENDL)
        return text

    def __logit(self, *args, **kwargs):
        """
        Takes args and creates a log str
        for output to the log file
        Condition
        ----------
        set_logging must be true, otherwise
            test for param to update set_logging
            to True
        arguements
        ----------
        *args:
            all args are converted to strings and
            appended to text str
        Parameters
        ----------
        **kwargs:
            text: str, optional
            setlog: bool, optional
            filemode: str, optional
            level: str, optional
            logfile: str, optional
            dtformat: str, optional
        """
        if self.set_logging:
            onerr = False
            params = defaultdict(str)
            params = {
                'filename': "",
                'filemode': "",
                'setlog': "",
                'level': "",
                'logfile': "",
                'dtformat': [],
            }
            modes = ['a', 'r', 'w']
            dttemplate = [
                '%d', '%m', '%Y',
                '%H', '%M', '%S',
                ' ', ':', '/'
            ]
            dtdefault = [
                '%d', '/', '%m',
                '/', '%Y', ' ',
                '%H', ':', '%M',
                ':', '%S'
            ]
            params['text'] = kwargs.get('text', "")
            self.set_logging = kwargs.get(
                'setlog',
                self.set_logging
            )
            dtemp = []
            errs = defaultdict(str)
            params['filemode'] = str(kwargs.get('filemode', 'a'))
            if params['filemode'] not in modes:
                errs['filemode'] = params['filemode']
                onerr = True
            params['level'] = str(kwargs.get('level', 'DEFAULT'))
            params['logfile'] = str(kwargs.get('logfile', LOGZ))
            params['dtformat'] = kwargs.get(
                'dtformat', dtdefault)
            for d in dttemplate:
                if d in params['dtformat']:
                    dtemp.append(str(d))
            dtdiff = [x for x in params['dtformat'] if x not in dtemp]
            if len(dtdiff) > 1:
                dtdiff = [str(li) for li in dtdiff]
                errs['dtformat'] = "WARNING: dtformat invalid options: [" \
                    + "], [".join(dtdiff) + "]"
                onerr = True
            dtstamp = datetime.now()
            dtstamp = dtstamp.strftime(str(params['dtformat']))
            for arg in args:
                params['text'] += "[{0}]".format(str(arg))
            if onerr:
                errmsg = "INVALID OPTIONS:" + str(self.__lcount) + str(dtstamp)
                for err in errs:
                    errmsg += err
                    errmsg += str(errs[err])
                print(errmsg)
                return errmsg
            else:
                logmsg = str(self.__lcount) + str(dtstamp)
                for p in params:
                    logmsg += " [{}]".format(params[p])
                logmsg += ENDL
                if self.__v:
                    lfh = open(
                        params['logfile'], params['filemode'])
                    self.__lcount += 1
                    lfh.write(logmsg)
                return logmsg

    def trunc_results(self):
        if self.__limr >= 1:
            trez = defaultdict(int)
            r = 0
            for rez in self.__rezd:
                trez[rez] = self.__rezd[rez]
                r += 1
                if r >= self.__limr:
                    break
            if r >= 1:
                self.__rezd = trez.copy()
                return True
            else:
                return False

    def echo_results(self):
        n = 0
        tblhdr = ["No.", "Key", "Count"]
        tbldat = []
        for i in self.__rezd:
            if self.__rezd[i] > self.__llim \
                    and self.__rezd[i] < self.__ulim:
                n += 1
                if len(i) > 25:
                    istr = i[0:25]
                else:
                    istr = i
                tbldat.append([
                    n,
                    istr,
                    self.__rezd[i]
                ])
                self.__logit(
                    n, i, self.__rezd[i]
                )
        tt.print(
            tbldat,
            header=tblhdr,
            style=tt.styles.rounded,
            padding=(0, 1),
            alignment="clc"
        )

    def echo_stats(self):
        tblhdr = [
            "Statistic", "Total"
        ]
        stats = [
            ["Keys", self.__kcount],
            ["Text", self.__tcount],
            ["Matches", self.__mcount],
            ["Comparisons", self.__ccount],
            ["Logs", self.__lcount],
            ["Runtime", self.timer.timestamp(True)]
        ]
        tt.print(
            stats,
            header=tblhdr,
            style=tt.styles.rounded,
            padding=(0, 1),
            alignment="lc"
        )

    def itemize_keys(self):
        fhkey = open(self.key_file, 'r')
        self.__kcount = 0
        spinner = Halo(
            text="Extract data from {}".format(self.key_file),
            spinner='dots'
        )
        spinner.start()
        for key in fhkey:
            key = self.__sanitext(key)
            if self.__ps.stem(key) not in self.__keyd:
                self.__keyd[key] = 0
                self.__kcount += 1
                info = self.__logit(
                    self.__kcount, key
                )
                if self.__v:
                    print(
                        self.timer.get_string(),
                        info
                    )
        fhkey.close()
        spinner.stop_and_persist(
            '✔',
            "Extracted {} items.[{}]".format(
                self.key_file,
                self.timer.get_string()
            )
        )

    def itemize_text(self):
        fhtxt = open(self.text_file, 'r')
        self.__tcount = 0
        spinner = Halo(
            text="Extract data from {}".format(self.text_file),
            spinner='dots'
        )
        spinner.start()
        for text in fhtxt:
            text = self.__sanitext(text)
            self.__txtd[text] = 0
            self.__tcount += 1
            info = self.__logit(
                self.__tcount, text
            )
            if self.__v:
                print(info)
        fhtxt.close()
        spinner.stop_and_persist(
            '✔',
            "Extracted {} items.[{}]".format(
                self.text_file,
                self.timer.get_string()
            )
        )

    def match_txt2keys(self):
        spinner = Halo(
            text="Match {} items to {} items".format(
                self.key_file,
                self.text_file),
            spinner='dots'
        )
        spinner.start()
        for key in self.__keyd:
            if key in STOP_WORDS or len(key) <= 3:
                continue
            for item in self.__txtd:
                if item in STOP_WORDS or len(key) <= 3:
                    continue
                spinner.text = "Compare {} to {} items".format(
                    key, item)
                self.__ccount += 1
                info = self.__logit(
                    self.__ccount, key, self.__ccount, item
                )
                if self.__v:
                    print(
                        self.timer.get_string(),
                        info
                    )
                if key in item:
                    self.__rezd[key] += 1
                    self.__mcount += 1
                    info = self.__logit(
                        self.__ccount, self.__mcount,
                        key, self.__txtd[item], item
                    )
                    if self.__v:
                        print(
                            self.timer.get_string(),
                            info
                        )
                else:
                    kwords = word_tokenize(key)
                    tk = kwords
                    # Reomove stop words from kwords
                    for w in tk:
                        if w in STOP_WORDS or len(key) <= 3:
                            kwords.remove(w)
                            continue
                    # Convert to strings
                    kstr = str(kwords)
                    iwords = word_tokenize(item)
                    tk = iwords
                    # Reomove stop words from kwords
                    for w in tk:
                        if w in STOP_WORDS or len(key) <= 3:
                            iwords.remove(w)
                            continue
                    istr = str(iwords)
                    if kstr in istr:
                        self.__rezd[key] += 1
                        self.__mcount += 1
                        info = self.__logit(
                            self.__ccount, self.__mcount,
                            key, self.__txtd[item], item
                        )
                        if self.__v:
                            print(
                                self.timer.get_string(),
                                info
                            )
                    elif fuzz.partial_ratio(key, item) >= self.__fuzz:
                        self.__rezd[key] += 1
                        self.__mcount += 1
                        info = self.__logit(
                            FUZZ.format(self.__fuzz), key,
                            self.__txtd[item], item
                        )
                        if self.__v:
                            print(
                                self.timer.get_string(),
                                info
                            )
        self.__rezd = dict(sorted(
            self.__rezd.items(),
            key=lambda item: item[1], reverse=True))
        self.trunc_results()
        spinner.stop_and_persist(
            '✔',
            "Matched {} items to {} items.[{}]".format(
                self.key_file,
                self.text_file,
                self.timer.get_string()
            )
        )

    def reset_log(self):
        results_file = open(self.log_file, 'w')
        results_file.close()

    def results2file(self):
        rf = open(self.result_file, 'w')
        write_count = 0
        spinner = Halo(
            text="Writing results to {}".format(
                self.result_file),
            spinner='dots'
        )
        spinner.start()
        for i in self.__rezd:
            if self.__rezd[i] > self.__llim \
                    and self.__rezd[i] < self.__ulim:
                write_count += 1
                ritem = str(i) + "," + str(self.__rezd[i])
                rf.write(ritem)
                rf.write(ENDL)
                info = self.__logit(
                    write_count, i, self.__rezd[i]
                )
                if self.__v:
                    print(
                        self.timer.get_string(),
                        info
                    )
        rf.close()
        spinner.stop_and_persist(
            '✔',
            "{} Complete.[{}]".format(
                self.result_file,
                self.timer.get_string()
            )
        )

    def verify_filez(self, *args):
        for arg in args:
            if not os.path.exists(arg):
                self.__valid_files = False
            else:
                self.__valid_files = True
