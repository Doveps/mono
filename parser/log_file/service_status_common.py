from . import common
from systems import service

class ServiceStatusCommonLog(common.Log):

    def parse(self):
        self.logger.debug('parsing')

        self.data = service.Services()
        self.name = 'services'

        with open(self.path, 'r') as f:
            for line in f.readlines():
                self.parse_line(line)

    def parse_line(self, line):
        assert hasattr(self, 'states')

        parts = line.split()
        assert len(parts) is 4

        state = parts[1]
        assert state in self.states

        name = parts[3]

        assert name not in self.data
        self.data[name] = service.Service(name)
        self.data[name].add_upstart_init(state)
