# Copyright (c) 2016 Kurt Yoder
# See the file LICENSE for copying permission.

class DebPackage(object):
    def __init__(self, name):
        self.name = name

    def set_stat(self, stat):
        self.stat = stat

    def set_vers(self, vers):
        self.vers = vers

    def set_arch(self, arch):
        self.arch = arch
