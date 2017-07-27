# Copyright (c) 2015 Kurt Yoder
# See the file LICENSE for copying permission.
import pytest

import bassist.diff.flavor
import bassist.flavor.obj

@pytest.fixture(scope='function')
def type_missing():
    return bassist.diff.flavor.Flavor({})

def test_missing_type_different(type_missing):
    assert type_missing.different() is True

def test_missing_type_matches(type_missing):
    assert type_missing.matches['type'] is False

@pytest.fixture(scope='function')
def type_mismatch():
    return bassist.diff.flavor.Flavor({}, 1)

def test_type_mismatch_different(type_mismatch):
    assert type_mismatch.different() is True

def test_type_mismatch_matches(type_mismatch):
    assert type_mismatch.matches['type'] is False

@pytest.fixture(scope='function')
def only_in():
    flavor1 = bassist.flavor.obj.Obj()
    flavor1.record_system('a', {})
    flavor2 = bassist.flavor.obj.Obj()
    flavor2.record_system('b', {})
    return bassist.diff.flavor.Flavor(flavor1, flavor2)

def test_only_in_different(only_in):
    assert only_in.different() is True

def test_only_in_1_matches(only_in):
    assert only_in.matches['flavor1'] is False

def test_only_in_2_matches(only_in):
    assert only_in.matches['flavor2'] is False

@pytest.fixture(scope='function')
def both_match():
    flavor1 = bassist.flavor.obj.Obj()
    flavor1.record_system('a', {})
    flavor2 = bassist.flavor.obj.Obj()
    flavor2.record_system('a', {})
    return bassist.diff.flavor.Flavor(flavor1, flavor2)

def test_both_match_same(both_match):
    assert both_match.different() is False

def test_both_match_1_matches(both_match):
    assert both_match.matches['flavor1'] is True

def test_both_match_2_matches(both_match):
    assert both_match.matches['flavor2'] is True

@pytest.fixture(scope='function')
def service_mismatch():
    flavor1 = bassist.flavor.obj.Obj()
    flavor1.record_system('a', {'a': 1})
    flavor2 = bassist.flavor.obj.Obj()
    flavor2.record_system('a', {'b': 1})
    return bassist.diff.flavor.Flavor(flavor1, flavor2)

def test_service_mismatch_different(service_mismatch):
    assert service_mismatch.different() is True

def test_service_mismatch_systems(service_mismatch):
    assert service_mismatch.matches['systems'] is False

def test_service_mismatch_system_diffs(service_mismatch):
    assert type(service_mismatch.system_diffs['a']) is \
            bassist.diff.system.System
