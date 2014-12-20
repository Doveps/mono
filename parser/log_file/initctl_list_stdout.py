import re

from . import common
from systems import service

class InitctlListStdoutLog(common.Log):
    # tty5 start/running, process 856
    # passwd stop/waiting
    # network-interface-security (networking) start/running
    line_re = re.compile('^(\S+) (?:(\S+) )?(\S+)/(\S+)(?:, process (\d+))?$')

    def parse(self):
        self.logger.debug('parsing')

        self.services = {}
        with open(self.path, 'r') as f:
            for line in f.readlines():
                self.parse_line(line)

    def parse_line(self, line):
        matches = self.line_re.match(line)
        assert matches
        (name, instance, wanted, state, pid) = matches.groups()
        if instance is not None:
            name = name + ' ' + instance

        assert not self.services.has_key(name)
        self.services[name] = service.Service(name)
        self.services[name].add_upstart(wanted, state, pid)

    def record(self, flavor):
        self.logger.debug('recording %d upstart services',len(self.services))
        flavor.record('services', self.services)
