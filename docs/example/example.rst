Example of usage
================

Lets say, that you have following MARC OAI document, which you need to process:

.. code-block:: xml

    <record>
    <metadata>
    <oai_marc>
    <fixfield id="LDR">-----nas-a22------a-4500</fixfield>
    <fixfield id="FMT">SE</fixfield>
    <fixfield id="001">nkc20150003059</fixfield>
    <fixfield id="003">CZ-PrNK</fixfield>
    <fixfield id="005">20150326133612.0</fixfield>
    <fixfield id="007">ta</fixfield>
    <fixfield id="008">150312c20149999xr--u---------0---b0cze--</fixfield>
    <varfield id="BAS" i1=" " i2=" ">
    <subfield label="a">01</subfield>
    </varfield>
    <varfield id="040" i1=" " i2=" ">
    <subfield label="a">ABA001</subfield>
    <subfield label="b">cze</subfield>
    </varfield>
    <varfield id="245" i1="0" i2="0">
    <subfield label="a">Echa ... :</subfield>
    <subfield label="b">[fórum pro literární vědu] /</subfield>
    <subfield label="c">Jiří Brabec ... [et al.]</subfield>
    </varfield>
    <varfield id="246" i1="3" i2=" ">
    <subfield label="a">Echa Institutu pro studium literatury ...</subfield>
    </varfield>
    <varfield id="260" i1=" " i2=" ">
    <subfield label="a">Praha :</subfield>
    <subfield label="b">Institut pro studium literatury,</subfield>
    <subfield label="c">[2014?]-</subfield>
    </varfield>
    <varfield id="300" i1=" " i2=" ">
    <subfield label="a">^^^ online zdroj</subfield>
    </varfield>
    <varfield id="362" i1="0" i2=" ">
    <subfield label="a">2010/2011</subfield>
    </varfield>
    <varfield id="500" i1=" " i2=" ">
    <subfield label="a">Součástí názvu je označení rozmezí let, od r. 2012 součástí názvu označení kalendářního roku vzniku příspěvků</subfield>
    </varfield>
    <varfield id="500" i1=" " i2=" ">
    <subfield label="a">V některých formátech autoři neuvedeni</subfield>
    </varfield>
    <varfield id="500" i1=" " i2=" ">
    <subfield label="a">Jednotlivé sv. mají ISBN</subfield>
    </varfield>
    <varfield id="500" i1=" " i2=" ">
    <subfield label="a">Popsáno podle: 2010/2011</subfield>
    </varfield>
    <varfield id="700" i1="1" i2=" ">
    <subfield label="a">Brabec, Jiří</subfield>
    <subfield label="4">aut</subfield>
    </varfield>
    <varfield id="856" i1="4" i2="0">
    <subfield label="u">http://edeposit-test.nkp.cz/producents/nakladatelstvi-delta/epublications/echa-2010-2011/echa-2010-2011-eva-jelinkova-michael-spirit-eds.pdf</subfield>
    <subfield label="z">2010-2011</subfield>
    <subfield label="4">N</subfield>
    </varfield>
    <varfield id="856" i1="4" i2="0">
    <subfield label="u">http://edeposit-test.nkp.cz/producents/nakladatelstvi-delta/epublications/echa-2010-2011-1/echa-2010-2011-eva-jelinkova-michael-spirit-eds.epub</subfield>
    <subfield label="z">2010-2011</subfield>
    <subfield label="4">N</subfield>
    </varfield>
    <varfield id="856" i1="4" i2="0">
    <subfield label="u">http://edeposit-test.nkp.cz/producents/nakladatelstvi-delta/epublications/echa-2010-2011-1/echa-2010-2011-eva-jelinkova-michael-spirit-eds.mobi</subfield>
    <subfield label="z">201-2011</subfield>
    <subfield label="4">N</subfield>
    </varfield>
    <varfield id="856" i1="4" i2="0">
    <subfield label="u">http://edeposit-test.nkp.cz/producents/nakladatelstvi-delta/epublications/echa-2012-1/echa-2012-eva-jelinkova-michael-spirit-eds.mobi</subfield>
    <subfield label="z">2012</subfield>
    <subfield label="4">N</subfield>
    </varfield>
    <varfield id="856" i1="4" i2="0">
    <subfield label="u">http://edeposit-test.nkp.cz/producents/nakladatelstvi-delta/epublications/echa-2010-2011/echa-2013-eva-jelinkova-michael-spirit-eds.epub</subfield>
    <subfield label="z">2013</subfield>
    <subfield label="4">N</subfield>
    </varfield>
    <varfield id="902" i1=" " i2=" ">
    <subfield label="a">978-80-87899-10-6</subfield>
    <subfield label="q">(2010/2011 :</subfield>
    <subfield label="q">online :</subfield>
    <subfield label="q">pdf)</subfield>
    </varfield>
    <varfield id="902" i1=" " i2=" ">
    <subfield label="a">978-80-87899-09-0</subfield>
    <subfield label="q">(2010/2011 :</subfield>
    <subfield label="q">online :</subfield>
    <subfield label="q">Mobipocket)</subfield>
    </varfield>
    <varfield id="902" i1=" " i2=" ">
    <subfield label="a">978-80-87899-08-3</subfield>
    <subfield label="q">(2010/2011 :</subfield>
    <subfield label="q">online :</subfield>
    <subfield label="q">ePub)</subfield>
    </varfield>
    <varfield id="902" i1=" " i2=" ">
    <subfield label="a">978-80-87899-06-9</subfield>
    <subfield label="q">(2012 :</subfield>
    <subfield label="q">online :</subfield>
    <subfield label="q">Mobipocket)</subfield>
    </varfield>
    <varfield id="902" i1=" " i2=" ">
    <subfield label="a">978-80-87899-05-2</subfield>
    <subfield label="q">(2012 :</subfield>
    <subfield label="q">online :</subfield>
    <subfield label="q">ePub)</subfield>
    <subfield label="z">978-80-87899-07-6</subfield>
    </varfield>
    <varfield id="902" i1=" " i2=" ">
    <subfield label="a">978-80-87899-07-6</subfield>
    <subfield label="q">(2012 :</subfield>
    <subfield label="q">online :</subfield>
    <subfield label="q">pdf)</subfield>
    <subfield label="z">978-80-87899-05-2</subfield>
    </varfield>
    <varfield id="902" i1=" " i2=" ">
    <subfield label="a">978-80-87899-02-1</subfield>
    <subfield label="q">(2013 :</subfield>
    <subfield label="q">online :</subfield>
    <subfield label="q">ePub)</subfield>
    </varfield>
    <varfield id="902" i1=" " i2=" ">
    <subfield label="a">978-80-87899-03-8</subfield>
    <subfield label="q">(2013 :</subfield>
    <subfield label="q">online :</subfield>
    <subfield label="q">Mobipocket)</subfield>
    </varfield>
    <varfield id="902" i1=" " i2=" ">
    <subfield label="a">978-80-87899-04-5</subfield>
    <subfield label="q">(2013 :</subfield>
    <subfield label="q">online :</subfield>
    <subfield label="q">pdf)</subfield>
    </varfield>
    <varfield id="910" i1=" " i2=" ">
    <subfield label="a">ABA001</subfield>
    <subfield label="s">2010/2011, 2012-2013-</subfield>
    </varfield>
    <varfield id="998" i1=" " i2=" ">
    <subfield label="a">http://aleph.nkp.cz/F/?func=direct&amp;doc_number=000003059&amp;local_base=CZE-DEP</subfield>
    </varfield>
    <varfield id="PSP" i1=" " i2=" ">
    <subfield label="a">BK</subfield>
    </varfield>
    <varfield id="IST" i1="1" i2=" ">
    <subfield label="a">jp20150312</subfield>
    <subfield label="b">kola</subfield>
    </varfield>
    </oai_marc>
    </metadata>
    </record>

This document is saved at ``tests/data/aleph_epub.xml``. To parse this document,
you just open it and create :class:`.MARCXMLRecord` object from the string:

.. code-block:: python

    from marcxml_parser import MARCXMLRecord

    with open("tests/data/aleph_epub.xml") as f:
        data = f.read()

    rec = MARCXMLRecord(data)

Lowlevel access
---------------

All the controlfields and datafields were parsed into
:attr:`.controlfields` and :attr:`.datafields`:

.. code-block:: python

    >>> rec.controlfields

.. code-block:: python

    OrderedDict([
        ('LDR', '-----nas-a22------a-4500'),
        ('FMT', 'SE'),
        ('001', 'nkc20150003059'),
        ('003', 'CZ-PrNK'),
        ('005', '20150326133612.0'),
        ('007', 'ta'),
        ('008', '150312c20149999xr--u---------0---b0cze--'),
    ])

.. code-block:: python

    >>> rec.controlfields

.. code-block:: python

    OrderedDict([
        ('BAS', [OrderedDict([('i1', ' '), ('i2', ' '), ('a', ['01'])])]),
        ('040', [OrderedDict([
            ('i1', ' '),
            ('i2', ' '),
            ('a', ['ABA001']),
            ('b', ['cze'])
        ])]),
        ('245', [OrderedDict([
            ('i1', '0'),
            ('i2', '0'),
            ('a', ['Echa ... :']),
            ('b', ['[f\xc3\xb3rum pro liter\xc3\xa1rn\xc3\xad v\xc4\x9bdu] /']),
            ('c', ['Ji\xc5\x99\xc3\xad Brabec ... [et al.]'])
        ])]),
        ('246', [OrderedDict([
            ('i1', '3'),
            ('i2', ' '),
            ('a', ['Echa Institutu pro studium literatury ...'])
        ])]),
        ('260', [OrderedDict([
            ('i1', ' '),
            ('i2', ' '),
            ('a', ['Praha :']),
            ('b', ['Institut pro studium literatury,']),
            ('c', ['[2014?]-'])
        ])]),
        ('300', [OrderedDict([
            ('i1', ' '),
            ('i2', ' '),
            ('a', ['^^^ online zdroj'])
        ])]),
        ('362', [OrderedDict([
            ('i1', '0'),
            ('i2', ' '),
            ('a', ['2010/2011'])
        ])]),
        ('500', 
            [OrderedDict([
                ('i1', ' '),
                ('i2', ' '),
                ('a', ['Sou\xc4\x8d\xc3\xa1st\xc3\xad n\xc3\xa1zvu je ozna\xc4\x8den\xc3\xad rozmez\xc3\xad let, od r. 2012 sou\xc4\x8d\xc3\xa1st\xc3\xad n\xc3\xa1zvu ozna\xc4\x8den\xc3\xad kalend\xc3\xa1\xc5\x99n\xc3\xadho roku vzniku p\xc5\x99\xc3\xadsp\xc4\x9bvk\xc5\xaf'])
            ]),
            OrderedDict([
                ('i1', ' '),
                ('i2', ' '),
                ('a', ['V n\xc4\x9bkter\xc3\xbdch form\xc3\xa1tech auto\xc5\x99i neuvedeni'])
            ]),
            OrderedDict([
                ('i1', ' '),
                ('i2', ' '),
                ('a', ['Jednotliv\xc3\xa9 sv. maj\xc3\xad ISBN'])
            ]),
            OrderedDict([
                ('i1', ' '),
                ('i2', ' '),
                ('a', ['Pops\xc3\xa1no podle: 2010/2011'])
            ])
        ]),
        ('700', [OrderedDict([
            ('i1', '1'),
            ('i2', ' '),
            ('a', ['Brabec, Ji\xc5\x99\xc3\xad']),
            ('4', ['aut'])
        ])]),
        ('856', [
            OrderedDict([
                ('i1', '4'),
                ('i2', '0'),
                ('u', ['http://edeposit-test.nkp.cz/producents/nakladatelstvi-delta/epublications/echa-2010-2011/echa-2010-2011-eva-jelinkova-michael-spirit-eds.pdf']),
                ('z', ['2010-2011']),
                ('4', ['N'])
            ]),
            OrderedDict([
                ('i1', '4'),
                ('i2', '0'),
                ('u', ['http://edeposit-test.nkp.cz/producents/nakladatelstvi-delta/epublications/echa-2010-2011-1/echa-2010-2011-eva-jelinkova-michael-spirit-eds.epub']),
                ('z', ['2010-2011']),
                ('4', ['N'])
            ]),
            OrderedDict([
                ('i1', '4'),
                ('i2', '0'),
                ('u', ['http://edeposit-test.nkp.cz/producents/nakladatelstvi-delta/epublications/echa-2010-2011-1/echa-2010-2011-eva-jelinkova-michael-spirit-eds.mobi']),
                ('z', ['201-2011']),
                ('4', ['N'])
            ]),
            OrderedDict([
                ('i1', '4'),
                ('i2', '0'),
                ('u', ['http://edeposit-test.nkp.cz/producents/nakladatelstvi-delta/epublications/echa-2012-1/echa-2012-eva-jelinkova-michael-spirit-eds.mobi']),
                ('z', ['2012']),
                ('4', ['N'])
            ]),
            OrderedDict([
                ('i1', '4'),
                ('i2', '0'),
                ('u', ['http://edeposit-test.nkp.cz/producents/nakladatelstvi-delta/epublications/echa-2010-2011/echa-2013-eva-jelinkova-michael-spirit-eds.epub']),
                ('z', ['2013']),
                ('4', ['N'])
            ])
        ]),
        ('902', [
            OrderedDict([
                ('i1', ' '),
                ('i2', ' '),
                ('a', ['978-80-87899-10-6']),
                ('q', ['(2010/2011 :', 'online :', 'pdf)'])
            ]),
            OrderedDict([
                ('i1', ' '),
                ('i2', ' '),
                ('a', ['978-80-87899-09-0']),
                ('q', ['(2010/2011 :', 'online :', 'Mobipocket)'])
            ]),
            OrderedDict([
                ('i1', ' '),
                ('i2', ' '),
                ('a',"['978-80-87899-08-3']),
                ('q', ['(2010/2011 :', 'online :', 'ePub)'])
            ]),
            OrderedDict([
                ('i1', ' '),
                ('i2', ' '),
                ('a', ['978-80-87899-06-9']),
                ('q', ['(2012 :', 'online :', 'Mobipocket)'])
            ]),
            OrderedDict([
                ('i1', ' '),
                ('i2', ' '),
                ('a', ['978-80-87899-05-2']),
                ('q', ['(2012 :', 'online :' , 'ePub)']),
                ('z', ['978-80-87899-07-6'])
            ]),
            OrderedDict([
                ('i1', ' '),
                ('i2', ' '),
                ('a', ['978-80-87899-07-6']),
                ('q', ['(2012 :', 'online :', 'pdf)']),
                ('z', ['978-80-87899-05-2'])
            ]),
            OrderedDict([
                ('i1', ' '),
                ('i2', ' '),
                ('a', ['978-80-87899-02-1']),
                ('q', ['(2013 :', 'online :' , 'ePub)'])
            ]),
            OrderedDict([
                ('i1', ' '),
                ('i2', ' '),
                ('a', ['978-80-87899-03-8']),
                ('q', ['(2013 :', 'online :' , 'Mobipocket)'])
            ]),
            OrderedDict([
                ('i1', ' '),
                ('i2', ' '),
                ('a', ['978-80-87899-04-5']),
                ('q', ['(2013 :', 'online :' , 'pdf)'])
            ]),
        ]),
        ('910', [OrderedDict([
            ('i1', ' '),
            ('i2', ' '),
            ('a', ['ABA001']),
            ('s', ['2010/2011, 2012-2013-'])])
        ]),
        ('998', [OrderedDict([
            ('i1', ' '),
            ('i2', ' '),
            ('a', ['http://aleph.nkp.cz/F/?func=direct&doc_number=000003059&local_base=CZE-DEP'])
        ])]),
        ('PSP', [OrderedDict([('i1', ' '), ('i2', ' '), ('a', ['BK'])])]),
        ('IST', [OrderedDict([
            ('i1', '1'),
            ('i2', ' '),
            ('a', ['jp20150312']),
            ('b', ['kola'])
        ])]),
    ])

As you can see, this is more lowlevel, than you would ever want to use,
but it shows one important aspect of the parser - all values are parsed to
(ordered) dicts.

That means, that XML:

.. code-block:: XML

    <varfield id="902" i1=" " i2=" ">
    <subfield label="a">978-80-87899-05-2</subfield>
    <subfield label="q">(2012 :</subfield>
    <subfield label="q">online :</subfield>
    <subfield label="q">ePub)</subfield>
    <subfield label="z">978-80-87899-07-6</subfield>
    </varfield>
    <varfield id="902" i1=" " i2=" ">
    <subfield label="a">978-80-87899-07-6</subfield>
    <subfield label="q">(2012 :</subfield>
    <subfield label="q">online :</subfield>
    <subfield label="q">pdf)</subfield>
    <subfield label="z">978-80-87899-05-2</subfield>
    </varfield>

Have is parsed to:

.. code-block:: python

    OrderedDict([
        ('902', [
            OrderedDict([
                ('i1', ' '),
                ('i2', ' '),
                ('a', ['978-80-87899-05-2']),
                ('q', ['(2012 :', 'online :' , 'ePub)']),
                ('z', ['978-80-87899-07-6'])
            ]),
            OrderedDict([
                ('i1', ' '),
                ('i2', ' '),
                ('a', ['978-80-87899-07-6']),
                ('q', ['(2012 :', 'online :', 'pdf)']),
                ('z', ['978-80-87899-05-2'])
            ]),
        ]),
    ])

Which is equivalent with following code without ordered dicts:

.. code-block:: python

    {
        "902": [
            {
                'i1': ' ',
                'i2': ' ',
                'a': ['978-80-87899-05-2'],
                'q': ['(2012 :', 'online :' , 'ePub)'],
                'z': ['978-80-87899-07-6']
            },
            {
                'i1': ' ',
                'i2': ' ',
                'a': ['978-80-87899-07-6'],
                'q': ['(2012 :', 'online :', 'pdf)'],
                'z': ['978-80-87899-05-2']
            }
        ]
    }

Notice the ``q`` sub-record, qhich was three times in original XML and now is
in list.

This is the reason why most of the getters returns lists and not just simply
values - the nature of MARC records are lists.

Getters
-------

To access values inside :attr:`.controlfields` and :attr:`.datafields`, you can
use direct access to this dicts, but it is highly recommended to use highlevel
getters:

.. code-block:: python

    >>> rec.datafields["902"][4]["q"]

.. code-block:: python

    ['(2012 :', 'online :', 'ePub)']

vs:

.. code-block:: python

    >>> rec.get_subfields("902", "q")

.. code-block:: python

    [
        '(2010/2011 :',
        'online :',
        'pdf)',
        '(2010/2011 :',
        'online :',
        'Mobipocket)',
        '(2010/2011 :',
        'online :',
        'ePub)',
        '(2012 :',
        'online :',
        'Mobipocket)',
        '(2012 :',
        'online :',
        'ePub)',
        '(2012 :',
        'online :',
        'pdf)',
        '(2013 :',
        'online :',
        'ePub)',
        '(2013 :',
        'online :',
        'Mobipocket)',
        '(2013 :',
        'online :',
        'pdf)',
    ]

Whoa. What happened? There wasn't specified any more arguments to
:meth:`.get_subfields`, so all the ``902q`` subrecords were returned.

Lets look at the first returned item:

.. code-block:: python

    >>> rec.get_subfields("902", "q")[0]

.. code-block:: python

    '(2010/2011 :'

It looks like a string. But in fact, it is :class:`.MARCSubrecord` instance:

.. code-block:: python

    >>> type(rec.get_subfields("902", "q")[0])

.. code-block:: python

    <class 'marcxml_parser.structures.marcsubrecord.MARCSubrecord'>

That means, that it has more context, than ordinary string:

.. code-block:: python

    >>> r = rec.get_subfields("902", "q")[0]
    >>> r.val

.. code-block:: python

    '(2010/2011 :'

.. code-block:: python

    >>> r.i1

.. code-block:: python

    ' '

.. code-block:: python

    >>> r.i2

.. code-block:: python

    ' '

.. code-block:: python

    >>> r.other_subfields

.. code-block:: python

    OrderedDict([('i1', ' '), ('i2', ' '), ('a', ['978-80-87899-10-6']), ('q', ['(2010/2011 :', 'online :', 'pdf)'])])

Highlevel getters
-----------------

Highlevel getters are defined by :class:`.MARCXMLQuery`:

- :meth:`.get_name`
- :meth:`.get_subname`
- :meth:`.get_price`
- :meth:`.get_part`
- :meth:`.get_part_name`
- :meth:`.get_publisher`
- :meth:`.get_pub_date`
- :meth:`.get_pub_order`
- :meth:`.get_pub_place`
- :meth:`.get_format`
- :meth:`.get_authors`
- :meth:`.get_corporations`
- :meth:`.get_distributors`
- :meth:`.get_ISBNs`
- :meth:`.get_binding`
- :meth:`.get_originals`

You will probably like the indexing operator, which was redefined:

    >>> rec["500a"]

.. code-block:: python

    [
        'Sou\xc4\x8d\xc3\xa1st\xc3\xad n\xc3\xa1zvu je ...',  # shortened
        'V n\xc4\x9bkter\xc3\xbdch form\xc3\xa1tech auto\xc5\x99i neuvedeni',
        'Jednotliv\xc3\xa9 sv. maj\xc3\xad ISBN',
        'Pops\xc3\xa1no podle: 2010/2011'
    ]

.. code-block:: python

    >>> rec["001"]

.. code-block:: python

    'nkc20150003059

or with ``i1``/``i2`` arguments:

.. code-block:: python

    >>> rec["500a 9"]

.. code-block:: python

    []

(nothing was returned, because there isn't ``i1`` == `` `` and ``i2`` == ``9``)

.. code-block:: python

    >>> rec["902q  "]

.. code-block:: python

    [
        'Sou\xc4\x8d\xc3\xa1st\xc3\xad n\xc3\xa1zvu je ...',  # shortened
        'V n\xc4\x9bkter\xc3\xbdch form\xc3\xa1tech auto\xc5\x99i neuvedeni',
        'Jednotliv\xc3\xa9 sv. maj\xc3\xad ISBN',
        'Pops\xc3\xa1no podle: 2010/2011'
    ]