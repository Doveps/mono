# Copyright (c) 2015 Kurt Yoder
# See the file LICENSE for copying permission.
from . import common

class ProcessInstance(common.NaiveRepr):
    def __init__(self, fields):
        (self.pid, self.ppid, self.uid, self.gid, self.cgroup,
                self.flag, self.nice, self.priority,
                self.tty) = fields[0:9]

class Process(common.NaiveRepr):
    def __init__(self, command):
        self.command = command
        self.instances = []

    def add(self, fields):
        self.instances.append(ProcessInstance(fields))

class Processes(common.MergeableDict):
    pass
