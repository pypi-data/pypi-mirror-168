#!/usr/bin/python3

# vim: set expandtab ts=4 sw=4:

"""Generic option handling code for anamnesis"""

from sys import stdout
from typing import TextIO

__all__ = []


class AnamOptions(object):
    """
    Singleton class for holding system-wide options
    """

    __shared_state = {}

    def __init__(self, *args, **kwargs):
        # Quick way of implementing a singleton
        self.__dict__ = self.__shared_state

        if not getattr(self, "initialised", False):
            self.initialised = True
            self.setup(*args, **kwargs)

    def setup(self) -> None:
        self.verbose = 0
        self.progress = 0

    def write(self, s: str, target: TextIO = stdout) -> None:
        if self.verbose > 0:
            target.write(s)

    def write_progress(self, s: str, target: TextIO = stdout) -> None:
        if self.progress > 0:
            target.write(s)


__all__.append("AnamOptions")
