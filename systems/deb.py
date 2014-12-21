from . import common

class Deb(object):
    def __init__(self, stat, vers, arch):
        self.stat = stat
        self.vers = vers
        self.arch = arch

class Debs(common.MergeableDict):
    pass
