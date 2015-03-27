#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest

from marcxml_parser import Person
from marcxml_parser import PublicationType

from marcxml_parser.query import MARCXMLQuery

from test_parser import unix_file
from test_serializer import aleph_files


# Functions & classes =========================================================
@pytest.fixture
def epub_file():
    files = aleph_files()

    filename = next((x for x in files if "epub" in x))

    with open(filename) as f:
        return f.read()


@pytest.fixture
def parsed():
    return MARCXMLQuery(unix_file())


@pytest.fixture
def epub():
    return MARCXMLQuery(epub_file())


# Tests =======================================================================
def test_get_name(parsed):
    assert parsed.get_name() == "Umění programování v UNIXu"


def test_get_subname(parsed):
    assert parsed.get_subname(undefined=None) is None


def test_get_price(parsed):
    assert parsed.get_price() == "Kč 590,00"


def test_get_part(parsed):
    assert parsed.get_part(undefined=None) is None


def test_get_part_name(parsed):
    assert parsed.get_part_name(undefined=None) is None


def test_get_publisher(parsed):
    assert parsed.get_publisher() == "Computer Press"


def test_get_pub_date(parsed):
    assert parsed.get_pub_date() == "2004"


def test_get_pub_order(parsed):
    assert parsed.get_pub_order() == "1. vyd."


def test_get_format(parsed):
    assert parsed.get_format() == "23 cm"


def test_get_pub_place(parsed):
    assert parsed.get_pub_place() == "Brno"


def test_get_authors(parsed):
    author = Person(
        name='Eric S.',
        second_name="",
        surname='Raymond',
        title="",
    )

    assert parsed.get_authors() == [author]


def test_get_corporations(parsed):
    assert parsed.get_corporations() == []


def test_get_distributors(parsed):
    assert parsed.get_distributors() == []


def test_get_ISBNs(parsed):
    assert parsed.get_ISBNs() == ['80-251-0225-4']


def test_get_binding(parsed):
    assert parsed.get_binding() == ["brož."]


def test_get_originals(parsed):
    assert parsed.get_originals() == ["Art of UNIX programming"]


def test_get_urls(parsed):
    assert parsed.get_urls() == []


def test_publication_type(parsed):
    assert parsed.get_pub_type() == PublicationType.monographic


def test_is_monographic(parsed):
    assert parsed.is_monographic() == True


def test_is_multi_mono(parsed):
    assert parsed.is_multi_mono() == False


def test_is_continuing(parsed):
    assert parsed.is_continuing() == False


def test_is_single_unit(parsed):
    assert parsed.is_single_unit() == False



# Tests of epub file ==========================================================
def test_epub_get_urls(epub):
    assert epub.get_urls() == []


def test_epub_get_internal_urls(epub):
    base_url = "http://edeposit-test.nkp.cz"
    path = "/producents/nakladatelstvi-delta/epublications/echa-201"

    url = base_url + path

    assert epub.get_internal_urls() == [
        url + "0-2011/echa-2010-2011-eva-jelinkova-michael-spirit-eds.pdf",
        url + "0-2011-1/echa-2010-2011-eva-jelinkova-michael-spirit-eds.epub",
        url + "0-2011-1/echa-2010-2011-eva-jelinkova-michael-spirit-eds.mobi",
        url + "2-1/echa-2012-eva-jelinkova-michael-spirit-eds.mobi",
        url + "0-2011/echa-2013-eva-jelinkova-michael-spirit-eds.epub",
        "http://aleph.nkp.cz/F/?func=direct&doc_number=000003059&local_base=CZE-DEP"
    ]


def test_epub_publication_type(epub):
    assert epub.get_pub_type() == PublicationType.monographic


def test_epub_is_monographic(epub):
    assert epub.is_monographic() == True


def test_epub_is_multi_mono(epub):
    assert epub.is_multi_mono() == False


def test_epub_is_continuing(epub):
    assert epub.is_continuing() == False


def test_epub_is_single_unit(epub):
    assert epub.is_single_unit() == False
