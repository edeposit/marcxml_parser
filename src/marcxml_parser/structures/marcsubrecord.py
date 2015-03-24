#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================


# Functions & classes =========================================================
class MarcSubrecord(str):
    """
    This class is used to store data returned from
    :meth:`MARCXMLRecord.getDataRecords()`.

    It looks kinda like overshot, but when you are parsing the MARC XML,
    values from `subrecords`, you need to know the context in which the
    `subrecord` is put.

    This context is provided by the ``i1``/``i2`` values, but sometimes it is
    also useful to have access to the other subfields from this `subrecord`.

    This class provides this access by :meth:`getI1`/:meth:`getI2` and
    :meth:`getOtherSubfields` getters. As a bonus, it is also fully replaceable
    with string, in which case only the value of `subrecord` is preserved.

    Attributes:
        arg (str):   Value of `subrecord`.
        ind1 (char): Indicator one.
        ind2 (char): Indicator two.
        other_subfields (dict): Dictionary with other subfields from the same
                                `subrecord`.

    """
    def __new__(self, arg, ind1, ind2, other_subfields):
        return str.__new__(self, arg)

    def __init__(self, arg, ind1, ind2, other_subfields):
        self.arg = arg
        self.ind1 = ind1
        self.ind2 = ind2
        self.other_subfields = other_subfields

    def getI1(self):
        return self.ind1

    def getI2(self):
        return self.ind2

    def getOtherSubfields(self):
        """
        Return reference to dictionary, from which the `subrecord` was given.

        Note:
            This method is used to get `backlink` to other fields (reference to
            field in :attr:`MARCXMLRecord.datafields`). It is not clean, but it
            works.
        """
        return self.other_subfields

    def __str__(self):
        return self.arg