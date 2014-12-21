import pytest

import parser.log_file.files_stdout

good_files_text = '''     2    4 drwxr-xr-x  23 root     root         4096 Oct 19 17:23 /
123010    4 -rw-r--r--   1 root     root          110 Dec  6 20:22 /a/file
  6320    0 crw-rw-rw-   1 root     root              Nov  1 15:58 /a/charfile
 13744    0 lrwxrwxrwx   1 root     root            0 Dec  6 20:22 /a/symlink -> ../target
  7607    0 lrwxrwxrwx   1 root     root           15 Nov  1 15:58 /dev/ignored -> /proc/somewhere
131001    4 -rw-r--r--   1 root     root          834 Dec 18  2013 /a\ path\ with\ spaces
'''

@pytest.fixture(scope='function')
def good_files(tmpdir):
    p = tmpdir.join('files.log')
    p.write(good_files_text)
    o = parser.log_file.files_stdout.FilesStdoutLog(str(p))
    o.parse()
    return o

def test_length(good_files):
    assert len(good_files.paths) is 5

def test_in_path(good_files):
    assert '/' in good_files.paths

def test_dev_not_in_path(good_files):
    assert '/dev/stderr' not in good_files.paths

@pytest.fixture(scope='function')
def slash(good_files):
    return good_files.paths['/']

def test_slash_path(slash):
    assert slash.path == '/'

def test_slash_inode(slash):
    assert slash.inode == '2'

def test_slash_blocks(slash):
    assert slash.blocks == '4'

def test_slash_perms(slash):
    assert slash.perms == 'drwxr-xr-x'

def test_slash_link_count(slash):
    assert slash.link_count == '23'

def test_slash_owner(slash):
    assert slash.owner == 'root'

def test_slash_group(slash):
    assert slash.group == 'root'

def test_slash_size(slash):
    assert slash.size == '4096'

def test_slash_month(slash):
    assert slash.month == 'Oct'

def test_slash_day(slash):
    assert slash.day == '19'

def test_slash_more_time(slash):
    assert slash.more_time == '17:23'

def test_slash_no_target(slash):
    assert slash.link_target is None

def test_link_target(good_files):
    assert good_files.paths['/a/symlink'].link_target == '../target'

def test_char_no_size(good_files):
    assert good_files.paths['/a/charfile'].size is None

broken_files_text = '''     2    4 -rwxr-xr-x  23 root     root         4096 Oct 19 17:23 /why so spacey?
'''

def test_broken_path(tmpdir):
    p = tmpdir.join('files.log')
    p.write(broken_files_text)
    o = parser.log_file.files_stdout.FilesStdoutLog(str(p))
    with pytest.raises(parser.log_file.files_stdout.ParsedFileException):
        o.parse()
