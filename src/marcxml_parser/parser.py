#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from collections import OrderedDict

import dhtmlparser
from dhtmlparser import HTMLElement

from . import tools
from .structures import MARCSubrecord


# Functions & classes =========================================================
class MARCXMLParser(object):
    """
    This class parses everything between ``<root>`` elements. It checks, if
    there is root element, so please, give it full XML.

    :attr:`controlfields` is simple dictionary, where keys are field
    identificators (string, 3 chars). Value is always string.

    :attr:`datafields` is little more complicated; it is dictionary made of
    arrays of dictionaries, which consists of arrays of :class:`MARCSubrecord`
    objects and two special parameters.

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

    Attributes:
      leader         (string): Leader of MARC XML document.
      oai_marc       (bool): True/False, depending if doc is OAI doc or not
      controlfields  (dict): Controlfields stored in dict.
      datafields     (dict of arrays of dict of arrays of strings): Datafileds
                     stored in nested dicts/arrays.
    """
    def __init__(self, xml=None, resort=True):
        """
        Constructor.

        Args:
            xml (str/file, default None): XML to be parsed. May be file-like
                object.
            resort (bool, default True): Sort the output alphabetically?
        """
        self.leader = None
        self.oai_marc = False
        self.controlfields = OrderedDict()
        self.datafields = OrderedDict()
        self.valid_i_chars = list(" 0123456789")

        # resort output XML alphabetically
        self.resorted = tools.resorted if resort else lambda x: x

        # handle file-like objects
        if hasattr(xml, "read"):
            xml = xml.read()

        # it is always possible to create blank object and add values into it
        # piece by piece using .add_ctl_field()/.add_data_field() methods.
        if xml is not None:
            self._original_xml = xml
            self._parse_string(xml)

    def _parse_string(self, xml):
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
        if not record:
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
            self._parse_control_fields(record.find("fixfield"), "id")
            self._parse_data_fields(record.find("varfield"), "id", "label")
        else:
            self._parse_control_fields(record.find("controlfield"), "tag")
            self._parse_data_fields(record.find("datafield"), "tag", "code")

        # for backward compatibility of MARC XML with OAI
        if self.oai_marc and "LDR" in self.controlfields:
            self.leader = self.controlfields["LDR"]

    def _parse_control_fields(self, fields, tag_id="tag"):
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

            # skip tags without parameters
            if tag_id not in params:
                continue

            self.controlfields[params[tag_id]] = field.getContent().strip()

    def _parse_data_fields(self, fields, tag_id="tag", sub_id="code"):
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
            params = field.params

            if tag_id not in params:
                continue

            # take care of iX/indX (indicator) parameters
            field_repr = OrderedDict([
                [self.i1_name, params.get(self.i1_name, " ")],
                [self.i2_name, params.get(self.i2_name, " ")],
            ])

            # process all subfields
            for subfield in field.find("subfield"):
                if sub_id not in subfield.params:
                    continue

                content = MARCSubrecord(
                    val=subfield.getContent().strip(),
                    i1=field_repr[self.i1_name],
                    i2=field_repr[self.i2_name],
                    other_subfields=field_repr
                )

                # add or append content to list of other contents
                code = subfield.params[sub_id]
                if code in field_repr:
                    field_repr[code].append(content)
                else:
                    field_repr[code] = [content]

            tag = params[tag_id]
            if tag in self.datafields:
                self.datafields[tag].append(field_repr)
            else:
                self.datafields[tag] = [field_repr]

    def add_ctl_field(self, name, value):
        """
        Add new control field `value` with under `name` into control field
        dictionary :attr:`controlfields`.
        """
        if len(name) != 3:
            raise ValueError("name parameter have to be exactly 3 chars long!")

        self.controlfields[name] = value

    def add_data_field(self, name, i1, i2, subfields_dict):
        """
        Add new datafield into :attr:`datafields` and take care of OAI MARC
        differencies.

        Args:
            name (str): Name of datafield.
            i1 (char): Value of i1/ind1 parameter.
            i2 (char): Value of i2/ind2 parameter.
            subfields_dict (dict): Dictionary containing subfields (as list).

        `subfields_dict` is expected to be in this format::

            {
                "field_id": ["subfield data",],
                ...
                "z": ["X0456b"]
            }

        Warning:
            For your own good, use OrderedDict for `subfields_dict`, or
            constructor's `resort` parameter set to ``True`` (it is by
            default).

        Warning:
            ``field_id`` can be only one character long!

        """
        if i1 not in self.valid_i_chars:
            raise ValueError("Invalid i1 parameter '" + i1 + "'!")
        if i2 not in self.valid_i_chars:
            raise ValueError("Invalid i2 parameter '" + i2 + "'!")

        if len(name) != 3:
            raise ValueError(
                "`name` parameter have to be exactly 3 chars long!"
            )
        if not subfields_dict:
            raise ValueError(
                "`subfields_dict` have to contain something!"
            )
        if not isinstance(subfields_dict, dict):
            raise ValueError(
                "`subfields_dict` parameter has to be dict instance!"
            )

        # check local keys, convert strings to MARCSubrecord instances
        subrecords = []
        for key, val in subfields_dict.items():
            if len(key) > 1:
                raise KeyError(
                    "`subfields_dict` can be only one character long!"
                )

            # convert other values to lists
            if not isinstance(val, list):
                val = [val]

            subfields = map(
                lambda x: MARCSubrecord(x, i1, i2, None),
                val
            )

            subfields_dict[key] = subfields
            subrecords.extend(subfields)

        # save i/ind values
        subfields_dict[self.i1_name] = i1
        subfields_dict[self.i2_name] = i2

        # append dict, or add new dict into self.datafields
        if name in self.datafields:
            self.datafields[name].append(subfields_dict)
        else:
            self.datafields[name] = [subfields_dict]

        # to each subrecord add reference to list of all subfields in this
        # datafield
        other_subfields = self.datafields[name]
        for record in subrecords:
            record.other_subfields = other_subfields

    def get_i_name(self, num, is_oai=None):
        """
        This method is used mainly internally, but it can be handy if you work
        with with raw MARC XML object and not using getters.

        Args:
            num (int): Which indicator you need (1/2).
            is_oai (bool/None): If None, :attr:`.oai_marc` is
                   used.

        Returns:
            str: current name of ``i1``/``ind1`` parameter based on \
                 :attr:`oai_marc` property.
        """
        if num not in (1, 2):
            raise ValueError("`num` parameter have to be 1 or 2!")

        if is_oai is None:
            is_oai = self.oai_marc

        i_name = "ind" if not is_oai else "i"

        return i_name + str(num)

    @property
    def i1_name(self):
        """
        Property getter / alias for ``self.get_i_name(1)``.
        """
        return self.get_i_name(1)

    @property
    def i2_name(self):
        """
        Property getter / alias for ``self.get_i_name(2)``.
        """
        return self.get_i_name(2)

    def get_ctl_field(self, controlfield, alt=None):
        """
        Method wrapper over :attr:`.controlfields` dictionary.

        Args:
            controlfield (str): Name of the controlfield.
            alt (object, default None): Alternative value of the `controlfield`
                when `controlfield` couldn't be found.

        Returns:
            str: record from given `controlfield`
        """
        if not alt:
            return self.controlfields[controlfield]

        return self.controlfields.get(controlfield, alt)

    def getDataRecords(self, datafield, subfield, throw_exceptions=True):
        """
        .. deprecated::
            Use :func:`get_subfields` instead.
        """
        return self.get_subfields(
            datafield=datafield,
            subfield=subfield,
            exception=throw_exceptions
        )

    def get_subfields(self, datafield, subfield, i1=None, i2=None,
                      exception=False):
        """
        Return content of given `subfield` in `datafield`.

        Args:
            datafield (str): Section name (for example "001", "100", "700").
            subfield (str):  Subfield name (for example "a", "1", etc..).
            i1 (str, default None): Optional i1/ind1 parameter value, which
               will be used for search.
            i2 (str, default None): Optional i2/ind2 parameter value, which
               will be used for search.
            exception (bool): If ``True``, :exc:`~exceptions.KeyError` is
                      raised when method couldn't found given `datafield` /
                      `subfield`. If ``False``, blank array ``[]`` is returned.

        Returns:
            list: of :class:`.MARCSubrecord`.

        Raises:
            KeyError: If the subfield or datafield couldn't be found.

        Note:
            MARCSubrecord is practically same thing as string, but has defined
            :meth:`.MARCSubrecord.i1` and :attr:`.MARCSubrecord.i2`
            methods.

            You may need to be able to get this, because MARC XML depends on
            i/ind parameters from time to time (names of authors for example).

        """
        if len(datafield) != 3:
            raise ValueError(
                "`datafield` parameter have to be exactly 3 chars long!"
            )
        if len(subfield) != 1:
            raise ValueError(
                "Bad subfield specification - subfield have to be 1 char long!"
            )

        # if datafield not found, return or raise exception
        if datafield not in self.datafields:
            if exception:
                raise KeyError(datafield + " is not in datafields!")

            return []

        # look for subfield defined by `subfield`, `i1` and `i2` parameters
        output = []
        for datafield in self.datafields[datafield]:
            if subfield not in datafield:
                continue

            # records are not returned just like plain string, but like
            # MARCSubrecord, because you will need ind1/ind2 values
            for sfield in datafield[subfield]:
                if i1 and sfield.i1 != i1:
                    continue

                if i2 and sfield.i2 != i2:
                    continue

                output.append(sfield)

        if not output and exception:
            raise KeyError(subfield + " couldn't be found in subfields!")

        return output
