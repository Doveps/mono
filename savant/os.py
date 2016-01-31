# Copyright (c) 2016 Kurt Yoder
# See the file LICENSE for copying permission.

from py2neo import Node, Relationship

from . import db

g = db.get_db()

class OS(object):
    '''All systems link to an instance of an OS.'''

    def __init__(self, id):
        self.id = id
        self.n = Node('OS', id=self.id)

    def add(self, obj):
        '''Link a new object to this OS.'''
        o = obj.get_node()
        contains = Relationship(self.n, 'contains', o)
        g.graph.create(contains)
