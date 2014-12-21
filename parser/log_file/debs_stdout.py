from . import common
from systems import package

class DebsStdoutLog(common.Log):

    def parse(self):
        self.logger.debug('parsing')

        self.packages = package.Packages()
        with open(self.path, 'r') as f:
            for line_number, line in enumerate(f.readlines()):
                # ignore header lines
                if line_number < 5: continue

                parts = line.split()

                assert len(parts) > 4
                (stat, name, vers, arch) = parts[0:4]
                self.packages[name] = package.Package()
                self.packages[name].add_deb(stat, vers, arch)

    def record(self, flavor):
        self.logger.debug('recording %d packages',len(self.packages))
        flavor.record('packages', self.packages)
