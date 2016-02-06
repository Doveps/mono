# Copyright (c) 2016 Kurt Yoder
# See the file LICENSE for copying permission.

from py2neo import Node, Relationship

from . import db

g = db.get_db()

class Snapshot(object):
    '''A system snapshot contains links to all sub-systems, e.g.
    packages, files, etc.'''

    def __init__(self, id):
        self.id = id
        self.n = Node('Snapshot', id=self.id)

    def add(self, obj):
        '''Link a new object to this snapshot.'''
        o = obj.get_node()
        contains = Relationship(self.n, 'contains', o)
        g.graph.create(contains)
