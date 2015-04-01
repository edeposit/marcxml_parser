#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from marcxml_parser.structures import MARCSubrecord


# Tests =======================================================================
def test_MARCSubrecord_class():
    m = MARCSubrecord(
        "ola",
        "1",
        "2",
        []
    )

    m2 = MARCSubrecord(
        val="ola",
        i1="1",
        i2="2",
        other_subfields=[]
    )

    assert m == m2
    assert m == "ola"

    assert m.val == "ola"
    assert m.i1 == "1"
    assert m.i2 == "2"
    assert m.other_subfields == []
