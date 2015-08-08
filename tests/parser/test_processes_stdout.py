import pytest

import bassist.parser.log_file.processes_stdout

good_processes_text = '''  PID  PPID   UID   GID CGROUP                      F  NI PRI TT       COMMAND
    1     0     0     0 -                           4   0  19 ?        /sbin/init
 1153     1     0     0 -                           4   0  19 ?        /usr/sbin/sshd -D
 1219  1153     0     0 2:name=systemd:/user/900.us 4   0  19 ?        sshd: vagrant [priv]
 1237  1219   900   900 2:name=systemd:/user/900.us 5   0  19 ?        sshd: vagrant@pts/0
 1238  1237   900   900 2:name=systemd:/user/900.us 0   0  19 pts/0    -bash
 1268  1238     0   900 2:name=systemd:/user/900.us 4   0  19 pts/0    sudo -s
 1269  1268     0     0 2:name=systemd:/user/900.us 4   0  19 pts/0    /bin/bash
 1505  1153     0     0 2:name=systemd:/user/900.us 4   0  19 ?        sshd: vagrant [priv]
 1528  1523   900   900 2:name=systemd:/user/900.us 0   0  19 pts/2    /bin/sh -c sudo -k && sudo -H -S -p "[sudo via ansible, key=auksipccnwlfnchfnplywdkzysxjlucb] password: " -u root /bin/sh -c 'echo SUDO-SUCCESS-auksipccnwlfnchfnplywdkzysxjlucb; LANG=C LC_CTYPE=C /usr/bin/python /home/vagrant/.ansible/tmp/ansible-tmp-1419040447.65-238273699227159/command; rm -rf /home/vagrant/.ansible/tmp/ansible-tmp-1419040447.65-238273699227159/ >/dev/null 2>&1'
 1530  1528     0   900 2:name=systemd:/user/900.us 4   0  19 pts/2    sudo -H -S -p [sudo via ansible, key=auksipccnwlfnchfnplywdkzysxjlucb] password:  -u root /bin/sh -c echo SUDO-SUCCESS-auksipccnwlfnchfnplywdkzysxjlucb; LANG=C LC_CTYPE=C /usr/bin/python /home/vagrant/.ansible/tmp/ansible-tmp-1419040447.65-238273699227159/command; rm -rf /home/vagrant/.ansible/tmp/ansible-tmp-1419040447.65-238273699227159/ >/dev/null 2>&1
 1531  1530     0     0 2:name=systemd:/user/900.us 4   0  19 pts/2    /bin/sh -c echo SUDO-SUCCESS-auksipccnwlfnchfnplywdkzysxjlucb; LANG=C LC_CTYPE=C /usr/bin/python /home/vagrant/.ansible/tmp/ansible-tmp-1419040447.65-238273699227159/command; rm -rf /home/vagrant/.ansible/tmp/ansible-tmp-1419040447.65-238273699227159/ >/dev/null 2>&1
 1532  1531     0     0 2:name=systemd:/user/900.us 4   0  19 pts/2    /usr/bin/python /home/vagrant/.ansible/tmp/ansible-tmp-1419040447.65-238273699227159/command
 1533  1532     0     0 2:name=systemd:/user/900.us 0   0  19 pts/2    /bin/sh -c ps -eo pid,ppid,uid,gid,cgroup,f,ni,pri,tty,args -www
 1534  1533     0     0 2:name=systemd:/user/900.us 4   0  19 pts/2    ps -eo pid,ppid,uid,gid,cgroup,f,ni,pri,tty,args -www
'''

@pytest.fixture(scope='function')
def good_processes(tmpdir):
    p = tmpdir.join('processes.log')
    p.write(good_processes_text)
    o = bassist.parser.log_file.processes_stdout.ProcessesStdoutLog(str(p))
    o.parse()
    return o

def test_count(good_processes):
    assert good_processes.process_count is 14

def test_recorded_count(good_processes):
    assert good_processes.recorded_process_count is 8

def test_process_name(good_processes):
    assert '/sbin/init' in good_processes.data

def test_no_ansible(good_processes):
    assert 'sudo -H -S -p [sudo via ansible, key=auksipccnwlfnchfnplywdkzysxjlucb] password:  -u root /bin/sh -c echo SUDO-SUCCESS-auksipccnwlfnchfnplywdkzysxjlucb; LANG=C LC_CTYPE=C /usr/bin/python /home/vagrant/.ansible/tmp/ansible-tmp-1419040447.65-238273699227159/command; rm -rf /home/vagrant/.ansible/tmp/ansible-tmp-1419040447.65-238273699227159/ >/dev/null 2>&1' \
            not in good_processes.data

def test_no_ps(good_processes):
    assert 'ps -eo pid,ppid,uid,gid,cgroup,f,ni,pri,tty,args -www' \
            not in good_processes.data

@pytest.fixture(scope='function')
def init_process(good_processes):
    return good_processes.data['/sbin/init'].instances[0]

def test_good_process_pid(init_process):
    assert init_process.pid == '1'

def test_good_process_ppid(init_process):
    assert init_process.ppid == '0'

def test_good_process_uid(init_process):
    assert init_process.uid == '0'

def test_good_process_gid(init_process):
    assert init_process.gid == '0'

def test_good_process_cgroup(init_process):
    assert init_process.cgroup == '-'

def test_good_process_flag(init_process):
    assert init_process.flag == '4'

def test_good_process_nice(init_process):
    assert init_process.nice == '0'

def test_good_process_priority(init_process):
    assert init_process.priority == '19'

def test_good_process_tty(init_process):
    assert init_process.tty == '?'

@pytest.fixture(scope='function')
def multi_instance_process(good_processes):
    return good_processes.data['sshd: vagrant [priv]'].instances

def test_has_two_instances(multi_instance_process):
    assert len(multi_instance_process) == 2

def test_instance1_pid(multi_instance_process):
    assert multi_instance_process[0].pid == '1219'

def test_instance2_pid(multi_instance_process):
    assert multi_instance_process[1].pid == '1505'

def test_bad_field_count(tmpdir):
    p = tmpdir.join('processes.log')
    p.write('junk\n  1  0  0  0')
    o = bassist.parser.log_file.processes_stdout.ProcessesStdoutLog(str(p))
    with pytest.raises(AssertionError):
        o.parse()
