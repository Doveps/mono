# Copyright (c) 2015 Kurt Yoder
# See the file LICENSE for copying permission.
import pytest

import bassist.parser.log_file.service_status_stdout

def test_bad_state(tmpdir):
    p = tmpdir.join('service_status.log')
    p.write(' [ ? ]  cron')
    o = bassist.parser.log_file.service_status_stdout.ServiceStatusStdoutLog(str(p))
    with pytest.raises(AssertionError):
        o.parse()
