# -*- coding: utf-8 -*-
"""
┌─┐─┐ ┬┌┬┐┬─┐┌─┐┌─┐┌┬┐┌─┐┌┐┌┌─┐┌┬┐┌─┐┬─┐
├┤ ┌┴┬┘ │ ├┬┘├─┤│   │ │ ││││├─┤ │ │ │├┬┘
└─┘┴ └─ ┴ ┴└─┴ ┴└─┘ ┴ └─┘┘└┘┴ ┴ ┴ └─┘┴└─

Copyright (C) 2022 Rush Solutions, LLC
Author: David Rush <davidprush@gmail.com>
License: MIT
Contains classes:
    1. ZTimer
        -
    2. KeyKrawler
        -
Notes:
    -
Todo:
    *
"""
import sys
import time
import os.path
import string
from halo import Halo
from time import sleep
from fuzzywuzzy import fuzz
from collections import defaultdict
from nltk.stem import PorterStemmer

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
RHDR = "=========================="
RTXT = "         Results          "
RFTR = "~~~~~~~~~~~~~~~~~~~~~~~~~~"
DIV = "--------------------------"
STATS = "Stats for this run... \n \
    Total Dictionary Items: {0} \n \
    Total Text File Items: {1} \n \
    Total Keys Added to List: {2} \n \
    Total Comparisons: {3} \n \
    Total Items Logged: {4} \n \
    Total Runtime: {5} seconds\n\n"
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
        """Constructs and starts the ZTimer object.
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
        stime = str(f"{self.__tspan:0.2f}")
        stime = stime.rstrip(" ")
        self.__fspan = stime
        self.__caller = str(self.__caller)

    def __cupdate(self, c):
        if not self.__sflag:
            if c:
                c = str(c)
            if c != self.__caller:
                self.__end_caller = c

    def __tupdate(self):
        if not self.__sflag:
            self.__toc = time.perf_counter()
            self.__tspan = self.__toc - self.__tic

    def __ftstr(self):
        self.__t2s()
        self.__fstr = "Caller[{0}] \
            Span[{1}]seconds".format(
            self.__caller, self.__fspan
        )
        self.__fstr = self.__fstr.rstrip(" ")
        return self.__fstr

    def stopit(self, caller="stopit"):
        if not self.__sflag:
            self.__cupdate(caller)
            self.__tupdate()
            self.__t2s()
            self.__sflag = True

    def echo(self):
        if not self.__sflag:
            self.__tupdate
        print(self.__ftstr())

    def get_start(self):
        return self.__tic

    def get_stop(self):
        return self.__toc

    def get_span(self, as_str=False):
        self.__tupdate()
        if as_str:
            return self.__fspan
        else:
            return self.__tspan

    def get_string(self):
        self.__tupdate()
        return self.__ftstr()


class KeyKrawler:
    def __init__(
        self,
        text_file=TXTS,
        key_file=KEYZ,
        result_file=REZF,
        log_file=LOGZ,
        verbosity=False,
        ubound=99999,
        lbound=0,
        fuzzyness=99,
        set_logging=False
    ):
        """Constructs the KeyCrawler object.
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
            identical matches. (default: 0)
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
        self.__ulim = ubound
        self.__llim = lbound
        self.__fuzz = fuzzyness
        self.__verb = verbosity
        self.__tcount = 0
        self.__kcount = 0
        self.__ccount = 0
        self.__fcount = 0
        self.__lcount = 0
        self.__mcount = 0
        self.__nomatch = True
        self.__ps = PorterStemmer()
        self.reset_log()
        self.itemize_text()
        self.itemize_keys()
        self.match_txt2keys()
        self.results2file()
        self.echo_results()
        self.echo_stats()
        self.timer.stopit(sys._getframe().f_code.co_name)

    def __sanitext(self, text):
        """Remove special chars, spaces, end line and
        convert to lowercase
        Parameters
        ----------
        text: str
        """
        text = text.translate(text.maketrans(
            "",
            "",
            string.punctuation
        ))
        text = text.lower()
        text = text.rstrip(ENDL)
        return text

    def __logit(self, *args):
        if self.set_logging:
            self.__lcount += 1
            logging.basicConfig(
                filename=LOGZ,
                filemode='a',
                format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                datefmt='%H:%M:%S',
                level=logging.DEBUG
            )
            log_string = ""
            for arg in args:
                log_string += "[{0}]".format(str(arg))
            log_string = log_string.rstrip(" ")
            logging.info(log_string)
            return str(log_string)

    def echo_results(self):
        if not self.__nomatch:
            print_item = 0
            print(RHDR)
            print(RTXT)
            for key in self.__keyd:
                if self.__keyd[key] > self.__llim \
                        and self.key_freq[key] < self.__ulim:
                    print_item += 1
                    print(
                        print_item, key, ",",
                        self.__keyd[key])
                    self.__logit(
                        self.timer.get_string(),
                        print_item, key, ",",
                        self.__keyd[key]
                    )
            print(RFTR)
        else:
            print(NOMATCH)
            self.__logit(
                self.timer.get_string(),
                NOMATCH
            )

    def echo_stats(self):
        print(DIV)
        print(RFTR)
        print(STATS.format(
            self.__kcount,
            self.__tcount,
            self.__mcount,
            self.__ccount,
            self.__lcount,
            self.timer.get_span(True)
        ))

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
                    self.__kcount,
                    ADDED, key
                )
                if self.__verb:
                    print(
                        self.timer.get_string(),
                        info
                    )
        fhkey.close()
        spinner.stop_and_persist('✔')

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
                self.__tcount,
                ADDED, text
            )
            if self.__verb:
                print(info)
            sleep(.02)
        fhtxt.close()
        spinner.stop_and_persist('✔')

    def match_txt2keys(self):
        self.__ccount = 0
        self.__mcount = 0
        tempd = defaultdict(int)
        spinner = Halo(
            text="Match {} items to {} items".format(
                self.key_file,
                self.text_file),
            spinner='dots'
        )
        spinner.start()
        for key in self.__keyd:
            for item in self.__txtd:
                spinner.text = "Caompare {} to {} items".format(
                    key, item)
                self.__ccount += 1
                info = self.__logit(
                    self.__ccount,
                    SEPR, key, SEPR,
                    self.__ccount,
                    ADDED, item
                )
                if self.__verb:
                    print(
                        self.timer.get_string(),
                        info
                    )
                # Check for near-perfect match
                if self.__ps.stem(key) in self.__ps.stem(item):
                    tempd[key] += 1
                    self.__mcount += 1
                    info = self.__logit(
                        self.__ccount,
                        SEPR, self.__mcount,
                        SEPR, key, ADDED,
                        self.__txtd[item],
                        item
                    )
                    if self.__verb:
                        print(
                            self.timer.get_string(),
                            info
                        )
                # Only perform fuzzy matching if imperfect match
                elif fuzz.partial_ratio(key, item) >= self.__fuzz:
                    tempd[key] += 1
                    self.__mcount += 1
                    info = self.__logit(
                        FUZZ.format(self.__fuzz),
                        SEPR, key, SEPR, ADDED,
                        self.__txtd[item], item
                    )
                    if self.__verb:
                        print(
                            self.timer.get_string(),
                            info
                        )
            sleep(.000001)
        self.__nomatch = False
        self.__rezd = tempd.copy()
        spinner.stop_and_persist(
            '✔',
            "Match {} items to {} items".format(
                self.key_file,
                self.text_file)
        )

    def reset_log(self):
        results_file = open(self.log_file, 'w')
        results_file.close()

    def results2file(self):
        if not self.__nomatch:
            rf = open(self.result_file, 'w')
            write_count = 0
            spinner = Halo(
                text="Writing results to {}".format(
                    self.result_file),
                spinner='dots'
            )
            spinner.start()
            for key in self.__keyd:
                if self.__keyd[key] > self.__llim \
                        and self.key_freq[key] < self.__ulim:
                    write_count += 1
                    rf.write(
                        write_count,
                        ". ", key, ",",
                        self.__rezd[key]
                    )
                    info = self.__logit(
                        write_count,
                        SEPR, key, SEPR,
                        self.__keyd[key]
                    )
                    if self.__verb:
                        print(
                            self.timer.get_string(),
                            info
                        )
                    sleep(.02)
            rf.close()
            self.__mcount = write_count
            spinner.stop_and_persist('✔')
        else:
            return False

    def verify_filez(self, *args):
        for arg in args:
            if not os.path.exists(arg):
                self.__valid_files = False
            else:
                self.__valid_files = True
