#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
"""
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
"""
from string import Template
from collections import namedtuple


import dhtmlparser
from dhtmlparser import HTMLElement


# Functions ===================================================================
def _undefinedPattern(value, fn, undefined):
    """
    If ``fn(value) == True``, return `undefined`, else `value`.
    """
    if fn(value):
        return undefined

    return value


def resorted(values):
    """
    Sort values, but put numbers after alphabetically sorted words.

    This function is here to make outputs diff-compatible with Aleph.

    Example::
        >>> sorted(["b", "1", "a"])
        ['1', 'a', 'b']
        >>> resorted(["b", "1", "a"])
        ['a', 'b', '1']

    Args:
        values (iterable): any iterable object/list/tuple/whatever.

    Returns:
        list of sorted values, but with numbers after words
    """
    values = sorted(values)
    words = filter(lambda x: not x.isdigit(), values)
    numbers = filter(lambda x: x.isdigit(), values)

    return words + numbers


# Classes =====================================================================
class Person(namedtuple("Person", ["name",
                                   "second_name",
                                   "surname",
                                   "title"])):
    """
    This class represents informations about persons as they are defined in
    MARC standards.

    Attributes:
        name (str)
        second_name (str)
        surname (str)
        title (str)
    """
    pass


class Corporation(namedtuple("Corporation", ["name", "place", "date"])):
    """
    Some informations about corporations (fields 110, 610, 710, 810).

    Attributes:
        name (str):  Name of the corporation.
        place (str): Location of the corporation/action.
        date (str):  Date in unspecified format.
    """
    pass


class MarcSubrecord(str):
    """
    This class is used to store data returned from
    :meth:`MARCXMLRecord.getDataRecords()`.

    It looks kinda like overshot, but when you are parsing the MARC XML,
    values from `subrecords`, you need to know the context in which the
    `subrecord` is put.

    This context is provided by the ``i1``/``i2`` values, but sometimes it is
    also useful to have access to the other subfields from this `subrecord`.

    This class provides this access by :meth:`getI1`/:meth:`getI2` and
    :meth:`getOtherSubfiedls` getters. As a bonus, it is also fully replaceable
    with string, in which case only the value of `subrecord` is preserved.

    Attributes:
        arg (str):   Value of `subrecord`.
        ind1 (char): Indicator one.
        ind2 (char): Indicator two.
        other_subfields (dict): Dictionary with other subfields from the same
                                `subrecord`.

    """
    def __new__(self, arg, ind1, ind2, other_subfields):
        return str.__new__(self, arg)

    def __init__(self, arg, ind1, ind2, other_subfields):
        self.arg = arg
        self.ind1 = ind1
        self.ind2 = ind2
        self.other_subfields = other_subfields

    def getI1(self):
        return self.ind1

    def getI2(self):
        return self.ind2

    def getOtherSubfiedls(self):
        """
        Return reference to dictionary, from which the `subrecord` was given.

        Note:
            This method is used to get `backlink` to other fields (reference to
            field in :attr:`MARCXMLRecord.datafields`). It is not clean, but it
            works.
        """
        return self.other_subfields

    def __str__(self):
        return self.arg


class MARCXMLRecord:
    """
    Class for serialization/deserialization of MARC XML and MARC OAI
    documents.

    This class parses everything between ``<root>`` elements. It checks, if
    there is root element, so please, give it full XML.

    Internal format is described in module docstring. You can access
    internal data directly, or using few handy methods on two different
    levels of abstraction.

    **No abstraction at all**

    You can choose to access data directly and for this use, there is few
    important properties:

    Attributes:
      leader         (string): Leader of MARC XML document.
      oai_marc       (bool): True/False, depending if doc is OAI doc or not
      controlfields  (dict): Controlfields stored in dict.
      datafields     (dict of arrays of dict of arrays of strings ^-^):
                     Datafileds stored in nested dicts/arrays.

    :attr:`controlfields` is simple and easy to use dictionary, where keys are
    field identificators (string, 3 chars, all chars digits). Value is
    always string.

    :attr:`datafields` is little more complicated; it is dictionary made of
    arrays of dictionaries, which consists of arrays of strings and two special
    parameters.

    It sounds horrible, but it is not that hard to understand::

        .datafields = {
            "011": ["ind1": " ", "ind2": " "]  # array of 0 or more dicts
            "012": [
                {
                    "a": ["a) subsection value"],
                    "b": ["b) subsection value"],
                    "ind1": " ",
                    "ind2": " "
                },
                {
                    "a": [
                        "multiple values in a) subsections are possible!",
                        "another value in a) subsection"
                    ],
                    "c": [
                        "subsection identificator is always one character long"
                    ],
                    "ind1": " ",
                    "ind2": " "
                }
            ]
        }

    Notice ``ind1``/``ind2`` keywords, which are reserved indicators and used
    in few cases thru MARC standard.

    Dict structure is not that hard to understand, but kinda long to access,
    so there is also higher-level abstraction access methods.

    **Lowlevel abstraction**

    To access data little bit easier, there are defined two methods to
    access and two methods to add data to internal dictionaries:

        - :meth:`addControlField`
        - :meth:`addDataField`

    Getters are also simple to use:

        - :meth:`getControlRecord`
        - :meth:`getDataRecords`

    :meth:`getControlRecord` is just wrapper over :attr:`controlfields` and
    works same way as accessing ``.controlfields[controlfield]``.

    ``.getDataRecords(datafield, subfield, throw_exceptions)`` return list of
    :class:`MarcSubrecord` objects* with informations from section `datafield`
    subsection `subfield`.

    If `throw_exceptions` parameter is set to ``False``, method returns empty
    list instead of throwing :exc:`~exceptions.KeyError`.

    \*As I said, function returns list of :class:`MarcSubrecord` objects. They
    are almost same thing as normal ``str`` (they are actually subclassed
    strings), but defines few important methods, which can make your life
    little bit easier:

        - :meth:`~MarcSubrecord.getI1`
        - :meth:`~MarcSubrecord.getI2`
        - :meth:`~MarcSubrecord.getOtherSubfiedls`

    :meth:`~MarcSubrecord.getOtherSubfiedls` returns dictionary with other
    subsections from subfield requested by calling :meth:`getDataRecords`. It
    works as backlink to object, from which you get the record.

    **Highlevel abstractions**

    There is also lot of highlevel getters:

        - :meth:`getName`
        - :meth:`getSubname`
        - :meth:`getPrice`
        - :meth:`getPart`
        - :meth:`getPartName`
        - :meth:`getPublisher`
        - :meth:`getPubDate`
        - :meth:`getPubOrder`
        - :meth:`getFormat`
        - :meth:`getPubPlace`
        - :meth:`getAuthors`
        - :meth:`getCorporations`
        - :meth:`getDistributors`
        - :meth:`getISBNs`
        - :meth:`getBinding`
        - :meth:`getOriginals`
    """
    def __init__(self, xml=None):
        self.leader = None
        self.oai_marc = False
        self.controlfields = {}
        self.datafields = {}
        self.valid_i_chars = list(" 0123456789")

        # it is always possible to create blank object and add values into it
        # piece by piece thru .addControlField()/.addDataField() methods.
        if xml is not None:
            self._original_xml = xml
            self.__parseString(xml)

    def addControlField(self, name, value):
        """
        Add new control field `value` with under `name` into control field
        dictionary :attr:`controlfields`.
        """
        if len(name) != 3:
            raise ValueError("name parameter have to be exactly 3 chars long!")

        self.controlfields[name] = value

    def addDataField(self, name, i1, i2, subfields_dict):
        """
        Add new datafield into :attr:`datafields`.

        Args:
            name (str): name of datafield
            i1 (char): value of i1/ind1 parameter
            i2 (char): value of i2/ind2 parameter
            subfields_dict (dict): dictionary containing subfields

        `subfields_dict` is expected to be in this format::

            {
                "field_id": ["subfield data",],
                ...
                "z": ["X0456b"]
            }

        Warning:
            ``field_id`` can be only one character long!

        Function takes care of OAI MARC.
        """
        if i1 not in self.valid_i_chars:
            raise ValueError("Invalid i1parameter '" + i1 + "'!")
        if i2 not in self.valid_i_chars:
            raise ValueError("Invalid i2parameter '" + i2 + "'!")
        if len(name) != 3:
            raise ValueError("name parameter have to be exactly 3 chars long!")
        if not isinstance(subfields_dict, dict):
            raise ValueError(
                "subfields_dict parameter has to be dict instance!"
            )
        for key in subfields_dict:
            if len(key) > 1:
                raise KeyError(
                    "subfields_dict can be only one character long!"
                )
            if not isinstance(subfields_dict[key], list):
                raise ValueError(
                    "Values at under '" + key + "' have to be list!"
                )

        subfields_dict[self.getI(1)] = i1
        subfields_dict[self.getI(2)] = i2

        # append dict, or add new dict into self.datafields
        if name in self.datafields:
            self.datafields[name].append(subfields_dict)
        else:
            self.datafields[name] = [subfields_dict]

    def getControlRecord(self, controlfield):
        """
        Return record from given `controlfield`. Returned type: str.
        """
        return self.controlfields[controlfield]

    def getDataRecords(self, datafield, subfield, throw_exceptions=True):
        """
        Return content of given `subfield` in `datafield`.

        Args:
            datafield (str): Section name (for example "001", "100", "700")
            subfield (str):  Subfield name (for example "a", "1", etc..)
            throw_exceptions (bool): If ``True``, :exc:`~exceptions.KeyError` is
                                     raised if method couldn't found given
                                     `datafield`/`subfield`. If ``False``, blank
                                     array ``[]`` is returned.

        Returns:
            list: of :class:`MarcSubrecord`. MarcSubrecord is practically      \
        same thing as string, but has defined :meth:`~MarcSubrecord.getI1()`   \
        and :meth:`~MarcSubrecord.getI2()` properties. Believe me, you will    \
        need to be able to get this, because MARC XML depends on them from time\
        to time (name of authors for example).
        """
        if len(datafield) != 3:
            raise ValueError(
                "datafield parameter have to be exactly 3 chars long!"
            )
        if len(subfield) != 1:
            raise ValueError(
                "Bad subfield specification - subfield have to be 3 chars long!"
            )

        if datafield not in self.datafields:
            if throw_exceptions:
                raise KeyError(datafield + " is not in datafields!")
            else:
                return []

        output = []
        for df in self.datafields[datafield]:
            if subfield not in df:
                if throw_exceptions:
                    raise KeyError(subfield + " is not in subfields!")
                else:
                    return []

            # records are not returned just like plain string, but like
            # MarcSubrecord, because you will need ind1/ind2 values
            for i in df[subfield]:
                output.append(
                    MarcSubrecord(
                        i,
                        df[self.getI(1)],
                        df[self.getI(2)],
                        df
                    )
                )

        return output

    def getName(self):
        """
        Returns:
            str: Name of the book.

        Raises:
            KeyError: when name is not specified.
        """
        return "".join(self.getDataRecords("245", "a", True))

    def getSubname(self, undefined=""):
        """
        Args:
            undefined (optional): returned if sub-name record is not found.

        Returns:
            str: Sub-name of the book or `undefined` if name is not defined.
        """
        return _undefinedPattern(
            "".join(self.getDataRecords("245", "b", False)),
            lambda x: x.strip() == "",
            undefined
        )

    def getPrice(self, undefined=""):
        """
        Returns:
            str: Price of the book (with currency).
        """
        return _undefinedPattern(
            "".join(self.getDataRecords("020", "c", False)),
            lambda x: x.strip() == "",
            undefined
        )

    def getPart(self, undefined=""):
        """
        Returns:
            str: Which part of the book series is this record.
        """
        return _undefinedPattern(
            "".join(self.getDataRecords("245", "p", False)),
            lambda x: x.strip() == "",
            undefined
        )

    def getPartName(self, undefined=""):
        """
        Returns:
            str: Name of the part of the series.
        """
        return _undefinedPattern(
            "".join(self.getDataRecords("245", "n", False)),
            lambda x: x.strip() == "",
            undefined
        )

    def getPublisher(self, undefined=""):
        """
        Returns:
            str: name of the publisher ("``Grada``" for example)
        """
        return _undefinedPattern(
            "".join(self.getDataRecords("260", "b", False)),
            lambda x: x.strip() == "",
            undefined
        )

    def getPubDate(self, undefined=""):
        """
        Returns:
            str: date of publication (month and year usually)
        """
        return _undefinedPattern(
            "".join(self.getDataRecords("260", "c", False)),
            lambda x: x.strip() == "",
            undefined
        )

    def getPubOrder(self, undefined=""):
        """
        Returns:
            str: information about order in which was the book published
        """
        return _undefinedPattern(
            "".join(self.getDataRecords("901", "f", False)),
            lambda x: x.strip() == "",
            undefined
        )

    def getFormat(self, undefined=""):
        """
        Returns:
            str: dimensions of the book ('``23 cm``' for example)
        """
        return _undefinedPattern(
            "".join(self.getDataRecords("300", "c", False)),
            lambda x: x.strip() == "",
            undefined
        )

    def getPubPlace(self, undefined=""):
        """
        Returns:
            str: name of city/country where the book was published
        """
        return _undefinedPattern(
            "".join(self.getDataRecords("260", "a", False)),
            lambda x: x.strip() == "",
            undefined
        )

    def getAuthors(self):
        """
        Returns:
            list: authors represented as Person objects
        """
        authors = self._parsePersons("100", "a")
        authors += self._parsePersons("600", "a")
        authors += self._parsePersons("700", "a")
        authors += self._parsePersons("800", "a")

        return authors

    def getCorporations(self, roles=["dst"]):
        """
        Args:
            roles (list, optional): specify which types of corporations you
                  need. Set to ``["any"]`` for any role, ``["dst"]`` for
                  distributors, etc..
                  See http://www.loc.gov/marc/relators/relaterm.html for
                  details.

        Returns:
            list: :class:`Corporation` objects specified by roles parameter.
        """
        corporations = self._parseCorporations("110", "a", roles)
        corporations += self._parseCorporations("610", "a", roles)
        corporations += self._parseCorporations("710", "a", roles)
        corporations += self._parseCorporations("810", "a", roles)

        return corporations

    def getDistributors(self):
        """
        Returns:
            list: distributors represented as :class:`Corporation` object
        """
        return self.getCorporations(roles=["dst"])

    def getISBNs(self):
        """
        Returns:
            list: array with ISBN strings
        """

        if len(self.getDataRecords("020", "a", False)) != 0:
            return map(
                lambda ISBN: ISBN.strip().split(" ", 1)[0],
                self.getDataRecords("020", "a", True)
            )

        if len(self.getDataRecords("901", "i", False)) != 0:
            return map(
                lambda ISBN: ISBN.strip().split(" ", 1)[0],
                self.getDataRecords("901", "i", True)
            )

        return []

    def getBinding(self):
        """
        Returns:
            list: array of strings with bindings (``["brož."]``) or blank list
        """
        if len(self.getDataRecords("020", "a", False)) != 0:
            return map(
                lambda x: x.strip().split(" ", 1)[1],
                filter(
                    lambda x: "-" in x and " " in x,
                    self.getDataRecords("020", "a", True)
                )
            )

        return []

    def getOriginals(self):
        """
        Returns:
            list: of original names
        """
        return self.getDataRecords("765", "t", False)

    def getI(self, num, is_oai=None):
        """
        This method is used mainly internally, but it can be handy if you work
        with with raw MARC XML object and not using getters.

        Args:
            num (int): Which indicator you need (1/2).
            is_oai (bool/None): If None, :attr:`MARCXMLRecord.oai_marc` is
                   used.

        Returns:
            str: current name of ``i1``/``ind1`` parameter based on \
                 :attr:`oai_marc` property.
        """
        if num != 1 and num != 2:
            raise ValueError("num parameter have to be 1 or 2!")

        if is_oai is None:
            is_oai = self.oai_marc

        i_name = "ind" if not is_oai else "i"

        return i_name + str(num)

    def _parseCorporations(self, datafield, subfield, roles=["any"]):
        """
        Parse informations about corporations from given field identified
        by `datafield` parameter.

        Args:
            datafield (str): MARC field ID ("``110``", "``610``", etc..)
            subfield (str):  MARC subfield ID with name, which is typically
                             stored in "``a``" subfield.
            roles (str): specify which roles you need. Set to ``["any"]`` for
                         any role, ``["dst"]`` for distributors, etc.. For
                         details, see
                         http://www.loc.gov/marc/relators/relaterm.html

        Returns:
            list: :class:`Corporation` objects.
        """
        if len(datafield) != 3:
            raise ValueError(
                "datafield parameter have to be exactly 3 chars long!"
            )
        if len(subfield) != 1:
            raise ValueError(
                "Bad subfield specification - subield have to be 3 chars long!"
            )
        parsed_corporations = []
        for corporation in self.getDataRecords(datafield, subfield, False):
            other_subfields = corporation.getOtherSubfiedls()

            # check if corporation have at least one of the roles specified in
            # 'roles' parameter of function
            if "4" in other_subfields and roles != ["any"]:
                corp_roles = other_subfields["4"]  # list of role parameters

                relevant = any(map(lambda role: role in roles, corp_roles))

                # skip non-relevant corporations
                if not relevant:
                    continue

            name = ""
            place = ""
            date = ""

            name = corporation

            if "c" in other_subfields:
                place = ",".join(other_subfields["c"])
            if "d" in other_subfields:
                date = ",".join(other_subfields["d"])

            parsed_corporations.append(Corporation(name, place, date))

        return parsed_corporations

    def _parsePersons(self, datafield, subfield, roles=["aut"]):
        """
        Parse persons from given datafield.

        Args:
            datafield (str): code of datafield ("010", "730", etc..)
            subfield (char):  code of subfield ("a", "z", "4", etc..)
            role (list of str): set to ["any"] for any role, ["aut"] for
                 authors, etc.. For details see
                 http://www.loc.gov/marc/relators/relaterm.html

        Main records for persons are: "100", "600" and "700", subrecords "c".

        Returns:
            list: Person objects.
        """
        # parse authors
        parsed_persons = []
        raw_persons = self.getDataRecords(datafield, subfield, False)
        for person in raw_persons:
            ind1 = person.getI1()
            ind2 = person.getI2()
            other_subfields = person.getOtherSubfiedls()

            # check if person have at least one of the roles specified in
            # 'roles' parameter of function
            if "4" in other_subfields and roles != ["any"]:
                person_roles = other_subfields["4"]  # list of role parameters

                relevant = any(map(lambda role: role in roles, person_roles))

                # skip non-relevant persons
                if not relevant:
                    continue

            # result is string, so ind1/2 in MarcSubrecord are lost
            person = person.strip()

            name = ""
            second_name = ""
            surname = ""
            title = ""

            # here it gets nasty - there is lot of options in ind1/ind2
            # parameters
            if ind1 == "1" and ind2 == " ":
                if "," in person:
                    surname, name = person.split(",", 1)
                elif " " in person:
                    surname, name = person.split(" ", 1)
                else:
                    surname = person

                if "c" in other_subfields:
                    title = ",".join(other_subfields["c"])
            elif ind1 == "0" and ind2 == " ":
                name = person.strip()

                if "b" in other_subfields:
                    second_name = ",".join(other_subfields["b"])

                if "c" in other_subfields:
                    surname = ",".join(other_subfields["c"])
            elif ind1 == "1" and ind2 == "0" or ind1 == "0" and ind2 == "0":
                name = person.strip()
                if "c" in other_subfields:
                    title = ",".join(other_subfields["c"])

            parsed_persons.append(
                Person(
                    name.strip(),
                    second_name.strip(),
                    surname.strip(),
                    title.strip()
                )
            )

        return parsed_persons

    def __parseString(self, xml):
        """
        Parse MARC XML document to dicts, which are contained in
        self.controlfields and self.datafields.

        Args:
            xml (str or HTMLElement): input data

        Also detect if this is oai marc format or not (see elf.oai_marc).
        """
        if not isinstance(xml, HTMLElement):
            xml = dhtmlparser.parseString(str(xml))

        # check if there are any records
        record = xml.find("record")
        if len(record) <= 0:
            raise ValueError("There is no <record> in your MARC XML document!")
        record = record[0]

        self.oai_marc = len(record.find("oai_marc")) > 0

        # leader is separate only in marc21
        if not self.oai_marc:
            leader = record.find("leader")
            if len(leader) >= 1:
                self.leader = leader[0].getContent()

        # parse body in respect of OAI MARC format possibility
        if self.oai_marc:
            self.__parseControlFields(record.find("fixfield"), "id")
            self.__parseDataFields(record.find("varfield"), "id", "label")
        else:
            self.__parseControlFields(record.find("controlfield"), "tag")
            self.__parseDataFields(record.find("datafield"), "tag", "code")

        # for backward compatibility of MARC XML with OAI
        if self.oai_marc and "LDR" in self.controlfields:
            self.leader = self.controlfields["LDR"]

    def __parseControlFields(self, fields, tag_id="tag"):
        """
        Parse control fields.

        Args:
            fields (list): list of HTMLElements
            tag_id (str):  parameter name, which holds the information, about
                           field name this is normally "tag", but in case of
                           oai_marc "id".
        """
        for field in fields:
            params = field.params
            if tag_id not in params:  # skip tags with blank parameters
                continue

            self.controlfields[params[tag_id]] = field.getContent().strip()

    def __parseDataFields(self, fields, tag_id="tag", sub_id="code"):
        """
        Parse data fields.

        Args:
            fields (list): of HTMLElements
            tag_id (str): parameter name, which holds the information, about
                          field name this is normally "tag", but in case of
                          oai_marc "id"
            sub_id (str): id of parameter, which holds informations about
                          subfield name this is normally "code" but in case of
                          oai_marc "label"

        """
        for field in fields:
            field_repr = {}
            params = field.params

            if tag_id not in params:
                continue

            tag = params[tag_id]

            # take care of iX/indX parameter - I have no idea what is this, but
            # they look important (=they are everywhere)
            i1_name = self.getI(1)
            i2_name = self.getI(2)
            field_repr = {
                i1_name: " " if i1_name not in params else params[i1_name],
                i2_name: " " if i2_name not in params else params[i2_name],
            }

            # process all subfields
            for subfield in field.find("subfield"):
                if sub_id not in subfield.params:
                    continue
                code = subfield.params[sub_id]

                if code in field_repr:
                    field_repr[code].append(subfield.getContent().strip())
                else:
                    field_repr[code] = [subfield.getContent().strip()]

            if tag in self.datafields:
                self.datafields[tag].append(field_repr)
            else:
                self.datafields[tag] = [field_repr]

    def __serializeControlFields(self):
        template = '<$TAGNAME $FIELD_NAME="$FIELD_ID">$CONTENT</$TAGNAME>\n'
        tagname = "controlfield" if not self.oai_marc else "fixfield"
        field_name = "tag" if not self.oai_marc else "id"

        output = ""
        for field_id in resorted(self.controlfields):
            # some control fields are specific for oai
            # if not self.oai_marc and field_id in ["LDR", "FMT"]:
            if not self.oai_marc and not field_id.isdigit():
                continue

            output += Template(template).substitute(
                TAGNAME=tagname,
                FIELD_NAME=field_name,
                FIELD_ID=field_id,
                CONTENT=self.controlfields[field_id]
            )

        return output

    def __serializeDataSubfields(self, subfields):
        template = '\n<$TAGNAME $FIELD_NAME="$FIELD_ID">$CONTENT</$TAGNAME>'

        tagname = "subfield"
        field_name = "code" if not self.oai_marc else "label"

        output = ""
        for field_id in resorted(subfields):
            for subfield in subfields[field_id]:
                output += Template(template).substitute(
                    TAGNAME=tagname,
                    FIELD_NAME=field_name,
                    FIELD_ID=field_id,
                    CONTENT=subfield
                )

        return output

    def __serializeDataFields(self):
        template = '<$TAGNAME $FIELD_NAME="$FIELD_ID" $I1_NAME="$I1_VAL" '
        template += '$I2_NAME="$I2_VAL">'
        template += '$CONTENT\n'
        template += '</$TAGNAME>\n'

        tagname = "datafield" if not self.oai_marc else "varfield"
        field_name = "tag" if not self.oai_marc else "id"

        i1_name = self.getI(1)
        i2_name = self.getI(2)

        output = ""
        for field_id in resorted(self.datafields):
            # unpac dicts from array
            for dict_field in self.datafields[field_id]:
                # this allows to convert between OAI and XML formats simply
                # by switching .oai_marc property
                real_i1_name = i1_name if i1_name in dict_field \
                                       else self.getI(1, not self.oai_marc)
                real_i2_name = i2_name if i2_name in dict_field \
                                       else self.getI(2, not self.oai_marc)

                i1_val = dict_field[real_i1_name]
                i2_val = dict_field[real_i2_name]

                # temporarily remove i1/i2 from dict
                del dict_field[real_i1_name]
                del dict_field[real_i2_name]

                output += Template(template).substitute(
                    TAGNAME=tagname,
                    FIELD_NAME=field_name,
                    FIELD_ID=field_id,
                    I1_NAME=i1_name,
                    I2_NAME=i2_name,
                    I1_VAL=i1_val,
                    I2_VAL=i2_val,
                    CONTENT=self.__serializeDataSubfields(dict_field)
                )

                # put back temporarily removed i1/i2
                dict_field[real_i1_name] = i1_val
                dict_field[real_i2_name] = i2_val

        return output

    def toXML(self):
        """
        Convert object back to XML string.

        Returns:
            str: String which should be same as original input, if everything\
                 works as expected.
        """
        marcxml_template = """<record xmlns="http://www.loc.gov/MARC21/slim/"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.loc.gov/MARC21/slim
http://www.loc.gov/standards/marcxml/schema/MARC21slim.xsd">
$LEADER
$CONTROL_FIELDS
$DATA_FIELDS
</record>
"""

        oai_template = """<record>
<metadata>
<oai_marc>
$LEADER$CONTROL_FIELDS
$DATA_FIELDS
</oai_marc>
</metadata>
</record>
"""

        # serialize leader, if it is present and record is marc xml
        leader = self.leader if self.leader is not None else ""
        if leader:  # print only visible leaders
            leader = "<leader>" + leader + "</leader>"

        # discard leader for oai
        if self.oai_marc:
            leader = ""

        # serialize
        xml_template = oai_template if self.oai_marc else marcxml_template
        xml_output = Template(xml_template).substitute(
            LEADER=leader.strip(),
            CONTROL_FIELDS=self.__serializeControlFields().strip(),
            DATA_FIELDS=self.__serializeDataFields().strip()
        )

        return xml_output

    def __str__(self):
        return self.toXML()

    def __repr__(self):
        return str(self.__dict__)
