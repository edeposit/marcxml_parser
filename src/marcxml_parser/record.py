#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from .query import MARCXMLQuery


# Functions & classes =========================================================
class MARCXMLRecord(MARCXMLQuery):
    """
    Syndication of :class:`.MARCXMLParser`, :class:`.MARCXMLSerializer` and
    :class:`.MARCXMLQuery` into one class for backward compatibility.
    """
    def __init__(self, xml=None, resort=True):
        super(MARCXMLRecord, self).__init__(xml, resort)
