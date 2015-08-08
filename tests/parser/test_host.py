import pytest
import os

import bassist.parser.host

@pytest.fixture(scope='function')
def dir_parser(tmpdir):
    parse_debs = tmpdir.join('find_debs_stdout.log')
    parse_debs.write('content')
    parse_junk = tmpdir.join('junk.log')
    parse_junk.write('content')
    parse_missing = tmpdir.join('find_nothing_stdout.log')
    parse_missing.write('content')
    ignore_dir = tmpdir.mkdir('sub')
    h = bassist.parser.host.Host(str(tmpdir))
    return h

def test_parser_count(dir_parser):
    assert len(dir_parser.parsers) is 1

def test_generated_parsers(dir_parser):
    assert type(dir_parser.parsers[0]) is bassist.parser.log_file.debs_stdout.DebsStdoutLog
