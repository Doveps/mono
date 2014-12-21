from . import common
from systems import deb

class DebsStdoutLog(common.Log):

    def parse(self):
        self.logger.debug('parsing')

        self.debs = deb.Debs()
        with open(self.path, 'r') as f:
            for line_number, line in enumerate(f.readlines()):
                # ignore header lines
                if line_number < 5: continue

                parts = line.split()
                (stat, name, vers, arch) = parts[0:4]
                self.debs[name] = deb.Deb(stat, vers, arch)

    def record(self, flavor):
        self.logger.debug('recording %d packages',len(self.debs))
        flavor.record('debs', self.debs)
