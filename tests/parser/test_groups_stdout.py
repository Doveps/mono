import pytest

import bassist.parser.log_file.groups_stdout

good_groups_text = '''root:x:0:
adm:x:4:syslog,vagrant
cdrom:x:24:vagrant
'''

@pytest.fixture(scope='function')
def good_groups(tmpdir):
    p = tmpdir.join('groups.log')
    p.write(good_groups_text)
    o = bassist.parser.log_file.groups_stdout.GroupsStdoutLog(str(p))
    o.parse()
    return o

def test_length(good_groups):
    assert len(good_groups.data) is 3

def test_group_name(good_groups):
    assert 'root' in good_groups.data

@pytest.fixture(scope='function')
def adm_group(good_groups):
    return good_groups.data['adm']

def test_good_group_users(adm_group):
    assert adm_group.users == ['syslog', 'vagrant']

def test_good_group_password(adm_group):
    assert adm_group.password == 'x'

def test_good_group_gid(adm_group):
    assert adm_group.gid == '4'

def test_empty_group_users(good_groups):
    assert good_groups.data['root'].users is None

bad_field_count_text = '''cdrom:x:24
'''

def test_bad_field_count(tmpdir):
    p = tmpdir.join('groups.log')
    p.write(bad_field_count_text)
    o = bassist.parser.log_file.groups_stdout.GroupsStdoutLog(str(p))
    with pytest.raises(AssertionError):
        o.parse()

duplicates_text = '''root:x:0:
root:x:1:
'''

def test_duplicates(tmpdir):
    p = tmpdir.join('groups.log')
    p.write(duplicates_text)
    o = bassist.parser.log_file.groups_stdout.GroupsStdoutLog(str(p))
    with pytest.raises(AssertionError):
        o.parse()
