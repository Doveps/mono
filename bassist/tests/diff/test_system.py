# Copyright (c) 2015 Kurt Yoder
# See the file LICENSE for copying permission.
import pytest

import bassist.diff.system

@pytest.fixture(scope='function')
def type_missing():
    return bassist.diff.system.System({})

def test_missing_type_different(type_missing):
    assert type_missing.different() is True

def test_missing_type_matches(type_missing):
    assert type_missing.matches['type'] is False

@pytest.fixture(scope='function')
def type_mismatch():
    return bassist.diff.system.System({}, 1)

def test_type_mismatch_different(type_mismatch):
    assert type_mismatch.different() is True

def test_type_mismatch_matches(type_mismatch):
    assert type_mismatch.matches['type'] is False

@pytest.fixture(scope='function')
def only_in():
    return bassist.diff.system.System({'a': 1}, {'b': 1})

def test_only_in_different(only_in):
    assert only_in.different() is True

def test_only_in_1_matches(only_in):
    assert only_in.matches['data1'] is False

def test_only_in_2_matches(only_in):
    assert only_in.matches['data2'] is False

@pytest.fixture(scope='function')
def both_match():
    return bassist.diff.system.System({'a': 1}, {'a': 1})

def test_both_match_same(both_match):
    assert both_match.different() is False

def test_both_match_1_matches(both_match):
    assert both_match.matches['data1'] is True

def test_both_match_2_matches(both_match):
    assert both_match.matches['data2'] is True
