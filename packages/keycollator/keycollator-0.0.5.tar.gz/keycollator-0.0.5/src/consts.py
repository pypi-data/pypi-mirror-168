# -*- coding: utf-8 -*-
"""
Copyright (C) 2022 Rush Solutions, LLC
Author: David Rush <davidprush@gmail.com>
License: MIT
Contains Constants:
    consts.py
        └──DEFAULT_LOG_FILE:
        └──DEFAULT_TEXT_FILE:
        └──DEFAULT_CSV_FILE:
        └──DEFAULT_KEY_FILE:
        └──END_LINE:
        └──SYMBOLS:
        └──STOP_WORDS:
"""
import os
from pathlib import Path


# Default file names
DEFAULT_LOG_FILE = "log.log"
DEFAULT_TEXT_FILE = "text.txt"
DEFAULT_CSV_FILE = "results.csv"
DEFAULT_KEY_FILE = "keys.txt"

# Formatter constants
END_LINE = "\n"
MODES = ['a', 'r', 'w']
DTTEMPLATE = [
    '%d', '%m', '%Y',
    '%H', '%M', '%S',
    ' ', ':', '/'
]
DTDEFAULT = [
    '%d', '/', '%m',
    '/', '%Y', ' ',
    '%H', ':', '%M',
    ':', '%S'
]
# Symbols
SYMBOLS = {
    'info': 'ℹ',
    'success': '✔',
    'warning': '⚠',
    'error': '✖'
}
SYMBOLS_FALLBACK = {
    'info': '¡',
    'success': 'v',
    'warning': '!!',
    'error': '×'
}
LOG_DEFAULT_PARAMS = {
    'filename': DEFAULT_LOG_FILE,
    'filemode': 'a',
    'level': 'info',
    'dtformat': 'default',
    'message': "",
    'phony': 'no',
}
DATETIME_FORMATS = {
    'locale': '%c',
    'default': '%d/%m/%Y %H:%M:%S',
    'timeonly': '%H:%M:%S',
    'compressed': '%d%m%Y%H%M%S',
    'long': '%A %B %d, %Y, [%I:%M:%S %p]',
    'micro': '%H:%M:%S:%f'
}
# Stop Words
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