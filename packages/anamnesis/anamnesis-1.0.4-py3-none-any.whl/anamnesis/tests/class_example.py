#!/usr/bin/python3

# This file should be loaded during the register tests

"""Example class used by test cases"""

from ..register import register_class


class AutoLoadTestCase:
    pass


__all__ = ["AutoLoadTestCase"]
register_class(AutoLoadTestCase)
