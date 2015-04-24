#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import dhtmlparser

from .query import MARCXMLQuery


# Functions & classes =========================================================
class MARCXMLRecord(MARCXMLQuery):
    """
    Syndication of :class:`.MARCXMLParser`, :class:`.MARCXMLSerializer` and
    :class:`.MARCXMLQuery` into one class for backward compatibility.
    """
    def __init__(self, xml=None, resort=True):
        super(MARCXMLRecord, self).__init__(xml, resort)


def record_iterator(xml):
    """
    Iterate over all ``<record>`` tags in `xml`.

    Args:
        xml (str/file): Input string with XML. UTF-8 is prefered encoding,
                        unicode should be ok.

    Yields:
        MARCXMLRecord: For each corresponding ``<record>``.
    """
    # handle file-like objects
    if hasattr(xml, "read"):
        xml = xml.read()

    dom = None
    try:
        dom = dhtmlparser.parseString(xml)
    except UnicodeError:
        dom = dhtmlparser.parseString(xml.encode("utf-8"))

    for record_xml in dom.findB("record"):
        yield MARCXMLRecord(record_xml)
