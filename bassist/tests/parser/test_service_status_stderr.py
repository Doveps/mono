# Copyright (c) 2015 Kurt Yoder
# See the file LICENSE for copying permission.
import pytest

import bassist.parser.log_file.service_status_stderr

def test_bad_state(tmpdir):
    p = tmpdir.join('service_status.log')
    p.write(' [ + ]  console-setup')
    o = bassist.parser.log_file.service_status_stderr.ServiceStatusStderrLog(str(p))
    with pytest.raises(AssertionError):
        o.parse()
