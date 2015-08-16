from . import common
from ...systems import process

class ProcessesStdoutLog(common.Log):

    def parse(self):
        self.logger.debug('parsing')

        self.data = process.Processes()
        self.name = 'processes'

        # since processes can overlap, resulting in >1 process in a
        # self.processes key, manually keep track of the count:
        self.process_count = 0
        self.recorded_process_count = 0

        with open(self.path, 'r') as f:
            for line_number, line in enumerate(f.readlines()):
                # ignore header lines
                if line_number < 1: continue

                self.process_count += 1
                self.parse_line(line)

    def parse_line(self, line):
        parts = line.split()

        assert len(parts) >= 10

        command = ' '.join(parts[9:])

        # ignore "observer effect" commands, that is: Ansible
        if common.Observer.timestamp_re.search(command):
            return
        if common.Observer.pslist_re.search(command):
            return

        self.recorded_process_count += 1
        if command not in self.data:
            self.data[command] = process.Process(command)

        self.data[command].add(parts[0:9])
