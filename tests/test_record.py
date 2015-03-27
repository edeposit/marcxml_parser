#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest


# Tests =======================================================================
def test_record_class():
    from marcxml_parser import MARCXMLRecord

    MARCXMLRecord()
