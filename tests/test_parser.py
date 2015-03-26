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

from marcxml_parser import MARCXMLRecord


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
    return MARCXMLRecord(unix_file())


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
    parsed = MARCXMLRecord(xml, resort=False)

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
    parsed = MARCXMLRecord(xml, resort=True)

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


def test_get_i_name(record):
    assert record.get_i_name(1) == "ind1"
    assert record.get_i_name(2) == "ind2"

    assert record.i1_name == "ind1"
    assert record.i2_name == "ind2"


def test_input_output(aleph_files):
    for fn in aleph_files:
        with open(fn) as f:
            data = f.read()

        parsed = MARCXMLRecord(data, resort=False)

        assert parsed.__str__().strip() == data.strip()


def test_leader(record):
    assert record.leader == "-----cam-a22------a-4500"


def test_control_getters(record):
    assert record.get_ctlfield("001") == "cpk20051492461"
    assert record.get_ctlfield("003") == "CZ-PrNK"
    assert record.get_ctlfield("005") == "20120509091037.0"
    assert record.get_ctlfield("007") == "ta"
    assert record.get_ctlfield("008") == "041216s2004----xr-a---e-f----001-0-cze--"

    assert record.get_ctlfield("azgabash", alt="xe") == "xe"


def test_data_getter_properties(record):
    subrecord = record.getDataRecords("015", "a")

    assert subrecord

    subrecord = subrecord[0]

    # test convertibility to string
    assert subrecord == "cnb001492461"

    # test 'I' getters
    assert subrecord.i1 == " "
    assert subrecord.i2 == " "

    # test link to other subfileds
    assert subrecord.other_subfields == OrderedDict(
        [('ind1', ' '), ('ind2', ' '), ('a', ['cnb001492461'])]
    )

    with pytest.raises(KeyError):
        record.get_subfield("015", "b", exception=True)

    assert record.get_subfield("015", "b", exception=False) == []


def test_data_getters(record):
    assert record.get_subfield("015", "a")[0] == "cnb001492461"
    ind_test = record.get_subfield("015", "a")[-1]
    assert ind_test.i1 == " "
    assert ind_test.i2 == " "

    assert record.get_subfield("020", "a")[0] == "80-251-0225-4 (brož.) :"
    assert record.get_subfield("020", "c")[0] == "Kč 590,00"
    ind_test = record.get_subfield("020", "c")[-1]
    assert ind_test.i1 == " "
    assert ind_test.i2 == " "

    assert record.get_subfield("035", "a")[0] == "(OCoLC)85131856"
    ind_test = record.get_subfield("035", "a")[-1]
    assert ind_test.i1 == " "
    assert ind_test.i2 == " "

    assert record.get_subfield("040", "a")[0] == "BOA001"
    assert record.get_subfield("040", "b")[0] == "cze"
    assert record.get_subfield("040", "d")[0] == "ABA001"
    ind_test = record.get_subfield("040", "d")[-1]
    assert ind_test.i1 == " "
    assert ind_test.i2 == " "

    assert record.get_subfield("041", "a")[0] == "cze"
    assert record.get_subfield("041", "h")[0] == "eng"
    ind_test = record.get_subfield("041", "h")[-1]
    assert ind_test.i1 == "1"
    assert ind_test.i2 == " "

    assert record.get_subfield("072", "a")[0] == "004.4/.6"
    assert record.get_subfield("072", "x")[0] == "Programování. Software"
    assert record.get_subfield("072", "2")[0] == "Konspekt"
    assert record.get_subfield("072", "9")[0] == "23"
    ind_test = record.get_subfield("072", "9")[-1]
    assert ind_test.i1 == " "
    assert ind_test.i2 == "7"

    assert record.get_subfield("080", "a")[0] == "004.451.9Unix"
    assert record.get_subfield("080", "2")[0] == "MRF"
    ind_test = record.get_subfield("080", "2")[0]
    assert ind_test.i1 == " "
    assert ind_test.i2 == " "

    assert record.get_subfield("080", "a")[1] == "004.451"
    assert record.get_subfield("080", "2")[1] == "MRF"
    ind_test = record.get_subfield("080", "2")[1]
    assert ind_test.i1 == " "
    assert ind_test.i2 == " "

    assert record.get_subfield("080", "a")[2] == "004.42"
    assert record.get_subfield("080", "2")[2] == "MRF"
    ind_test = record.get_subfield("080", "2")[-1]
    assert ind_test.i1 == " "
    assert ind_test.i2 == " "

    assert record.get_subfield("080", "a")[3] == "(035)"
    assert record.get_subfield("080", "2")[3] == "MRF"
    ind_test = record.get_subfield("080", "2")[-1]
    assert ind_test.i1 == " "
    assert ind_test.i2 == " "

    assert record.get_subfield("100", "a")[0] == "Raymond, Eric S."
    assert record.get_subfield("100", "7")[0] == "jn20020721375"
    assert record.get_subfield("100", "4")[0] == "aut"
    ind_test = record.get_subfield("100", "4")[-1]
    assert ind_test.i1 == "1"
    assert ind_test.i2 == " "

    assert record.get_subfield("245", "a")[0] == "Umění programování v UNIXu /"
    assert record.get_subfield("245", "c")[0] == "Eric S. Raymond"
    ind_test = record.get_subfield("245", "c")[-1]
    assert ind_test.i1 == "1"
    assert ind_test.i2 == "0"

    assert record.get_subfield("250", "a")[0] == "Vyd. 1."
    ind_test = record.get_subfield("250", "a")[-1]
    assert ind_test.i1 == " "
    assert ind_test.i2 == " "

    assert record.get_subfield("260", "a")[0] == "Brno :"
    assert record.get_subfield("260", "b")[0] == "Computer Press,"
    assert record.get_subfield("260", "c")[0] == "2004"
    ind_test = record.get_subfield("260", "c")[-1]
    assert ind_test.i1 == " "
    assert ind_test.i2 == " "

    assert record.get_subfield("300", "a")[0] == "509 s. :"
    assert record.get_subfield("300", "b")[0] == "il. ;"
    assert record.get_subfield("300", "c")[0] == "23 cm"
    ind_test = record.get_subfield("300", "c")[-1]
    assert ind_test.i1 == " "
    assert ind_test.i2 == " "

    assert record.get_subfield("500", "a")[0] == "Glosář"
    ind_test = record.get_subfield("500", "a")[-1]
    assert ind_test.i1 == " "
    assert ind_test.i2 == " "

    assert record.get_subfield("504", "a")[0] == "Obsahuje bibliografii, bibliografické odkazy a rejstřík"
    ind_test = record.get_subfield("504", "a")[-1]
    assert ind_test.i1 == " "
    assert ind_test.i2 == " "

    assert record.get_subfield("546", "a")[0] == "Přeloženo z angličtiny"
    ind_test = record.get_subfield("546", "a")[-1]
    assert ind_test.i1 == " "
    assert ind_test.i2 == " "

    assert record.get_subfield("650", "a")[0] == "UNIX"
    assert record.get_subfield("650", "7")[0] == "ph117153"
    assert record.get_subfield("650", "2")[0] == "czenas"
    ind_test = record.get_subfield("650", "2")[0]
    assert ind_test.i1 == "0"
    assert ind_test.i2 == "7"

    assert record.get_subfield("650", "a")[1] == "operační systémy"
    assert record.get_subfield("650", "7")[1] == "ph115593"
    assert record.get_subfield("650", "2")[1] == "czenas"
    ind_test = record.get_subfield("650", "2")[1]
    assert ind_test.i1 == "0"
    assert ind_test.i2 == "7"

    assert record.get_subfield("650", "a")[2] == "programování"
    assert record.get_subfield("650", "7")[2] == "ph115891"
    assert record.get_subfield("650", "2")[2] == "czenas"
    ind_test = record.get_subfield("650", "2")[2]
    assert ind_test.i1 == "0"
    assert ind_test.i2 == "7"

    assert record.get_subfield("650", "a")[3] == "UNIX"
    assert record.get_subfield("650", "2")[3] == "eczenas"
    ind_test = record.get_subfield("650", "2")[3]
    assert ind_test.i1 == "0"
    assert ind_test.i2 == "9"

    assert record.get_subfield("650", "a")[4] == "operating systems"
    assert record.get_subfield("650", "2")[4] == "eczenas"
    ind_test = record.get_subfield("650", "2")[4]
    assert ind_test.i1 == "0"
    assert ind_test.i2 == "9"

    assert record.get_subfield("650", "a")[5] == "programming"
    assert record.get_subfield("650", "2")[5] == "eczenas"
    ind_test = record.get_subfield("650", "2")[5]
    assert ind_test.i1 == "0"
    assert ind_test.i2 == "9"

    assert record.get_subfield("655", "a")[0] == "příručky"
    assert record.get_subfield("655", "7")[0] == "fd133209"
    assert record.get_subfield("655", "2")[0] == "czenas"
    ind_test = record.get_subfield("655", "2")[0]
    assert ind_test.i1 == " "
    assert ind_test.i2 == "7"

    assert record.get_subfield("655", "a")[1] == "handbooks, manuals, etc."
    assert record.get_subfield("655", "2")[1] == "eczenas"
    ind_test = record.get_subfield("655", "2")[1]
    assert ind_test.i1 == " "
    assert ind_test.i2 == "9"

    assert record.get_subfield("765", "t")[0] == "Art of UNIX programming"
    assert record.get_subfield("765", "9")[0] == "Česky"
    ind_test = record.get_subfield("765", "9")[-1]
    assert ind_test.i1 == "0"
    assert ind_test.i2 == " "

    assert record.get_subfield("901", "b")[0] == "9788025102251"
    assert record.get_subfield("901", "f")[0] == "1. vyd."
    assert record.get_subfield("901", "o")[0] == "20050217"
    ind_test = record.get_subfield("901", "o")[-1]
    assert ind_test.i1 == " "
    assert ind_test.i2 == " "

    assert record.get_subfield("910", "a")[0] == "ABA001"
    ind_test = record.get_subfield("910", "a")[-1]
    assert ind_test.i1 == "1"
    assert ind_test.i2 == " "


def test_get_subfield_i_parameters(record):
    assert record.get_subfield("901", "b", " ", " ")[0] == "9788025102251"
    assert record.get_subfield("901", "f", " ", " ")[0] == "1. vyd."
    assert record.get_subfield("901", "o", " ", " ")[0] == "20050217"

    assert len(record.get_subfield("650", "a", "0", "9")) == 3

    assert record.get_subfield("650", "a", "0", "9")[0] == "UNIX"
    assert record.get_subfield("650", "2", "0", "9")[0] == "eczenas"

    assert record.get_subfield("650", "a", "0", "9")[1] == "operating systems"
    assert record.get_subfield("650", "2", "0", "9")[1] == "eczenas"

    assert record.get_subfield("650", "a", "0", "9")[2] == "programming"
    assert record.get_subfield("650", "2", "0", "9")[2] == "eczenas"
