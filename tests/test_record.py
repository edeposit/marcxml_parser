#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from marcxml_parser import MARCXMLRecord


# Functions & classes =========================================================
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
