# Copyright (c) 2016 Kurt Yoder
# See the file LICENSE for copying permission.
import time
import logging
logger = logging.getLogger(__name__)

from py2neo import Node, Relationship

from . import db

g = db.get_db()

class Snapshot(object):
    '''A system snapshot contains links to all sub-systems, e.g.
    packages, files, etc.'''

    def __init__(self, secondary_id=None):
        self.secondary_id = secondary_id
        self.timestamp = time.time()

        if self.secondary_id is not None:
            logger.debug('setting secondary id %s',self.secondary_id)
            n = g.graph.find_one('Snapshot', 'secondary_id', self.secondary_id)
            if n is None:
                n = Node('Snapshot', timestamp=self.timestamp,
                        secondary_id=self.secondary_id)

            self.n = n

        else:
            self.n = Node('Snapshot', timestamp=self.timestamp)

    def add(self, obj):
        '''Link a new object to this snapshot.'''
        o = obj.get_node()
        contains = Relationship(self.n, 'contains', o)
        g.graph.create(contains)

    def exists(self):
        '''Did this snapshot already run?'''
        n = g.graph.find_one('Snapshot', 'secondary_id', self.secondary_id)
        if n is None:
            return False
        else:
            return True
