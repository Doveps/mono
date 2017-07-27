# Copyright (c) 2015 Kurt Yoder
# See the file LICENSE for copying permission.
import re

from . import common
from ...systems import service

class InitctlListStdoutLog(common.Log):
    # tty5 start/running, process 856
    # passwd stop/waiting
    # network-interface-security (networking) start/running
    line_re = re.compile('^(\S+) (?:(\S+) )?(\S+)/(\S+)(?:, process (\d+))?$')

    #    pre-stop process 928
    ignored_re = re.compile('^\t\S+ \S+ \d+$')

    def parse(self):
        self.logger.debug('parsing')

        self.data = service.Services()
        self.name = 'services'

        with open(self.path, 'r') as f:
            for line in f.readlines():
                self.parse_line(line)

    def parse_line(self, line):
        if InitctlListStdoutLog.ignored_re.match(line):
            self.logger.debug('ignoring: %s',line)
            return

        matches = InitctlListStdoutLog.line_re.match(line)
        assert matches
        (name, instance, wanted, state, pid) = matches.groups()
        if instance is not None:
            name = name + ' ' + instance

        assert name not in self.data
        self.data[name] = service.Service(name)
        self.data[name].add_upstart(wanted, state, pid)
