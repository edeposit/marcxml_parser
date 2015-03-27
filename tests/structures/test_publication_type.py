#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from marcxml_parser import PublicationType


# Tests =======================================================================
def test_publication_type():
    assert hasattr(PublicationType, "monographic")
    assert hasattr(PublicationType, "continuing")
    assert hasattr(PublicationType, "multipart_monograph")
    assert hasattr(PublicationType, "single_unit")
