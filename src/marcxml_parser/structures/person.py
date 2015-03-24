#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from collections import namedtuple


# Functions & classes =========================================================
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
