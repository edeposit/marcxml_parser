Marc XML / Marc OAI parser
==========================

Module for parsing and high-level processing of MARC XML records.

Standard MARC record is made from three parts:

* `leader` - Binary something, you can probably ignore it.
* `controlfields` - MARC fields with ``ID < 10``.
* `datafields` - Informations you actually want.

Basic MARC XML scheme has this structure::

    <record xmlns=definition..>
        <leader>optional_binary_something</leader>

        <controlfield tag="001">data</controlfield>
        ...
        <controlfield tag="010">data</controlfield>

        <datafield tag="011" ind1=" " ind2=" ">
            <subfield code="scode">data</subfield>
            <subfield code="a">data</subfield>
            <subfield code="a">another data, but same code!</subfield>
            ...
            <subfield code"scode+">another data</subfield>
        </datafield>

        ...

        <datafield tag="999" ind1=" " ind2=" ">
            ...
        </datafield>
    </record>

`<leader>` is optional and it is parsed into :attr:`MARCXMLRecord.leader` as
string.

`<controlfield>s` are optional and are parsed as dictionary into
:class:`MARCXMLRecord.controlfields`. Dictionary for data in example above
would look like this::

    MARCXMLRecord.controlfields = {
        "001": "data",
        ...
        "010": "data"
    }

`<datafield>s` are non-optional and are parsed into
:class:`MARCXMLRecord.datafields`, which is little bit more complicated
dictionary. Complicated is mainly because tag parameter is not unique, so there
can be more `<datafield>s` with same tag!

`scode` (subfield code) is always one character (ASCII lowercase), or number.

Example dict::

    MARCXMLRecord.datafields = {
        "011": [{
            "ind1": " ",
            "ind2": " ",
            "scode": ["data"],
            "scode+": ["another data"]
        }],

        # real example
        "928": [{
            "ind1": "1",
            "ind2": " ",
            "a": ["Portál"]
        }],

        "910": [
            {
                "ind1": "1",
                "ind2": " ",
                "a": ["ABA001"]
            },
            {
                "ind1": "2",
                "ind2": " ",
                "a": ["BOA001"],
                "b": ["2-1235.975"]
            },
            {
                "ind1": "3",
                "ind2": " ",
                "a": ["OLA001"],
                "b": ["1-218.844"]
            }
        ]
    }

Warning:
    NOTICE, THAT RECORDS ARE STORED IN ARRAY, NO MATTER IF IT IS JUST ONE
    RECORD, OR MULTIPLE RECORDS. SAME APPLY TO SUBFIELDS.

Example above corresponds with this piece of code from real world::

    <datafield tag="910" ind1="1" ind2=" ">
    <subfield code="a">ABA001</subfield>
    </datafield>
    <datafield tag="910" ind1="2" ind2=" ">
    <subfield code="a">BOA001</subfield>
    <subfield code="b">2-1235.975</subfield>
    </datafield>
    <datafield tag="910" ind1="3" ind2=" ">
    <subfield code="a">OLA001</subfield>
    <subfield code="b">1-218.844</subfield>
    </datafield>

OAI
===
To prevent things to be too much simple, there is also another type of MARC
XML document - OAI format.

OAI documents are little bit different, but almost same in structure.

`leader` is optional and is stored in ``MARCXMLRecord.controlfields["LDR"]``,
but also in :attr:`MARCXMLRecord.leader` for backward compatibility.

`<controlfield>` is renamed to `<fixfield>` and its "tag" parameter to "label".

`<datafield>` tag is not named datafield, but `<varfield>`, "tag" parameter is
"id" and ind1/ind2 are named i1/i2, but works the same way.

`<subfield>s` parameter "code" is renamed to "label".

Real world example::

    <oai_marc>
    <fixfield id="LDR">-----nam-a22------aa4500</fixfield>
    <fixfield id="FMT">BK</fixfield>
    <fixfield id="001">cpk19990652691</fixfield>
    <fixfield id="003">CZ-PrNK</fixfield>
    <fixfield id="005">20130513104801.0</fixfield>
    <fixfield id="007">tu</fixfield>
    <fixfield id="008">990330m19981999xr-af--d------000-1-cze--</fixfield>
    <varfield id="015" i1=" " i2=" ">
    <subfield label="a">cnb000652691</subfield>
    </varfield>
    <varfield id="020" i1=" " i2=" ">
    <subfield label="a">80-7174-091-8 (sv. 1 : váz.) :</subfield>
    <subfield label="c">Kč 182,00</subfield>
    </varfield>
    ...
    </oai_marc>

MARC documentation
------------------
`Definition of MARC OAI`_, `simplified MARC XML schema`_ and `full MARC XML
specification`_ of all elements (19492 lines of code) is freely accessible for
anyone interested.

.. _Definition of MARC OAI: http://www.openarchives.org/OAI/oai_marc.xsd
.. _simplified MARC XML schema: http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd
.. _full MARC XML specification: http://www.loc.gov/standards/marcxml/mrcbxmlfile.dtd 

API
===

.. automodule:: aleph.marcxml
    :members:
    :undoc-members:
    :show-inheritance:
