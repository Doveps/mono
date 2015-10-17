import pytest

import bassist.parser.log_file.files_stdout

good_files_text = '''     2    4 drwxr-xr-x  23 root     root         4096 Oct 19 17:23 /
123010    4 -rw-r--r--   1 root     root          110 Dec  6 20:22 /a/file
  6320    0 crw-rw-rw-   1 root     root              Nov  1 15:58 /a/charfile
 13744    0 lrwxrwxrwx   1 root     root            0 Dec  6 20:22 /a/symlink -> ../target
  7607    0 lrwxrwxrwx   1 root     root           15 Nov  1 15:58 /dev/ignored -> /proc/somewhere
131001    4 -rw-r--r--   1 root     root          834 Dec 18  2013 /a\ path\ with\ spaces
225014    4 drwx-wx--T   2 root     crontab      4096 Feb  9  2013 /var/spool/cron/crontabs
785394    4 -rw-r--r--   1 501      staff        1407 Jan  9  2012 /opt/httpd/man/man1/logresolve.1
224957    4 drwxrwsr-x   2 libuuid  libuuid      4096 Apr 16  2014 /var/lib/libuuid
225018    4 drwxrwxrwt   2 root     root         4096 Oct 21  2014 /var/tmp
104664   44 -rwsr-xr-x   1 root     root        44168 May  7  2014 /bin/ping
'''

@pytest.fixture(scope='function')
def good_files(tmpdir):
    p = tmpdir.join('files.log')
    p.write(good_files_text)
    o = bassist.parser.log_file.files_stdout.FilesStdoutLog(str(p))
    o.parse()
    return o

def test_length(good_files):
    assert len(good_files.data) is 10

def test_in_path(good_files):
    assert '/' in good_files.data

def test_dev_not_in_path(good_files):
    assert '/dev/stderr' not in good_files.data

@pytest.fixture(scope='function')
def slash(good_files):
    return good_files.data['/']

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
    assert good_files.data['/a/symlink'].link_target == '../target'

def test_char_no_size(good_files):
    assert good_files.data['/a/charfile'].size is None

extra_space_text = '''     2    4  -rwxr-xr-x  23 root     root         4096 Oct 19 17:23 /why so spacey?
'''

def test_broken_parse(tmpdir):
    p = tmpdir.join('files.log')
    p.write(extra_space_text)
    o = bassist.parser.log_file.files_stdout.FilesStdoutLog(str(p))
    with pytest.raises(bassist.parser.log_file.files_stdout.ParsedFileException):
        o.parse()

missing_size_text = '''123010    4 -rw-r--r--   1 root     root              Dec  6 20:22 /a/file
'''

def test_missing_size(tmpdir):
    p = tmpdir.join('files.log')
    p.write(missing_size_text)
    o = bassist.parser.log_file.files_stdout.FilesStdoutLog(str(p))
    with pytest.raises(bassist.parser.log_file.files_stdout.ParsedFileException):
        o.parse()

char_size_text = ''' 6320    0 crw-rw-rw-   1 root     root          123 Nov  1 15:58 /a/charfile
'''

def test_extra_size(tmpdir):
    p = tmpdir.join('files.log')
    p.write(char_size_text)
    o = bassist.parser.log_file.files_stdout.FilesStdoutLog(str(p))
    with pytest.raises(bassist.parser.log_file.files_stdout.ParsedFileException):
        o.parse()

missing_symlink_perms_text = ''' 13744    0 -rwxrwxrwx   1 root     root            0 Dec  6 20:22 /a/symlink -> ../target
'''

def test_missing_symlink_perms(tmpdir):
    p = tmpdir.join('files.log')
    p.write(missing_symlink_perms_text)
    o = bassist.parser.log_file.files_stdout.FilesStdoutLog(str(p))
    with pytest.raises(bassist.parser.log_file.files_stdout.ParsedFileException):
        o.parse()

missing_symlink_path_text = ''' 13744    0 lrwxrwxrwx   1 root     root            0 Dec  6 20:22 /a/symlink
'''

def test_missing_symlink_path(tmpdir):
    p = tmpdir.join('files.log')
    p.write(missing_symlink_path_text)
    o = bassist.parser.log_file.files_stdout.FilesStdoutLog(str(p))
    with pytest.raises(bassist.parser.log_file.files_stdout.ParsedFileException):
        o.parse()

duplicates_text = '''     2    4 drwxr-xr-x  23 root     root         4096 Oct 19 17:23 /
     3    4 drwxr-xr-x  23 root     root         4096 Oct 19 17:23 /
'''

def test_duplicates(tmpdir):
    p = tmpdir.join('files.log')
    p.write(duplicates_text)
    o = bassist.parser.log_file.files_stdout.FilesStdoutLog(str(p))
    with pytest.raises(AssertionError):
        o.parse()
