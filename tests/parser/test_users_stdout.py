import pytest

import bassist.parser.log_file.users_stdout

good_users_text = '''root:x:0:0:root:/root:/bin/bash
vagrant:x:900:900:vagrant,,,:/home/vagrant:/bin/bash
vboxadd:x:999:1::/var/run/vboxadd:/bin/false
'''

@pytest.fixture(scope='function')
def good_users(tmpdir):
    p = tmpdir.join('users.log')
    p.write(good_users_text)
    o = bassist.parser.log_file.users_stdout.UsersStdoutLog(str(p))
    o.parse()
    return o

def test_length(good_users):
    assert len(good_users.data) is 3

def test_user_name(good_users):
    assert 'root' in good_users.data

@pytest.fixture(scope='function')
def root_user(good_users):
    return good_users.data['root'].passwd

def test_good_user_password(root_user):
    assert root_user.password == 'x'

def test_good_user_uid(root_user):
    assert root_user.uid == '0'

def test_good_user_gid(root_user):
    assert root_user.gid == '0'

def test_good_user_description(root_user):
    assert root_user.description == 'root'

def test_good_user_path(root_user):
    assert root_user.path == '/root'

def test_good_user_shell(root_user):
    assert root_user.shell == '/bin/bash'

def test_empty_user_description(good_users):
    assert good_users.data['vboxadd'].passwd.description == ''

def test_bad_field_count(tmpdir):
    p = tmpdir.join('users.log')
    p.write('root:x:0:0')
    o = bassist.parser.log_file.users_stdout.UsersStdoutLog(str(p))
    with pytest.raises(AssertionError):
        o.parse()

def test_duplicates(tmpdir):
    p = tmpdir.join('users.log')
    p.write('root:x:0:0:root:/root:/bin/bash\nroot:x:0:0:root:/root:/bin/bash')
    o = bassist.parser.log_file.users_stdout.UsersStdoutLog(str(p))
    with pytest.raises(AssertionError):
        o.parse()
