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
    Highlevel abstractions
    ++++++++++++++++++++++

    Getters:
        - :meth:`get_name`
        - :meth:`get_subname`
        - :meth:`get_price`
        - :meth:`get_part`
        - :meth:`get_part_name`
        - :meth:`get_publisher`
        - :meth:`get_pub_date`
        - :meth:`get_pub_order`
        - :meth:`get_pub_place`
        - :meth:`get_format`
        - :meth:`get_authors`
        - :meth:`get_corporations`
        - :meth:`get_distributors`
        - :meth:`get_ISBNs`
        - :meth:`get_binding`
        - :meth:`get_originals`
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
            KeyError: when name is not specified.
        """
        return "".join(self.get_subfields("245", "a"))

    @remove_hairs_decorator
    def get_subname(self, undefined=""):
        """
        Args:
            undefined (optional): returned if sub-name record is not found.

        Returns:
            str: Sub-name of the book or `undefined` if name is not defined.
        """
        return _undefined_pattern(
            "".join(self.get_subfields("245", "b")),
            lambda x: x.strip() == "",
            undefined
        )

    @remove_hairs_decorator
    def get_price(self, undefined=""):
        """
        Returns:
            str: Price of the book (with currency).
        """
        return _undefined_pattern(
            "".join(self.get_subfields("020", "c")),
            lambda x: x.strip() == "",
            undefined
        )

    @remove_hairs_decorator
    def get_part(self, undefined=""):
        """
        Returns:
            str: Which part of the book series is this record.
        """
        return _undefined_pattern(
            "".join(self.get_subfields("245", "p")),
            lambda x: x.strip() == "",
            undefined
        )

    @remove_hairs_decorator
    def get_part_name(self, undefined=""):
        """
        Returns:
            str: Name of the part of the series.
        """
        return _undefined_pattern(
            "".join(self.get_subfields("245", "n")),
            lambda x: x.strip() == "",
            undefined
        )

    @remove_hairs_decorator
    def get_publisher(self, undefined=""):
        """
        Returns:
            str: name of the publisher ("``Grada``" for example)
        """
        return _undefined_pattern(
            "".join(self.get_subfields("260", "b")),
            lambda x: x.strip() == "",
            undefined
        )

    @remove_hairs_decorator
    def get_pub_date(self, undefined=""):
        """
        Returns:
            str: date of publication (month and year usually)
        """
        return _undefined_pattern(
            "".join(self.get_subfields("260", "c")),
            lambda x: x.strip() == "",
            undefined
        )

    @remove_hairs_decorator
    def get_pub_order(self, undefined=""):
        """
        Returns:
            str: information about order in which was the book published
        """
        return _undefined_pattern(
            "".join(self.get_subfields("901", "f")),
            lambda x: x.strip() == "",
            undefined
        )

    @remove_hairs_decorator
    def get_pub_place(self, undefined=""):
        """
        Returns:
            str: name of city/country where the book was published
        """
        return _undefined_pattern(
            "".join(self.get_subfields("260", "a")),
            lambda x: x.strip() == "",
            undefined
        )

    @remove_hairs_decorator
    def get_format(self, undefined=""):
        """_p  _p     Returns:
            str: dimensions of the book ('``23 cm``' for example)
        """
        return _undefined_pattern(
            "".join(self.get_subfields("300", "c")),
            lambda x: x.strip() == "",
            undefined
        )

    def get_authors(self):
        """
        Returns:
            list: authors represented as Person objects
        """
        authors = self._parse_persons("100", "a")
        authors += self._parse_persons("600", "a")
        authors += self._parse_persons("700", "a")
        authors += self._parse_persons("800", "a")

        return authors

    def get_corporations(self, roles=["dst"]):
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
        corporations = self._parse_corporations("110", "a", roles)
        corporations += self._parse_corporations("610", "a", roles)
        corporations += self._parse_corporations("710", "a", roles)
        corporations += self._parse_corporations("810", "a", roles)

        return corporations

    def get_distributors(self):
        """
        Returns:
            list: distributors represented as :class:`Corporation` object
        """
        return self.get_corporations(roles=["dst"])

    def get_ISBNs(self):
        """
        Returns:
            list: array with ISBN strings
        """

        if self.get_subfields("020", "a"):
            return map(
                lambda ISBN: ISBN.strip().split(" ", 1)[0],
                self.get_subfields("020", "a", exception=True)
            )

        if self.get_subfields("901", "i"):
            return map(
                lambda ISBN: ISBN.strip().split(" ", 1)[0],
                self.get_subfields("901", "i", exception=True)
            )

        return []

    def get_binding(self):
        """
        Returns:
            list: array of strings with bindings (``["brož."]``) or blank list
        """
        if self.get_subfields("020", "a"):
            return map(
                lambda x: remove_hairs_fn(
                    x.strip().split(" ", 1)[1]
                ),
                filter(
                    lambda x: "-" in x and " " in x,
                    self.get_subfields("020", "a", exception=True)
                )
            )

        return []

    def get_originals(self):
        """
        Returns:
            list: List of strings with original names.
        """
        return self.get_subfields("765", "t")

    def get_urls(self):
        """
        Returns:
            list: List of urls defined by producer (typically one pointing to \
                  producers homepage).
        """
        urls = self.get_subfields("856", "u", i1="4", i2="2")

        return map(lambda x: x.replace("&amp;", "&"), urls)

    def get_internal_urls(self):
        """
        Returns:
            list: List of internal urls. Url's may point to edeposit, aleph, \
                  kramerius and so on.
        """
        internal_urls = self.get_subfields("856", "u", i1="4", i2="0")
        internal_urls.extend(
            self.get_subfields("998", "a")
        )

        return map(lambda x: x.replace("&amp;", "&"), internal_urls)
