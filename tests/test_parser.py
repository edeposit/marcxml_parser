#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os
import os.path
import glob
from collections import OrderedDict

import pytest

from marcxml_parser import marcxml


# Variables ===================================================================
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


# Functions & classes =========================================================
@pytest.fixture
def aleph_files():
    files = glob.glob(DATA_DIR + "/aleph_*.xml")

    return map(lambda x: os.path.abspath(x), files)


@pytest.fixture
def unix_file():
    files = aleph_files()

    filename = next((x for x in files if "unix" in x))

    with open(filename) as f:
        return f.read()


@pytest.fixture
def record():
    return marcxml.MARCXMLRecord(unix_file())


# Tests =======================================================================
def test_order_original():
    xml = """<record xmlns="http://www.loc.gov/MARC21/slim/"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.loc.gov/MARC21/slim
http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd">


<datafield tag="650" ind1="0" ind2="7">
<subfield code="a">programování</subfield>
<subfield code="7">ph115891</subfield>
<subfield code="2">czenas</subfield>
</datafield>
</record>
"""
    parsed = marcxml.MARCXMLRecord(xml, resort=False)

    assert xml == parsed.__str__()


def test_order_resort():
    xml = """<record xmlns="http://www.loc.gov/MARC21/slim/"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.loc.gov/MARC21/slim
http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd">


<datafield tag="650" ind1="0" ind2="7">
<subfield code="a">programování</subfield>
<subfield code="7">ph115891</subfield>
<subfield code="2">czenas</subfield>
</datafield>
</record>
"""
    parsed = marcxml.MARCXMLRecord(xml, resort=True)

    assert parsed.__str__() == """<record xmlns="http://www.loc.gov/MARC21/slim/"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.loc.gov/MARC21/slim
http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd">


<datafield tag="650" ind1="0" ind2="7">
<subfield code="a">programování</subfield>
<subfield code="2">czenas</subfield>
<subfield code="7">ph115891</subfield>
</datafield>
</record>
"""


def test_input_output(aleph_files):
    for fn in aleph_files:
        with open(fn) as f:
            data = f.read()

        parsed = marcxml.MARCXMLRecord(data, resort=False)

        assert parsed.__str__().strip() == data.strip()


def test_leader(record):
    assert record.leader == "-----cam-a22------a-4500"


def test_control_getters(record):
    assert record.getControlRecord("001") == "cpk20051492461"
    assert record.getControlRecord("003") == "CZ-PrNK"
    assert record.getControlRecord("005") == "20120509091037.0"
    assert record.getControlRecord("007") == "ta"
    assert record.getControlRecord("008") == "041216s2004----xr-a---e-f----001-0-cze--"


def test_data_getter_properties(record):
    subrecord = record.getDataRecords("015", "a")

    assert subrecord

    subrecord = subrecord[0]

    # test convertibility to string
    assert subrecord == "cnb001492461"

    # test 'I' getters
    assert subrecord.getI1() == " "
    assert subrecord.getI2() == " "

    # test link to other subfileds
    assert subrecord.getOtherSubfields() == OrderedDict(
        [('ind1', ' '), ('ind2', ' '), ('a', ['cnb001492461'])]
    )