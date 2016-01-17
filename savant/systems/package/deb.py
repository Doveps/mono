from py2neo import Node, Relationship

from ... import db

g = db.get_db()

class DebPackage(object):
    def __init__(self, name):
        self.name = name

    def set_stat(self, stat):
        self.stat = stat

    def set_vers(self, vers):
        self.vers = vers

    def set_arch(self, arch):
        self.arch = arch

    def add(self):
        n = Node('DebPackage', name=self.name)
        g.graph.create(n)
