from . import common

class Deb(object):
    def __init__(self, stat, vers, arch):
        self.stat = stat
        self.vers = vers
        self.arch = arch

class DebsStdoutLog(common.Log):

    def parse(self):
        self.logger.debug('parsing')

        self.pkgs = {}
        with open(self.path, 'r') as f:
            for line_number, line in enumerate(f.readlines()):
                # ignore header lines
                if line_number < 5: continue

                parts = line.split()
                (stat, name, vers, arch) = parts[0:4]
                self.pkgs[name] = Deb(stat, vers, arch)

    def record(self, flavor):
        self.logger.debug('recording %d packages',len(self.pkgs))
        flavor.record('debs', self.pkgs)
