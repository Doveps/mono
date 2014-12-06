from . import common
from systems import process

class ProcessesStdoutLog(common.Log):

    def parse(self):
        self.logger.debug('parsing')

        self.processes = {}

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

        if not self.processes.has_key(command):
            self.processes[command] = process.Process(command)

        self.processes[command].add(parts[0:9])

    def record(self, flavor):
        self.logger.debug('recording %d processes',self.process_count)
        flavor.record('processes', self.processes)
