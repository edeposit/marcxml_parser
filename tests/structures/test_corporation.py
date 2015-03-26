#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from marcxml_parser.structures import Corporation


# Tests =======================================================================
def test_corporation_structure():
    c = Corporation(
        "NAME",
        "PLACE",
        "NOW"
    )

    c2 = Corporation(
        name="NAME",
        place="PLACE",
        date="NOW"
    )

    assert c == c2

    assert c.name == "NAME"
    assert c.place == "PLACE"
    assert c.date == "NOW"
