#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from collections import namedtuple


# Functions & classes =========================================================
class Corporation(namedtuple("Corporation", ["name", "place", "date"])):
    """
    Informations about corporations (fields 110, 610, 710, 810).

    Attributes:
        name (str):  Name of the corporation.
        place (str): Location of the corporation/action.
        date (str):  Date in unspecified format.
    """
