# Copyright (c) 2015 Kurt Yoder
# See the file LICENSE for copying permission.
import os
import logging

import psycopg2

import ZODB
import BTrees.OOBTree
import transaction

from . import name
from . import obj


class FlavorDBException(Exception):
    pass


class DB(object):
    def __init__(self, path):
        # self.path = os.path.join(path, 'flavors.zodb')
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)
        self.db = ZODB.DB(self.path)
        self.connection = self.db.open()
        self.dbroot = self.connection.root()

        self.logger.debug('dbroot has: %s', self.dbroot)

        if not 'names' in self.dbroot:
            self.dbroot['names'] = BTrees.OOBTree.BTree()
            transaction.commit()

        if not 'uuids' in self.dbroot:
            self.dbroot['uuids'] = BTrees.OOBTree.BTree()
            transaction.commit()

    def close(self):
        self.connection.close()
        self.db.close()

    def get_id_from_name(self, flavor_name):
        '''Check if the flavor name has a flavor ID. If not, create it.
        Then return the flavor ID.'''
        self.logger.debug('flavor_name: %s', flavor_name)
        name_obj = name.get(self.dbroot['names'], flavor_name)
        return (name_obj.uuid)

    def get_flavor_from_id(self, flavor_id):
        '''Check if the flavor object referenced by the given ID exists. If
        not, create it. Then return the flavor object.'''
        self.logger.debug('flavor_id: %s', flavor_id)
        uuid_obj = obj.get(self.dbroot['uuids'], flavor_id)
        return (uuid_obj)

    def get_obj_from_name(self, flavor_name):
        '''Return a flavor object from a given name.'''
        uuid = self.get_id_from_name(flavor_name)
        self.logger.debug('uuid: %s', uuid)
        obj = self.get_flavor_from_id(uuid)
        return (obj)
