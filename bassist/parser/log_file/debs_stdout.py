# Copyright (c) 2015 Kurt Yoder
# See the file LICENSE for copying permission.
import savant.systems.package.deb as deb

from . import common

class DebsStdoutLog(common.Log):

    def parse(self, save):

        with open(self.path, 'r') as f:
            for line_number, line in enumerate(f.readlines()):
                # ignore header lines
                if line_number < 5: continue

                parts = line.split()

                assert len(parts) > 4
                (stat, name, vers, arch) = parts[0:4]

                d = deb.DebPackage(name)
                d.set_stat(stat)
                d.set_vers(vers)
                d.set_arch(arch)

                save(d)
