#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from marcxml_parser.structures import Person


# Tests =======================================================================
def test_person_structure():
    p = Person(
        "Lishaak",
        "",
        "Bystroushaak",
        "-"
    )

    p2 = Person(
        name="Lishaak",
        second_name="",
        surname="Bystroushaak",
        title="-"
    )

    assert p == p2

    assert p.name == "Lishaak"
    assert p.second_name == ""
    assert p.surname == "Bystroushaak"
    assert p.title == "-"
