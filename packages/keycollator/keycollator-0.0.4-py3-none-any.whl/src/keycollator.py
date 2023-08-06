#!venv/bin/ python3
# -*- coding: utf-8 -*-
"""
┬┌─┌─┐┬ ┬┌─┐┌─┐┬  ┬  ┌─┐┌┬┐┌─┐┬─┐
├┴┐├┤ └┬┘│  │ ││  │  ├─┤ │ │ │├┬┘
┴ ┴└─┘ ┴ └─┘└─┘┴─┘┴─┘┴ ┴ ┴ └─┘┴└─
Description:
    Compares text in a file to reference/glossary/key-items/dictionary file.
Copyright (C) 2022 Rush Solutions, LLC
Author: David Rush <davidprush@gmail.com>
License: MIT
Example:

        $ python keycollator.py

        Usage:

Todo:

    ***See Extractonator Todo Notes***

"""
import sys
import click

from extractonator import KeyKrawler
from proceduretimer import ProcedureTimer
from consts import \
    DEFAULT_LOG_FILE, DEFAULT_TEXT_FILE, \
    DEFAULT_CSV_FILE, DEFAULT_KEY_FILE


@click.group(
    context_settings=dict(
        ignore_unknown_options=True,
    ),
    invoke_without_command=True)
@click.option(
    '-t', '--text-file',
    default=DEFAULT_TEXT_FILE,
    type=click.Path(exists=True),
    help='''Path/file name of the text to be searched
    for against items in the key file'''
)
@click.option(
    '-k', '--key-file',
    default=DEFAULT_KEY_FILE,
    type=click.Path(exists=True),
    help='''Path/file name of the key file containing a
        dictionary, key items, glossary, or reference
        list used to search the text file'''
)
@click.option(
    '-r', '--result-file',
    default=DEFAULT_CSV_FILE,
    type=click.Path(exists=True),
    help="Path/file name of the output file that \
        will contain the results (CSV or TXT)"
)
@click.option(
    '--limit-result',
    default=0,
    help="Limit the number of results"
)
@click.option(
    '--fuzzy-match-ratio',
    default=99,
    type=click.IntRange(0, 99, clamp=True),
    help='''Set the level of fuzzy matching (default=99) to
        validate matches using approximations/edit distances,
        uses acceptance ratios with integer values from 0 to 99,
        where 99 is nearly identical and 0 is not similar'''
)
@click.option(
    '--ubound-limit',
    default=99999,
    type=click.IntRange(1, 99999, clamp=True),
    help="""
        Ignores items from the results with
        matches greater than the upper boundary (upper-limit);
        reduce eroneous matches
        """
)
@click.option(
    '--lbound-limit',
    default=0,
    type=click.IntRange(0, 99999, clamp=True),
    help="""
        Ignores items from the results with
        matches less than the lower boundary (lower-limit);
        reduce eroneous matches
        """
)
@click.option(
    '-v', '--verbose',
    is_flag=True,
    # default=0,
    # type=click.IntRange(0, 5, clamp=True),
    help="Turn on verbose"
)
@click.option(
    '-l', '--logging',
    is_flag=True,
    help="Turn on logging"
)
@click.option(
    '-L', '--log-file',
    default=DEFAULT_LOG_FILE,
    type=click.Path(exists=True),
    help="Path/file name to be used for the log file"
)
def cli(
    verbose,
    fuzzy_match_ratio,
    key_file,
    text_file,
    limit_result,
    result_file,
    ubound_limit,
    lbound_limit,
    logging,
    log_file,
):
    """
    keycollator is an app that finds occurances of keys in a text file
        Parameters
        ----------
        text_file: str, optional
            Name of the text file to find keys. (default: DEFAULT_TEXT_FILE)
        key_file: str, optional
            Name of file to read keys. (default: DEFAULT_KEY_FILE)
        result_file str, optional
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
    KeyKrawler(
        text_file,
        key_file,
        result_file,
        limit_result,
        log_file,
        verbose,
        ubound_limit,
        lbound_limit,
        fuzzy_match_ratio,
        logging,
        True
    )


def main(**kwargs):
    pt.stop_timer(sys._getframe().f_code.co_name)
    pt.echo(False, sys._getframe().f_code.co_name)


if __name__ == '__main__':
    pt = ProcedureTimer(sys._getframe().f_code.co_name)
    cli()
    main(pt)
