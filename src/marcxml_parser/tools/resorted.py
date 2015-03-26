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
    if not values:
        return values

    values = sorted(values)

    # look for first word
    first_word = next(
        (cnt for cnt, val in enumerate(values)
             if val and not val[0].isdigit()),
        None
    )

    # if not found, just return the values
    if first_word is None:
        return values

    words = values[first_word:]
    numbers = values[:first_word]

    return words + numbers
