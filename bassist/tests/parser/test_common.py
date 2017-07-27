# Copyright (c) 2015 Kurt Yoder
# See the file LICENSE for copying permission.
import pytest

import bassist.parser.log_file.common

@pytest.fixture(scope='function')
def common_log():
    return bassist.parser.log_file.common.Log('path/to/nonexistent')

def test_path(common_log):
    assert common_log.path == 'path/to/nonexistent'

def test_log(common_log):
    assert common_log.log == 'common'
