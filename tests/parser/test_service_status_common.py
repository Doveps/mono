import pytest

import parser.log_file.service_status_common
import parser.log_file.service_status_stderr

good_service_status_text = ''' [ ? ]  console-setup
 [ ? ]  cryptdisks
'''

@pytest.fixture(scope='function')
def good_service_status(tmpdir):
    p = tmpdir.join('service_status.log')
    p.write(good_service_status_text)
    o = parser.log_file.service_status_stderr.ServiceStatusStderrLog(str(p))
    o.parse()
    return o

def test_count(good_service_status):
    assert len(good_service_status.services) is 2

def test_service_name(good_service_status):
    assert 'console-setup' in good_service_status.services

def test_good_service_state(good_service_status):
    assert good_service_status.services['console-setup'].upstart_init.state == '?'

def test_bad_field_count(tmpdir):
    p = tmpdir.join('service_status.log')
    p.write(' [ ? ]')
    o = parser.log_file.service_status_stderr.ServiceStatusStderrLog(str(p))
    with pytest.raises(AssertionError):
        o.parse()

def test_duplicates(tmpdir):
    p = tmpdir.join('service_status.log')
    p.write(' [ ? ]  svc1\n [ ? ]  svc2')
    o = parser.log_file.service_status_common.ServiceStatusCommonLog(str(p))
    with pytest.raises(AssertionError):
        o.parse()
