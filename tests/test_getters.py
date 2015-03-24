#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest

from marcxml_parser import marcxml

from test_parser import unix_file


# Variables ===================================================================



# Functions & classes =========================================================
@pytest.fixture
def parsed():
    return marcxml.MARCXMLRecord(unix_file())


# Tests =======================================================================
def test_getI(parsed):
    assert parsed.getI(1) == "ind1"
    assert parsed.getI(2) == "ind2"


def test_getName(parsed):
    assert parsed.getName() == "Umění programování v UNIXu"


def test_getSubname(parsed):
    assert parsed.getSubname(undefined=None) is None


def test_getPrice(parsed):
    assert parsed.getPrice(undefined="") == "Kč 590,00"


def test_getPart(parsed):
    assert parsed.getPart(undefined=None) is None


def test_getPartName(parsed):
    assert parsed.getPartName(undefined=None) is None


def test_getPublisher(parsed):
    assert parsed.getPublisher() == "Computer Press"


def test_getPubDate(parsed):
    assert parsed.getPubDate() == "2004"


def test_getPubOrder(parsed):
    assert parsed.getPubOrder() == "1. vyd."


def test_getFormat(parsed):
    assert parsed.getFormat() == "23 cm"


def test_getPubPlace(parsed):
    assert parsed.getPubPlace() == "Brno"


def test_getAuthors(parsed):
    author = marcxml.Person(
        name='Eric S.',
        second_name="",
        surname='Raymond',
        title="",
    )

    assert parsed.getAuthors() == [author]


def test_getCorporations(parsed):
    assert parsed.getCorporations() == []


def test_getDistributors(parsed):
    assert parsed.getDistributors() == []


def test_getISBNs(parsed):
    assert parsed.getISBNs() == ['80-251-0225-4']


def test_getBinding(parsed):
    assert parsed.getBinding() == "brož."


def test_getOriginals(parsed):
    assert parsed.getOriginals() == ["Art of UNIX programming"]
