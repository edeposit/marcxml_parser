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


# Fixtures ====================================================================
@pytest.fixture
def aleph_files():
    files = glob.glob(DATA_DIR + "/aleph_*.xml")

    return map(lambda x: os.path.abspath(x), files)


# Tests =======================================================================
def test_input_output(aleph_files):
    for fn in aleph_files:
        with open(fn) as f:
            data = f.read()

        parsed = MARCXMLRecord(data, resort=False)

        assert parsed.__str__().strip() == data.strip()


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


def test_creation_and_resort():
    rec = MARCXMLRecord()

    rec.add_data_field("222", "1", "2", {"a": "bbb"})
    rec.add_data_field("111", " ", " ", {"a": "aaa"})

    assert rec.__str__() == """<record xmlns="http://www.loc.gov/MARC21/slim/"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.loc.gov/MARC21/slim
http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd">


<datafield tag="111" ind1=" " ind2=" ">
<subfield code="a">aaa</subfield>
</datafield>
<datafield tag="222" ind1="1" ind2="2">
<subfield code="a">bbb</subfield>
</datafield>
</record>
"""


def test_creation_and_resort_disabled():
    rec = MARCXMLRecord(resort=False)

    rec.add_data_field("222", "1", "2", {"a": "bbb"})
    rec.add_data_field("111", " ", " ", {"a": "aaa"})

    assert rec.__str__() == """<record xmlns="http://www.loc.gov/MARC21/slim/"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.loc.gov/MARC21/slim
http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd">


<datafield tag="222" ind1="1" ind2="2">
<subfield code="a">bbb</subfield>
</datafield>
<datafield tag="111" ind1=" " ind2=" ">
<subfield code="a">aaa</subfield>
</datafield>
</record>
"""


def test_creation_and_subfields_resort():
    rec = MARCXMLRecord()

    rec.add_data_field(
        "111",
        " ",
        " ",
        OrderedDict([
            ["a", "1"],
            ["u", "1"],
            ["c", "1"]
        ])
    )

    assert rec.__str__() == """<record xmlns="http://www.loc.gov/MARC21/slim/"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.loc.gov/MARC21/slim
http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd">


<datafield tag="111" ind1=" " ind2=" ">
<subfield code="a">1</subfield>
<subfield code="c">1</subfield>
<subfield code="u">1</subfield>
</datafield>
</record>
"""


def test_creation_and_subfields_resort_disabled():
    rec = MARCXMLRecord(resort=False)

    rec.add_data_field(
        "111",
        " ",
        " ",
        OrderedDict([
            ["a", "1"],
            ["u", "1"],
            ["c", "1"]
        ])
    )

    assert rec.__str__() == """<record xmlns="http://www.loc.gov/MARC21/slim/"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.loc.gov/MARC21/slim
http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd">


<datafield tag="111" ind1=" " ind2=" ">
<subfield code="a">1</subfield>
<subfield code="u">1</subfield>
<subfield code="c">1</subfield>
</datafield>
</record>
"""
