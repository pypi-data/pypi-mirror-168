# -*- coding: utf-8 -*-
"""
Copyright (C) 2022 Rush Solutions, LLC
Author: David Rush <davidprush@gmail.com>
License: MIT
Contains class:
    ProcedureTimer
        └──usage:
"""
import time


class ProcedureTimer:
    def __init__(
        self,
        caller="ProcedureTimer"
    ):
        """
        Constructs and starts the ProcedureTimer object.
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

    def stop_timer(self, caller="stop_timer"):
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

    def timestampstr(self):
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
