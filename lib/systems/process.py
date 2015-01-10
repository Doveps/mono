from . import common

class ProcessInstance(object):
    def __init__(self, fields):
        (self.pid, self.ppid, self.uid, self.gid, self.cgroup,
                self.flag, self.nice, self.priority,
                self.tty) = fields[0:9]

class Process(object):
    def __init__(self, command):
        self.command = command
        self.instances = []

    def add(self, fields):
        self.instances.append(ProcessInstance(fields))

class Processes(common.MergeableDict):
    pass
