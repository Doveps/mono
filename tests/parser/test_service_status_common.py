import pytest

import bassist.parser.log_file.service_status_common
import bassist.parser.log_file.service_status_stderr

good_service_status_text = ''' [ ? ]  console-setup
 [ ? ]  cryptdisks
'''

@pytest.fixture(scope='function')
def good_service_status(tmpdir):
    p = tmpdir.join('service_status.log')
    p.write(good_service_status_text)
    o = bassist.parser.log_file.service_status_stderr.ServiceStatusStderrLog(str(p))
    o.parse()
    return o

def test_count(good_service_status):
    assert len(good_service_status.data) is 2

def test_service_name(good_service_status):
    assert 'console-setup' in good_service_status.data

def test_good_service_state(good_service_status):
    assert good_service_status.data['console-setup'].upstart_init.state == '?'

def test_bad_field_count(tmpdir):
    p = tmpdir.join('service_status.log')
    p.write(' [ ? ]')
    o = bassist.parser.log_file.service_status_stderr.ServiceStatusStderrLog(str(p))
    with pytest.raises(AssertionError):
        o.parse()

def test_duplicates(tmpdir):
    p = tmpdir.join('service_status.log')
    p.write(' [ ? ]  svc1\n [ ? ]  svc2')
    o = bassist.parser.log_file.service_status_common.ServiceStatusCommonLog(str(p))
    with pytest.raises(AssertionError):
        o.parse()
