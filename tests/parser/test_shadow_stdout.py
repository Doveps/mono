import pytest

import lib.parser.log_file.shadow_stdout

good_shadow_text = '''root:!:16179:0:99999:7:::
vagrant:$6$5M8f9rEy$nFWJvEnn2KFQwFsm6oRMyxva3mVixbyxZIE3cYTJ.ARFMt6Nq6gsnqScUkZ/slZ8tQzhZovx1M2CnmSsF71JA1:16179:0:99999:7:::
vboxadd:!:16179::::::
'''

@pytest.fixture(scope='function')
def good_shadow(tmpdir):
    p = tmpdir.join('shadow.log')
    p.write(good_shadow_text)
    o = lib.parser.log_file.shadow_stdout.ShadowStdoutLog(str(p))
    o.parse()
    return o

def test_length(good_shadow):
    assert len(good_shadow.data) is 3

def test_user_name(good_shadow):
    assert 'root' in good_shadow.data

@pytest.fixture(scope='function')
def root_user(good_shadow):
    return good_shadow.data['root'].shadow

def test_good_user_password(root_user):
    assert root_user.password == '!'

def test_good_user_lastchanged(root_user):
    assert root_user.lastchanged == '16179'

def test_good_user_minimum(root_user):
    assert root_user.minimum == '0'

def test_good_user_maximum(root_user):
    assert root_user.maximum == '99999'

def test_good_user_warn(root_user):
    assert root_user.warn == '7'

def test_good_user_inactive(root_user):
    assert root_user.inactive == ''

def test_good_user_expire(root_user):
    assert root_user.expire == ''

def test_good_user_reserved(root_user):
    assert root_user.reserved == ''

def test_bad_field_count(tmpdir):
    p = tmpdir.join('shadow.log')
    p.write('root:!:16179:0')
    o = lib.parser.log_file.shadow_stdout.ShadowStdoutLog(str(p))
    with pytest.raises(AssertionError):
        o.parse()

def test_duplicates(tmpdir):
    p = tmpdir.join('shadow.log')
    p.write('root:!:16179:0:99999:7:::\nroot:!:16179:0:99999:7:::')
    o = lib.parser.log_file.shadow_stdout.ShadowStdoutLog(str(p))
    with pytest.raises(AssertionError):
        o.parse()
