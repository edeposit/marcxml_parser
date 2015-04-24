#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os.path

import pytest

from marcxml_parser import MARCXMLRecord
from marcxml_parser import record_iterator

from test_serializer import DATA_DIR


# Fixtures ====================================================================
@pytest.fixture
def multi_file():
    with open(os.path.join(DATA_DIR, "multirecord.xml")) as f:
        return f.read()


# Tests =======================================================================
def test_record_class():
    MARCXMLRecord()


def test_record_iterator(multi_file):
    records = record_iterator(multi_file)

    assert len(list(records)) == 3

    for record in records:
        assert isinstance(record, MARCXMLRecord)
