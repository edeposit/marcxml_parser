#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import remove_hairs
from remove_hairs import remove_hairs as remove_hairs_fn
from remove_hairs import remove_hairs_decorator

from .serializer import MARCXMLSerializer

from structures import Person
from structures import Corporation
from structures import PublicationType


# Variables ===================================================================
remove_hairs.HAIRS = r" :;<>(){}[]\/"


# Functions & classes =========================================================
def _undefined_pattern(value, fn, undefined):
    """
    If ``fn(value) == True``, return `undefined`, else `value`.
    """
    if fn(value):
        return undefined

    return value


class MARCXMLQuery(MARCXMLSerializer):
    """
    This class defines highlevel getters over MARC XML / OAI records.
    """
    def __init__(self, xml=None, resort=True):
        super(MARCXMLQuery, self).__init__(xml, resort)

    def _parse_corporations(self, datafield, subfield, roles=["any"]):
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
        for corporation in self.get_subfields(datafield, subfield):
            other_subfields = corporation.other_subfields

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

    def _parse_persons(self, datafield, subfield, roles=["aut"]):
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
        raw_persons = self.get_subfields(datafield, subfield)
        for person in raw_persons:
            # check if person have at least one of the roles specified in
            # 'roles' parameter of function
            other_subfields = person.other_subfields
            if "4" in other_subfields and roles != ["any"]:
                person_roles = other_subfields["4"]  # list of role parameters

                relevant = any(map(lambda role: role in roles, person_roles))

                # skip non-relevant persons
                if not relevant:
                    continue

            # result of .strip() is string, so ind1/2 in MARCSubrecord are lost
            ind1 = person.i1
            ind2 = person.i2
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

    @remove_hairs_decorator
    def get_name(self):
        """
        Returns:
            str: Name of the book.

        Raises:
            KeyError: When name is not specified.
        """
        return "".join(self.get_subfields("245", "a"))

    @remove_hairs_decorator
    def get_subname(self, undefined=""):
        """
        Args:
            undefined (optional): Argument, which will be returned if the
                      `subname` record is not found.

        Returns:
            str: Subname of the book or `undefined` if `subname` is not \
                 found.
        """
        return _undefined_pattern(
            "".join(self.get_subfields("245", "b")),
            lambda x: x.strip() == "",
            undefined
        )

    @remove_hairs_decorator
    def get_price(self, undefined=""):
        """
        Args:
            undefined (optional): Argument, which will be returned if the
                      `price` record is not found.

        Returns:
            str: Price of the book (with currency) or `undefined` if `price` \
                 is not found.
        """
        return _undefined_pattern(
            "".join(self.get_subfields("020", "c")),
            lambda x: x.strip() == "",
            undefined
        )

    @remove_hairs_decorator
    def get_part(self, undefined=""):
        """
        Args:
            undefined (optional): Argument, which will be returned if the
                      `part` record is not found.

        Returns:
            str: Which part of the book series is this record or `undefined` \
                 if `part` is not found.
        """
        return _undefined_pattern(
            "".join(self.get_subfields("245", "p")),
            lambda x: x.strip() == "",
            undefined
        )

    @remove_hairs_decorator
    def get_part_name(self, undefined=""):
        """
        Args:
            undefined (optional): Argument, which will be returned if the
                      `part_name` record is not found.

        Returns:
            str: Name of the part of the series. or `undefined` if `part_name`\
                 is not found.
        """
        return _undefined_pattern(
            "".join(self.get_subfields("245", "n")),
            lambda x: x.strip() == "",
            undefined
        )

    @remove_hairs_decorator
    def get_publisher(self, undefined=""):
        """
        Args:
            undefined (optional): Argument, which will be returned if the
                      `publisher` record is not found.

        Returns:
            str: Name of the publisher ("``Grada``" for example) or \
                 `undefined` if `publisher` is not found.
        """
        return _undefined_pattern(
            "".join(self.get_subfields("260", "b")),
            lambda x: x.strip() == "",
            undefined
        )

    @remove_hairs_decorator
    def get_pub_date(self, undefined=""):
        """
        Args:
            undefined (optional): Argument, which will be returned if the
                      `pub_date` record is not found.

        Returns:
            str: Date of publication (month and year usually) or `undefined` \
                 if `pub_date` is not found.
        """
        return _undefined_pattern(
            "".join(self.get_subfields("260", "c")),
            lambda x: x.strip() == "",
            undefined
        )

    @remove_hairs_decorator
    def get_pub_order(self, undefined=""):
        """
        Args:
            undefined (optional): Argument, which will be returned if the
                      `pub_order` record is not found.

        Returns:
            str: Information about order in which was the book published or \
                 `undefined` if `pub_order` is not found.
        """
        return _undefined_pattern(
            "".join(self.get_subfields("901", "f")),
            lambda x: x.strip() == "",
            undefined
        )

    @remove_hairs_decorator
    def get_pub_place(self, undefined=""):
        """
        Args:
            undefined (optional): Argument, which will be returned if the
                      `pub_place` record is not found.

        Returns:
            str: Name of city/country where the book was published or \
                 `undefined` if `pub_place` is not found.
        """
        return _undefined_pattern(
            "".join(self.get_subfields("260", "a")),
            lambda x: x.strip() == "",
            undefined
        )

    @remove_hairs_decorator
    def get_format(self, undefined=""):
        """
        Args:
            undefined (optional): Argument, which will be returned if the
                      `format` record is not found.

        Returns:
            str: Dimensions of the book ('``23 cm``' for example) or 
                `undefined` if `format` is not found.
        """
        return _undefined_pattern(
            "".join(self.get_subfields("300", "c")),
            lambda x: x.strip() == "",
            undefined
        )

    def get_authors(self):
        """
        Returns:
            list: Authors represented as :class:`.Person` objects.
        """
        authors = self._parse_persons("100", "a")
        authors += self._parse_persons("600", "a")
        authors += self._parse_persons("700", "a")
        authors += self._parse_persons("800", "a")

        return authors

    def get_corporations(self, roles=["dst"]):
        """
        Args:
            roles (list, optional): Specify which types of corporations you
                  need. Set to ``["any"]`` for any role, ``["dst"]`` for
                  distributors, etc..

        Note:
            See http://www.loc.gov/marc/relators/relaterm.html for details.

        Returns:
            list: :class:`.Corporation` objects specified by roles parameter.
        """
        corporations = self._parse_corporations("110", "a", roles)
        corporations += self._parse_corporations("610", "a", roles)
        corporations += self._parse_corporations("710", "a", roles)
        corporations += self._parse_corporations("810", "a", roles)

        return corporations

    def get_distributors(self):
        """
        Returns:
            list: Distributors represented as :class:`.Corporation` object.
        """
        return self.get_corporations(roles=["dst"])

    def _clean_isbn(self, isbn):
        """
        Clean ISBN from other information (binding).
        """
        return isbn.strip().split(" ", 1)[0]

    def get_invalid_ISBNs(self):
        """
        Get list of invalid ISBN (``020z``).

        Returns:
            list: List with INVALID ISBN strings.
        """
        return [
            self._clean_isbn(isbn)
            for isbn in self["020z"]
        ]

    def get_ISBNs(self):
        """
        Get list of VALID ISBN.

        Returns:
            list: List with *valid* ISBN strings.
        """
        invalid_isbns = self.get_invalid_ISBNs()

        valid_isbns = [
            self._clean_isbn(isbn)
            for isbn in self["020a"]
            if self._clean_isbn(isbn) not in invalid_isbns
        ]

        if valid_isbns:
            return valid_isbns

        # this is used sometimes in czech national library
        return [
            self._clean_isbn(isbn)
            for isbn in self["901i"]
        ]

    def _filter_binding(self, binding):
        """
        Filter binding from ISBN record. In MARC XML / OAI, the binding
        information is stored in same subrecord as ISBN.

        Example:
            ``<subfield code="a">80-251-0225-4 (brož.) :</subfield>`` ->
            ``brož.``.
        """
        binding = binding.strip().split(" ", 1)[-1]  # isolate bind. from ISBN
        binding = remove_hairs_fn(binding)  # remove special chars from binding

        return binding.split(":")[-1].strip()

    def get_binding(self):
        """
        Returns:
            list: Array of strings with bindings (``["brož."]``) or blank list.
        """
        # binding is stored after space in ISBN
        return [
            self._filter_binding(binding)
            for binding in self["020a"]
            if "-" in binding and " " in binding
        ]

    def get_originals(self):
        """
        Returns:
            list: List of strings with names of original books (names of books\
                  in original language, before translation).
        """
        return self.get_subfields("765", "t")

    def get_urls(self):
        """
        Content of field ``856u42``. Typically URL pointing to producers
        homepage.

        Returns:
            list: List of URLs defined by producer.
        """
        urls = self.get_subfields("856", "u", i1="4", i2="2")

        return map(lambda x: x.replace("&amp;", "&"), urls)

    def get_internal_urls(self):
        """
        URL's, which may point to edeposit, aleph, kramerius and so on.

        Fields ``856u40``, ``998a`` and ``URLu``.

        Returns:
            list: List of internal URLs. 
        """
        internal_urls = self.get_subfields("856", "u", i1="4", i2="0")
        internal_urls.extend(self.get_subfields("998", "a"))
        internal_urls.extend(self.get_subfields("URL", "u"))

        return map(lambda x: x.replace("&amp;", "&"), internal_urls)

    def get_pub_type(self):
        """
        Returns:
            PublicationType: :class:`.PublicationType` enum **value**.
        """
        INFO_CHAR_INDEX = 6
        SECOND_INFO_CHAR_I = 18

        if not len(self.leader) >= INFO_CHAR_INDEX + 1:
            return PublicationType.monographic

        info_char = self.leader[INFO_CHAR_INDEX]
        multipart_n = self.get_subfields("245", "n", exception=False)
        multipart_p = self.get_subfields("245", "p", exception=False)

        if info_char in "acd":
            return PublicationType.monographic
        elif info_char in "bis":
            return PublicationType.continuing
        elif info_char == "m" and (multipart_n or multipart_p):
            return PublicationType.multipart_monograph
        elif info_char == "m" and len(self.leader) >= SECOND_INFO_CHAR_I + 1:
            if self.leader[SECOND_INFO_CHAR_I] == "a":
                return PublicationType.multipart_monograph
            elif self.leader[SECOND_INFO_CHAR_I] == " ":
                return PublicationType.single_unit

        return PublicationType.monographic

    def is_monographic(self):
        """
        Returns:
            bool: True if the record is monographic.
        """
        return self.get_pub_type() == PublicationType.monographic

    def is_multi_mono(self):
        """
        Returns:
            bool: True if the record is multi_mono.
        """
        return self.get_pub_type() == PublicationType.multipart_monograph

    def is_continuing(self):
        """
        Returns:
            bool: True if the record is continuing.
        """
        return self.get_pub_type() == PublicationType.continuing

    def is_single_unit(self):
        """
        Returns:
            bool: True if the record is single unit.
        """
        return self.get_pub_type() == PublicationType.single_unit

    def __getitem__(self, item):
        """
        Query inteface shortcut for :meth:`.MARCXMLParser.get_ctl_fields` and
        :meth:`.MARCXMLParser.get_subfields`.

        First three characters are considered as `datafield`, next character
        as `subfield` and optionaly, two others as `i1` / `i2` parameters.

        Returned value is str/None in case of ``len(item)`` == 3 (ctl_fields)
        or list (or blank list) in case of ``len(item) >= 4``.

        Returns:
            list/str: See :meth:`.MARCXMLParser.get_subfields` for details.
        """
        if not isinstance(item, basestring):
            raise ValueError("Only str/unide indexes are supported!")

        if len(item) == 3:
            return self.controlfields.get(item, None)

        if len(item) < 3:
            raise ValueError(
                "Required at least 3 chars for field id."
            )

        if len(item) > 6:
            raise ValueError(
                "Too many indexing characters. use 4-6."
            )

        datafield = item[:3]
        subfield = item[3]

        i1 = None
        i2 = None
        if len(item) >= 5:
            i1 = item[4]
        if len(item) >= 6:
            i2 = item[5]

        return self.get_subfields(
            datafield=datafield,
            subfield=subfield,
            i1=i1,
            i2=i2,
            exception=False
        )
