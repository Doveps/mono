# Copyright (c) 2016 Kurt Yoder
# See the file LICENSE for copying permission.
import time
import logging
logger = logging.getLogger(__name__)

from flask_restful import Resource
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

class SnapshotsAPI(Resource):
    def get(self):
        return find_probable_os()

def find_without_os():
    '''Get all snapshots that don't have any OS assigned to them.'''
    rets = []
    query = """
        MATCH (SBase:Snapshot)
        WHERE NOT (:OS)-[:has_snapshot]->(SBase)
        RETURN SBase
    """
    for record in g.graph.cypher.execute(query):
        rets.append(record.SBase.properties)
    return rets

def find_probable_os():
    '''Compare all snapshots, and rank them by likelihood of being a base OS.'''
    rets = []
    query = """
        MATCH (SBase:Snapshot)
        MATCH (:Snapshot)-[:contains]->(SPrimePackage)
        WHERE NOT (SBase)-[:contains]->(SPrimePackage)
        RETURN SBase, count(distinct(SPrimePackage)) AS diff
        ORDER BY diff DESC
    """
    for record in g.graph.cypher.execute(query):
        rets.append(record.SBase.properties)
    return rets

def find_difference(timestamp1, timestamp2):
    '''Find the difference between two snapshots.'''
    rets = []
    query = """
        MATCH (SBase:Snapshot {timestamp:{time1}})
        MATCH (:Snapshot {timestamp:{time2}})-[PContains:contains]->(SPrimePackage)
        WHERE NOT (SBase)-[:contains]->(SPrimePackage)
        RETURN SPrimePackage
    """
    for record in g.graph.cypher.execute(query, time1=timestamp1, time2=timestamp2):
        rets.append(record.SPrimePackage.properties)
    return rets
