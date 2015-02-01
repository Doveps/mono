from . import common

class Deb(common.NaiveRepr):
    def __init__(self, stat, vers, arch):
        self.stat = stat
        self.vers = vers
        self.arch = arch

class Package(common.NaiveRepr):
    def __init__(self):
        self.deb = None

    def add_deb(self, stat, vers, arch):
        self.deb = Deb(stat, vers, arch)

class Packages(common.MergeableDict):
    pass
