# -*- coding: utf-8 -*-
"""
Copyright (C) 2022 Rush Solutions, LLC
Author: David Rush <davidprush@gmail.com>
License: MIT
Contains class:
    CustomLogger
        └──usage:
"""
import os
from collections import defaultdict
from datetime import datetime

from consts import \
    DEFAULT_LOG_FILE, SYMBOLS, END_LINE, \
    MODES, LOG_DEFAULT_PARAMS, DATETIME_FORMATS


class CustomLogger:
    def __init__(self, *args, **kwargs):
        """
        Constructs and starts the CustomLogger object.
        arguements
        ----------
        *args:
            all args are converted to strings and appended to
                text str for the log message
        parameters
        ----------
        **kwargs:
            text: str, optional
            filemode: str, optional
                valid modes are 'a', 'w', 'r', default is 'a'
            level: str, optional
                valid options are 'info', 'success', 'warning', 'error'
            filename: str, optional
                name of the log file, default is DEFAULT_LOG_FILE from .consts
            dtformat: str, optional
                format date with:
                    ['locale', 'standar', 'timeonly', 'compressed', 'long', 'micro']
                    locale='%c', default='%d/%m/%Y %H:%M:%S',
                    timeonly='%H:%M:%S', compressed='%d%m%Y%H%M%S',
                    long='%A %B %d, %Y, [%I:%M:%S %p]', micro='%H:%M:%S:%f'
            message: str, optional
                message used for the log
        """
        self.__dtstamp = datetime.now()
        self.__log_symbol = SYMBOLS['info']
        self.__log_msg = ""
        self.__err_msg = ""
        self.__log_err = False
        self.__valid_params = False
        self.__log_count = 0
        self.__params = defaultdict(str)
        self.__params = {
            'filename': DEFAULT_LOG_FILE,
            'filemode': 'a',
            'level': 'info',
            'dtformat': 'default',
            'message': '',
            'phony': 'No',
        }
        if kwargs:
            self.set_options(kwargs)
        if args:
            self.set_log_msg(args)

    def __validate_dtformat(self):
        if self.__params['dtformat'] in [x for x in DATETIME_FORMATS]:
            self.__update_dtstamp
            return True
        else:
            self.__log_err = True
            self.__logger_error(
                "Invalid datetime format: ",
                self.__params['dtformat'],
                " falling back to \'default\': ",
                DATETIME_FORMATS['default'], END_LINE,
                "VALID datetime formats: ",
                ''.join(["[ {0} ] ".format(key) for key in DATETIME_FORMATS.keys()]),
                END_LINE
            )
            self.__params['dtformat'] = DATETIME_FORMATS['default']
            self.__log_err = False
            return False

    def __logger_error(self, *args):
        if self.__log_err:
            self.__err_msg = "Log[{0}]::[{1}]::INVALID OPTIONS:{2}".format(
                str(self.__log_count), str(self.__update_dtstamp()), END_LINE)
            for arg in args:
                for a in arg:
                    self.__err_msg += "{0}".format(str(a))
            if END_LINE not in self.__err_msg[len(self.__err_msg) - 2]:
                self.__err_msg += END_LINE
            print(self.__err_msg)
            return True
        else:
            return False

    def __update_dtstamp(self):
        self.__dtstamp = datetime.now()
        self.__dtstamp = \
            self.__dtstamp.strftime(DATETIME_FORMATS[self.__params['dtformat']])
        return self.__dtstamp

    def __set_params(self):
        self.__valid_params = True
        self.__log_err = False
        param_err = defaultdict()
        if not isinstance(self.__params['message'], str):
            self.__params['text'] = str(self.__params['text'])
        if self.__params['filemode'] not in MODES:
            self.__valid_params = False
            param_err['filemode'] = self.__params['filemode']
            self.__params['filemode'] = 'a'
            param_err['filemode'] = self.__params['filemode']
        if self.__params['level'] not in SYMBOLS.keys():
            self.__valid_params = False
            self.__params['level'] = 'info'
            param_err['level'] = self.__params['level']
        if not os.path.exists(self.__params['filename']):
            self.__valid_params = False
            param_err['filename'] = self.__params['filename']
            self.__params['filename'] = DEFAULT_LOG_FILE
        if not self.__validate_dtformat():
            self.__valid_params = False
            param_err['dtformat'] = self.__params['dtformat']
        if self.__params['phony'].lower() not in ['yes', 'no']:
            self.__valid_params = False
            param_err['phony'] = self.__params['phony']
            self.__params['phony'] = 'no'
        if not self.__valid_params:
            self.__log_err = True
            self.__logger_error(
                ["{0}: {1} ".format(
                    str(err), str(param_err[err])) for err in param_err]
            )
            self.__log_err = False
        return self.__valid_params

    def set_log_msg(self, *args, **kwargs):
        self.__log_count += 1
        self.__log_msg = ""
        if kwargs is not None:
            self.__log_symbol = kwargs.get(
                'symbol', 'info')
            new_kwargs = {k: v for k, v in kwargs.items() if k in ['symbol']}
            self.set_options(new_kwargs)
        self.__log_msg = "{0} {1}::{2}::".format(
            SYMBOLS['info'], str(self.__log_count), str(self.__update_dtstamp()))
        if args is not None:
            for arg in args:
                self.__log_msg += "{0}".format(str(arg))
        if END_LINE != self.__log_msg[len(self.__log_msg) - 2]:
            self.__log_msg += END_LINE
        return self.__log_msg

    def write_log(self, *args, **kwargs):
        if kwargs is not None:
            self.set_options(kwargs)
        self.set_log_msg(args)
        if self.__params['phony'].lower() == 'no':
            try:
                with open(
                    self.__params['filename'],
                        self.__params['filemode']) as log_fh:
                    log_fh.write(self.__log_msg)
            finally:
                log_fh.close()
        return self.__params['message']

    def set_options(self, *args, **kwargs):
        param_err = defaultdict(str)
        for opt in kwargs:
            if opt not in [x for x in self.__params]:
                param_err[opt] = kwargs[opt]
                self.__log_err = True
            else:
                self.__params[opt] = opt
        for param in [
            li for li in self.__params
                if li not in kwargs]:
            if param in [x for x in LOG_DEFAULT_PARAMS]:
                self.__params[param] = str(LOG_DEFAULT_PARAMS[param]) \
                    if not isinstance(LOG_DEFAULT_PARAMS[param], str) \
                    else LOG_DEFAULT_PARAMS[param]
        if self.__log_err:
            self.__logger_error(
                ["{0}:{1}".format(str(e), str(param_err[e])) for e in param_err])
            return False
        elif self.__set_params():
            return True
        return True

    def log_count(self):
        return self.__log_count

    def create_log_file(self):
        with open(
            self.__params['filename'],
                self.__params['filemode']) as log_fh:
            log_fh.close()

    def set_symbol(self, symbol):
        if symbol not in [SYMBOLS[x] for x in SYMBOLS]:
            self.__logger_error('SYMBOL:=', symbol, " not valid!")
            return False
        else:
            return True
