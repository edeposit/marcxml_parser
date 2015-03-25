#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================


# Functions & classes =========================================================
def resorted(values):
    """
    Sort values, but put numbers after alphabetically sorted words.

    This function is here to make outputs diff-compatible with Aleph.

    Example::
        >>> sorted(["b", "1", "a"])
        ['1', 'a', 'b']
        >>> resorted(["b", "1", "a"])
        ['a', 'b', '1']

    Args:
        values (iterable): any iterable object/list/tuple/whatever.

    Returns:
        list of sorted values, but with numbers after words
    """
    values = sorted(values)
    words = filter(lambda x: not x.isdigit(), values)
    numbers = filter(lambda x: x.isdigit(), values)

    return words + numbers
