#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest

from marcxml_parser.tools import resorted


# Tests =======================================================================
def test_resorted():
    assert resorted(["b", "1", "a"]) == ["a", "b", "1"]


def test_resorted_blank_argument():
    assert resorted([]) == []


def test_resorted_one_argument():
    assert resorted(["a"]) == ["a"]


def test_resorted_one_string_argument():
    assert resorted("a") == ["a"]


def test_resorted_string_argument():
    assert resorted("1bc3a") == list("abc13")


def test_resorted_string_array():
    assert resorted(["world", "hello", "3a"]) == ["hello", "world", "3a"]


def test_resorted_number_arguments():
    assert resorted(["2", "1"]) == list("12")


def test_resorted_blank_string_argument():
    assert resorted(["a", "", "1"]) == ["a", "", "1"]
