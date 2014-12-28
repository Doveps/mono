import pytest

import parser.log_file.service_status_stderr

def test_bad_state(tmpdir):
    p = tmpdir.join('service_status.log')
    p.write(' [ + ]  console-setup')
    o = parser.log_file.service_status_stderr.ServiceStatusStderrLog(str(p))
    with pytest.raises(AssertionError):
        o.parse()
