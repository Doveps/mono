import re

from . import common
from systems import process

class ProcessesStdoutLog(common.Log):
    # .ansible/tmp/ansible-tmp-1417897614.23-199064374829668/
    observer_timestamp_re = re.compile('\.ansible/tmp/ansible-tmp-\d+.\d+-\d+/')
    # /bin/sh -c ps -eo pid,ppid,uid,gid,cgroup,f,ni,pri,tty,args -www
    observer_pslist_re = re.compile('^(/bin/sh -c )?ps -eo ([a-z]{1,6},){9,}[a-z]{1,6} -www$')

    def parse(self):
        self.logger.debug('parsing')

        self.processes = process.Processes()

        # since processes can overlap, resulting in >1 process in a
        # self.processes key, manually keep track of the count:
        self.process_count = 0

        with open(self.path, 'r') as f:
            for line_number, line in enumerate(f.readlines()):
                # ignore header lines
                if line_number < 1: continue

                self.process_count += 1
                self.parse_line(line)

    def parse_line(self, line):
        parts = line.split()

        command = ' '.join(parts[9:])

        # ignore "observer effect" commands, that is: Ansible
        if self.observer_timestamp_re.search(command):
            return
        if self.observer_pslist_re.search(command):
            return

        if command not in self.processes:
            self.processes[command] = process.Process(command)

        self.processes[command].add(parts[0:9])

    def record(self, flavor):
        self.logger.debug('recording %d processes',self.process_count)
        flavor.record('processes', self.processes)
