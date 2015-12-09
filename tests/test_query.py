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
def read_file_from_partial_name(partial_name):
    files = aleph_files()

    filename = next((x for x in files if partial_name in x))

    with open(filename) as f:
        return f.read()


@pytest.fixture
def epub_file():
    return read_file_from_partial_name("epub")


def pasivni_domy_file():
    return read_file_from_partial_name("pasivni")


@pytest.fixture
def parsed():
    return MARCXMLQuery(unix_file())


@pytest.fixture
def epub():
    return MARCXMLQuery(epub_file())


@pytest.fixture
def pasivni_domy():
    return MARCXMLQuery(pasivni_domy_file())


@pytest.fixture
def zavate_doby():
    return MARCXMLQuery(read_file_from_partial_name("zavate"))


@pytest.fixture
def vladci_strachu():
    return MARCXMLQuery(read_file_from_partial_name("vladci"))


@pytest.fixture
def periodical():
    return MARCXMLQuery(read_file_from_partial_name("periodical"))


@pytest.fixture
def kviti():
    return MARCXMLQuery(read_file_from_partial_name("kviti"))


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


def test_get_invalid_ISBNs(parsed):
    assert parsed.get_invalid_ISBNs() == []


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


def test_indexing_operator(parsed):
    assert parsed["015a"][0] == "cnb001492461"
    assert parsed["015b"] == []

    assert parsed["901b  "][0] == "9788025102251"
    assert parsed["901f  "][0] == "1. vyd."
    assert parsed["901o  "][0] == "20050217"

    assert len(parsed["650a09"]) == 3

    assert parsed["650a09"][0] == "UNIX"
    assert parsed["650209"][0] == "eczenas"

    assert parsed["650a09"][1] == "operating systems"
    assert parsed["650209"][1] == "eczenas"

    assert parsed["650a09"][2] == "programming"
    assert parsed["650209"][2] == "eczenas"


def test_indexing_operator_fail(parsed):
    assert parsed["001"] == "cpk20051492461"
    assert parsed["003"] == "CZ-PrNK"
    assert parsed["005"] == "20120509091037.0"
    assert parsed["007"] == "ta"
    assert parsed["008"] == "041216s2004----xr-a---e-f----001-0-cze--"

    assert parsed["azg"] is None


def test_binding_of_parsed(parsed):
    assert parsed.get_binding() == ["brož."]


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
    assert epub.is_monographic()


def test_epub_is_multi_mono(epub):
    assert not epub.is_multi_mono()


def test_epub_is_continuing(epub):
    assert not epub.is_continuing()


def test_epub_is_single_unit(epub):
    assert not epub.is_single_unit()


def test_binding_of_epub(epub):
    assert epub.get_binding() == []


def test_epub_get_pub_date(epub):
    assert epub.get_pub_date() == "2014"


# Tests of pasivni domy =======================================================
def test_get_authors_pasivni_domy(pasivni_domy):
    assert pasivni_domy.get_authors() == []


# Tests of zavate doby ========================================================
def test_invalid_isbns(zavate_doby):
    invalid = zavate_doby.get_invalid_ISBNs()

    assert invalid == ["978-80-260-9075-5"]


def test_valid_isbns(zavate_doby):
    assert zavate_doby.get_ISBNs() == ["978-80-260-9077-9", "978-80-260-9076-2"]


def test_binding_of_zavate_doby(zavate_doby):
    assert zavate_doby.get_binding() == []


# Tests of vladci strachu =====================================================
def test_binding_of_vladci_strachu(vladci_strachu):
    assert vladci_strachu.get_binding() == ["brož."]


# Tests of periodical documents ===============================================
def test_periodical_issn(periodical):
    assert periodical.get_ISSNs() == ["1213-8215"]
    assert not periodical.get_invalid_ISSNs()
    assert not periodical.get_linking_ISSNs()
    assert periodical.is_continuing


def test_periodical_place(periodical):
    assert periodical.get_pub_place() == "Praha"


def test_periodical_publisher(periodical):
    assert periodical.get_publisher() == "JASTOG.CZ"


def test_periodical_pub_date(periodical):
    assert periodical.get_pub_date() == "2002-"


# Tests of kviti ==============================================================
def test_kviti_type(periodical):
    assert not periodical.is_continuing()
    assert not periodical.is_multi_mono()
    assert periodical.is_monographic()
