from . import common
from systems import service

class ServiceStatusStderrLog(common.Log):

    def parse(self):
        self.logger.debug('parsing')

        self.services = service.Services()
        with open(self.path, 'r') as f:
            for line in f.readlines():
                self.parse_line(line)

    def parse_line(self, line):
        #  [ ? ]  console-setup
        parts = line.split()
        assert len(parts) is 4

        state = parts[1]
        assert state is '?'

        name = parts[3]

        assert name not in self.services
        self.services[name] = service.Service(name)
        self.services[name].add_upstart_init(state)

    def record(self, flavor):
        self.logger.debug('recording %d services',len(self.services))
        flavor.record('services', self.services)
