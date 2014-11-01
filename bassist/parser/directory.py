import os

from . import host

class ParserDirectoryException(Exception):
    pass

class Directory(object):
    def __init__(self, path):
        self.path = path
        self.hosts = []

        for entry in os.listdir(self.path):
            full = os.path.join(self.path, entry)
            if not os.path.isdir(full):
                continue
            self.hosts.append(host.Host(full))
