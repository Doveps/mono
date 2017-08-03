# Copyright (c) 2015 Kurt Yoder
# See the file LICENSE for copying permission.
from . import common
from ...systems import package
from results import store_debs

class DebsStdoutLog(common.Log):

    def parse(self):
        self.logger.debug('parsing')

        self.data = package.Packages()
        self.name = 'packages'

        with open(self.path, 'r') as f:
            for line_number, line in enumerate(f.readlines()):
                # ignore header lines
                if line_number < 5: continue

                parts = line.split()

                assert len(parts) > 4
                (stat, name, vers, arch) = parts[0:4]

                store_debs(parts[0], parts[1], parts[2], parts[3])

                assert name not in self.data
                self.data[name] = package.Package()
                self.data[name].add_deb(stat, vers, arch)

