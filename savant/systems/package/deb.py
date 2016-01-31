# Copyright (c) 2016 Kurt Yoder
# See the file LICENSE for copying permission.

import py2neo

from ... import db

g = db.get_db()

class DebPackage(object):
    try:
        g.graph.schema.create_uniqueness_constraint('DebPackage',
                'unique_id')
    except py2neo.GraphError as error:
        if error.__class__.__name__ == 'ConstraintViolationException':
            # if it already exists, that's ok
            pass
        else:
            raise

    def __init__(self, name):
        self.name = name
        self.stat = None
        self.vers = None
        self.arch = None

    def set_stat(self, stat):
        self.stat = stat

    def set_vers(self, vers):
        self.vers = vers

    def set_arch(self, arch):
        self.arch = arch

    def get_node(self):
        '''Create a graph node.'''
        assert self.stat is not None
        assert self.vers is not None
        assert self.arch is not None
        unique_id = [self.name, self.vers, self.stat, self.arch]
        label = self.__class__.__name__
        o = g.graph.find_one(label, property_key='unique_id',
                property_value=unique_id)
        if o is None:
            o = py2neo.Node(label, name = self.name, stat = self.stat,
                    vers = self.vers, arch = self.arch, unique_id =
                    unique_id )
        return o
