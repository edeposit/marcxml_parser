#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest


# Tests =======================================================================
def test_module_imports():
    from marcxml_parser import Person
    from marcxml_parser import Corporation
    from marcxml_parser import MARCSubrecord
    from marcxml_parser import PublicationType

    from marcxml_parser import MARCXMLRecord
    from marcxml_parser import record_iterator


def test_module_imports_hidden():
    """
    Implementation details should be hidden.
    """
    with pytest.raises(ImportError):
        from marcxml_parser import MARCXMLParser
        from marcxml_parser import MARCXMLSerializer
        from marcxml_parser import MARCXMLQuery
