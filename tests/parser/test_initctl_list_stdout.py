import pytest

import parser.log_file.initctl_list_stdout

good_initctl_list_text = '''mountnfs-bootclean.sh start/running
rsyslog start/running, process 456
mountall-net stop/waiting
network-interface-security (networking) start/running
'''

@pytest.fixture(scope='function')
def good_initctl_list(tmpdir):
    p = tmpdir.join('initctl_list.log')
    p.write(good_initctl_list_text)
    o = parser.log_file.initctl_list_stdout.InitctlListStdoutLog(str(p))
    o.parse()
    return o

def test_length(good_initctl_list):
    assert len(good_initctl_list.data) is 4

def test_service_name(good_initctl_list):
    assert 'mountall-net' in good_initctl_list.data

@pytest.fixture(scope='function')
def rsyslog_service(good_initctl_list):
    return good_initctl_list.data['rsyslog'].upstart

def test_good_service_wanted(rsyslog_service):
    assert rsyslog_service.wanted == 'start'

def test_good_service_state(rsyslog_service):
    assert rsyslog_service.state == 'running'

def test_good_service_pid(rsyslog_service):
    assert rsyslog_service.pid == '456'

def test_good_service_without_pid(good_initctl_list):
    m = good_initctl_list.data['mountnfs-bootclean.sh'].upstart
    assert m.pid is None

def test_good_multipart_named_service(good_initctl_list):
    assert 'network-interface-security (networking)' in \
            good_initctl_list.data

@pytest.fixture(scope='function')
def rsyslog_stopped_service(good_initctl_list):
    return good_initctl_list.data['mountall-net'].upstart

def test_stopped_service_wanted(rsyslog_stopped_service):
    assert rsyslog_stopped_service.wanted == 'stop'

def test_stopped_service_state(rsyslog_stopped_service):
    assert rsyslog_stopped_service.state == 'waiting'

def test_bad_extra_field_count(tmpdir):
    p = tmpdir.join('initctl_list.log')
    p.write('mountnfs-bootclean.sh start/running junk')
    o = parser.log_file.initctl_list_stdout.InitctlListStdoutLog(str(p))
    with pytest.raises(AssertionError):
        o.parse()

def test_bad_missing_pid(tmpdir):
    p = tmpdir.join('initctl_list.log')
    p.write('rsyslog start/running, process')
    o = parser.log_file.initctl_list_stdout.InitctlListStdoutLog(str(p))
    with pytest.raises(AssertionError):
        o.parse()

duplicates_text = '''rsyslog start/running, process 456
rsyslog start/running, process 457
'''

def test_duplicates(tmpdir):
    p = tmpdir.join('initctl_list.log')
    p.write(duplicates_text)
    o = parser.log_file.initctl_list_stdout.InitctlListStdoutLog(str(p))
    with pytest.raises(AssertionError):
        o.parse()
