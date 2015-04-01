#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from enum import Enum


# Functions & classes =========================================================
class PublicationType(Enum):
    """
    Enum used to decide type of the publication.
    """
    _cnt = (x for x in range(100))

    monographic = next(_cnt)  #:
    continuing = next(_cnt)  #:
    multipart_monograph = next(_cnt)  #:
    single_unit = next(_cnt)  #:
