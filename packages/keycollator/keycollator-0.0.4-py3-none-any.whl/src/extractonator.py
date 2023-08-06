# -*- coding: utf-8 -*-
"""
┌─┐─┐ ┬┌┬┐┬─┐┌─┐┌─┐┌┬┐┌─┐┌┐┌┌─┐┌┬┐┌─┐┬─┐
├┤ ┌┴┬┘ │ ├┬┘├─┤│   │ │ ││││├─┤ │ │ │├┬┘
└─┘┴ └─ ┴ ┴└─┴ ┴└─┘ ┴ └─┘┘└┘┴ ┴ ┴ └─┘┴└─

Copyright (C) 2022 Rush Solutions, LLC
Author: David Rush <davidprush@gmail.com>
License: MIT
Contains class:
    KeyKrawler
        └──usage:

Notes:
    -
Todo:
    ✖ Fix pylint errors
    ✖ Add proper error handling
    ✖ Add CHANGELOG.md
    ✖ Create method to KeyKrawler to select and _create missing files_
    ✖ Update CODE_OF_CONDUCT.md
    ✖ Update CONTRIBUTING.md
    ✖ Update all comments
    ✖ Migrate click functionality to cli.py
    ✖ Test ALL CLI options
    ✖ Github: issue and pr templates
    ✖ Workflow Automation
    ✖ Makefile Usage
    ✖ Dockerfile
    ✖ @dependabot configuration
    ✖ Release Drafter (release-drafter.yml)
"""
import os.path
import string
import termtables as tt

from halo import Halo
from fuzzywuzzy import fuzz
from collections import defaultdict

import nltk.data
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

from consts import *
from proceduretimer import ProcedureTimer
from customlogger import CustomLogger

import nltk.downloader
# Requires:
# CLI command: python3 -m nltk.downloader punkt
try:
    dler = nltk.downloader.Downloader()
    if dler._status_cache['punkt'] != 'installed':
        dler._update_index()
        dler.download('punkt')
except Exception as ex:
    print(ex)  # replace with CustomLogger


class KeyKrawler:
    def __init__(
        self,
        text_file=DEFAULT_TEXT_FILE,
        key_file=DEFAULT_KEY_FILE,
        csv_file=DEFAULT_CSV_FILE,
        limit_result=0,
        log_file=DEFAULT_LOG_FILE,
        verbose=False,
        ubound_limit=99999,
        lbound_limit=0,
        fuzzy_match_ratio=99,
        logging=False,
        run_now=False
    ):
        """
        Constructs the KeyCrawler object.
        Parameters
        ----------
        text_file: str, optional
            Name of the text file to find keys. (default: DEFAULT_TEXT_FILE)
        key_file: str, optional
            Name of file to read keys. (default: DEFAULT_KEY_FILE)
        csv_file str, optional
            Name of the file to write results. (default: DEFAULT_CSV_FILE)
        limit_result: int, optional
            Sets the limit to the number (integer) of results
            where 0 is no limit and any number equal or above
            1 implements a limit (default: 0)
        log_file: str, optional
            Name of the file to write logs (default: DEFAULT_LOG_FILE)
        verbose: bool, optional
            Verbosity flag where False is off and True is on. (default: False)
        ubound_limit: int, optional
            Upper bound limit to reject key matches above the value.
            Helps eliminate eroneous results when using fuzzy matching.
            (default: 99999)
        lbound_limit: int, optional
            Lower bound limit to reject key matches below the value.
            Helps eliminate eroneous results when using fuzzy matching. (default: 0)
        fuzzy_match_ratio: int, optional
            Sets the level of fuzzy matching, range(0:99), where 0 accepts
            nearly everythong and 99 accepts nearly identical matches. (default: 99)
        logging: bool, optional
            Logging flag where False is off and True is on. (default: 0)
        """
        self.timer = ProcedureTimer(KeyKrawler)
        self.text_file = text_file
        self.key_file = key_file
        self.csv_file = csv_file
        self.log_file = log_file
        self.__valid_files = False
        self.__key_dictionary = defaultdict(int)
        self.__text_dictionary = defaultdict(int)
        self.__result_dictionary = defaultdict(int)
        self.__limit_result = limit_result
        self.__upper_limit_result_item = ubound_limit
        self.__lower_limit_result_item = lbound_limit
        self.__set_fuzzy_matching = fuzzy_match_ratio
        self.__set_verbose = verbose
        self.__text_item_count = 0
        self.__key_item_count = 0
        self.__comparison_count = 0
        self.__log_item_count = 0
        self.__result_item_count = 0
        self.__no_result = True
        self.__ps = PorterStemmer()
        if logging:
            self.logging = logging
            self.__logger = CustomLogger(phony=False)
        else:
            self.logging = False
            self.__logger = CustomLogger(phony=True)
        self.__sent_detector = nltk.data.load(
            'tokenizers/punkt/english.pickle')
        if run_now:
            self.run()
        self.timer.stop_timer(KeyKrawler)

    def __sanitize_text(self, text):
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
        text = text.rstrip(END_LINE)
        return text

    def __verbose(self, *args):
        if self.logging:
            self.__logger.write_log(
                result_item_count, item, self.__result_dictionary[item]
            )

    def truncate_result(self):
        if self.__limit_result >= 1:
            truncated_result = defaultdict(int)
            truncated_result_count = 0
            for item in self.__result_dictionary:
                truncated_result[item] = self.__result_dictionary[item]
                truncated_result_count += 1
                if truncated_result_count >= self.__limit_result:
                    break
            if truncated_result_count >= 1:
                self.__result_dictionary = truncated_result.copy()
                return True
            else:
                return False

    def echo_result(self):
        result_item_count = 0
        table_header = ["No.", "Key", "Count"]
        table_data = []
        self.truncate_result()
        self.purge_limited_items()
        for item in self.__result_dictionary:
            result_item_count += 1
            if len(item) > 20:
                char_count = 0
                for char in item:
                    char_count += 1
                    if (char_count % 20) == 0:
                        formatted_item += (char + END_LINE)
                    else:
                        formatted_item += char
            else:
                formatted_item = item
            table_data.append([
                result_item_count,
                formatted_item,
                self.__result_dictionary[item]
            ])
        tt.print(
            table_data,
            header=table_header,
            style=tt.styles.rounded,
            padding=(0, 0),
            alignment="clc"
        )

    def purge_limited_items(self):
        result_count = 0
        purged_item_count = 0
        purged_result = defaultdict(int)
        for item in self.__result_dictionary:
            result_count += 1
            if (self.__result_dictionary[item] > self.__lower_limit_result_item) \
                    and (self.__result_dictionary[item] < self.__upper_limit_result_item):
                purged_item_count += 1
                purged_result[item] = self.__result_dictionary[item]
        if result_count > purged_item_count:
            self.__result_dictionary = purged_result.copy()
            self.__result_item_count = purged_item_count
            return True
        else:
            return False

    def echo_stats(self):
        table_header = [
            "Statistic", "Total"
        ]
        stats = [
            ["Keys", self.__key_item_count],
            ["Text", self.__text_item_count],
            ["Matches", self.__result_item_count],
            ["Comparisons", self.__comparison_count],
            ["Logs", self.__logger.log_count()],
            ["Runtime", self.timer.timestamp(True)]
        ]
        tt.print(
            stats,
            header=table_header,
            style=tt.styles.rounded,
            padding=(0, 1),
            alignment="lc"
        )

    def itemize_keys(self):
        with open(self.key_file, 'r') as key_file_handler:
            self.__key_item_count = 0
            spinner = Halo(
                text="Extract data from {}".format(self.key_file),
                spinner='dots'
            )
            spinner.start()
            for key in key_file_handler:
                key = self.__sanitize_text(key)
                if key not in self.__key_dictionary:
                    self.__key_dictionary[key] = 0
                    self.__key_item_count += 1
                    info = self.__logger.write_log(
                        self.__key_item_count, key
                    )
                    if self.__set_verbose:
                        print(
                            self.timer.timestampstr(),
                            info
                        )
            key_file_handler.close()
        spinner.stop_and_persist(
            SYMBOLS['success'],
            "Extracted {} items.[{}]".format(
                self.key_file,
                self.timer.timestampstr()
            )
        )

    def itemize_text(self):
        with open(self.text_file, 'r') as text_file_handler:
            self.__text_item_count = 0
            spinner = Halo(
                text="Extract data from {}".format(self.text_file),
                spinner='dots'
            )
            spinner.start()
            for text in text_file_handler:
                text = self.__sanitize_text(text)
                self.__text_dictionary[text] = 0
                self.__text_item_count += 1
                info = self.__logger.write_log(
                    self.__text_item_count, text
                )
                if self.__set_verbose:
                    print(info)
            text_file_handler.close()
        spinner.stop_and_persist(
            SYMBOLS['success'],
            "Extracted {} items.[{}]".format(
                self.text_file,
                self.timer.timestampstr()
            )
        )

    def match_text2keys(self):
        spinner = Halo(
            text="Match {} items to {} items".format(
                self.key_file,
                self.text_file),
            spinner='dots'
        )
        spinner.start()
        for key in self.__key_dictionary:
            if key in STOP_WORDS:
                continue
            for item in self.__text_dictionary:
                if item in STOP_WORDS:
                    continue
                spinner.text = "Compare {} to {} items".format(
                    key, item)
                self.__comparison_count += 1
                info = self.__logger.write_log(
                    self.__comparison_count, key, self.__comparison_count, item
                )
                if self.__set_verbose:
                    print(
                        self.timer.timestampstr(),
                        info
                    )
                if key in item:
                    self.__result_dictionary[key] += 1
                    self.__result_item_count += 1
                    info = self.__logger.write_log(
                        self.__comparison_count, self.__result_item_count,
                        key, self.__text_dictionary[item], item
                    )
                    if self.__set_verbose:
                        print(
                            self.timer.timestampstr(),
                            info
                        )
                else:
                    key_tokenized = word_tokenize(key)
                    key_tokenized_copy = key_tokenized
                    # Reomove stop words from key_tokenized
                    for keyt in key_tokenized_copy:
                        if keyt in STOP_WORDS:
                            key_tokenized.remove(keyt)
                            continue
                    # Convert to strings
                    key_string = str(key_tokenized)
                    item_tokenized = word_tokenize(item)
                    item_tokenized_copy = item_tokenized
                    # Reomove stop words from key_tokenized
                    for itemt in item_tokenized_copy:
                        if itemt in STOP_WORDS:
                            item_tokenized.remove(itemt)
                            continue
                    item_string = str(item_tokenized)
                    if key_string in item_string:
                        self.__result_dictionary[key] += 1
                        self.__result_item_count += 1
                        info = self.__logger.write_log(
                            self.__comparison_count, self.__result_item_count,
                            key, self.__text_dictionary[item], item
                        )
                        if self.__set_verbose:
                            print(
                                self.timer.timestampstr(),
                                info
                            )
                    elif fuzz.partial_ratio(key, item) >= self.__set_fuzzy_matching:
                        self.__result_dictionary[key] += 1
                        self.__result_item_count += 1
                        info = self.__logger.write_log(
                            "fuzzy={0}".format(self.__set_fuzzy_matching), key,
                            self.__text_dictionary[item], item
                        )
                        if self.__set_verbose:
                            print(
                                self.timer.timestampstr(),
                                info
                            )
        self.__result_dictionary = dict(sorted(
            self.__result_dictionary.items(),
            key=lambda item: item[1], reverse=True))
        spinner.stop_and_persist(
            SYMBOLS['success'],
            "Matched {} items to {} items.[{}]".format(
                self.key_file,
                self.text_file,
                self.timer.timestampstr()
            )
        )

    def reset_log_file(self):
        with open(self.log_file, 'w') as fh:
            fh.close()

    def write_result2file(self):
        csv_file_handler = open(self.csv_file, 'w')
        write_count = 0
        spinner = Halo(
            text="Writing results to {}".format(
                self.csv_file),
            spinner='dots'
        )
        spinner.start()
        self.truncate_result()
        self.purge_limited_items()
        for item in self.__result_dictionary:
            write_count += 1
            csv_formatted_item = "{0}, {1} {2}".format(
                str(item), str(self.__result_dictionary[item]), END_LINE)
            csv_file_handler.write(csv_formatted_item)
            info = self.__logger.write_log(
                write_count, item, self.__result_dictionary[item]
            )
            if self.__set_verbose:
                print(
                    self.timer.timestampstr(),
                    info
                )
        csv_file_handler.close()
        spinner.stop_and_persist(
            SYMBOLS['success'],
            "{} Complete.[{}]".format(
                self.csv_file,
                self.timer.timestampstr()
            )
        )

    def run(self):
        self.reset_log_file()
        self.itemize_text()
        self.itemize_keys()
        self.match_text2keys()
        self.write_result2file()
        self.echo_result()
        self.echo_stats()

    def verify_files_exist(self, *args):
        for arg in args:
            if not os.path.exists(arg):
                self.__valid_files = False
            else:
                self.__valid_files = True
