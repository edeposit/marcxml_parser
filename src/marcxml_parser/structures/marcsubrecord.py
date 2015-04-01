#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================


# Functions & classes =========================================================
class MARCSubrecord(str):
    """
    This class is used to store data returned from
    :meth:`.MARCXMLParser.get_datafield()`.

    It may look like overshot, but when you are parsing the MARC XML, values
    from `subrecords`, you need to know the context in which the `subrecord` is
    put.

    This context is provided by the ``i1``/``i2`` values, but sometimes it is
    also useful to have access to the other subfields from this `subrecord`.

    Attributes:
        val (str): Value of `subrecord`.
        ind1 (char): Indicator one.
        ind2 (char): Indicator two.
        other_subfields (dict): Dictionary with other subfields from the same
                                `subrecord`.

    """
    def __new__(self, val, i1, i2, other_subfields):
        return str.__new__(self, val)

    def __init__(self, val, i1, i2, other_subfields):
        self.val = val
        self.i1 = i1
        self.i2 = i2
        self.other_subfields = other_subfields

    def __str__(self):
        return self.val
