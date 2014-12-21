import pytest

import parser.log_file.debs_stdout

good_debs_text = '''Desired=Unknown/Install/Remove/Purge/Hold
| Status=Not/Inst/Conf-files/Unpacked/halF-conf/Half-inst/trig-aWait/Trig-pend
|/ Err?=(none)/Reinst-required (Status,Err: uppercase=bad)
||/ Name                                Version                       Architecture Description
+++-===================================-=============================-============-===================================================================
ii  accountsservice                     0.6.35-0ubuntu7               amd64        query and manipulate user account information
'''

@pytest.fixture(scope='function')
def good_debs(tmpdir):
    p = tmpdir.join('debs.log')
    p.write(good_debs_text)
    o = parser.log_file.debs_stdout.DebsStdoutLog(str(p))
    o.parse()
    return o

def test_length(good_debs):
    assert len(good_debs.packages) is 1

def test_package_name(good_debs):
    assert 'accountsservice' in good_debs.packages

@pytest.fixture(scope='function')
def good_deb(good_debs):
    return good_debs.packages['accountsservice'].deb

def test_package_deb(good_deb):
    assert good_deb is not None

def test_package_deb_stat(good_deb):
    assert good_deb.stat == 'ii'

def test_package_deb_vers(good_deb):
    assert good_deb.vers == '0.6.35-0ubuntu7'

def test_package_deb_arch(good_deb):
    assert good_deb.arch == 'amd64'
