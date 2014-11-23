import os
import logging

import ZODB
import BTrees.OOBTree
import transaction

from . import name

class FlavorDBException(Exception):
    pass

class DB(object):
    def __init__(self, path):
        self.path = os.path.join(path, 'flavors.zodb')
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)
        self.db = ZODB.DB(self.path)
        self.connection = self.db.open()
        self.dbroot = self.connection.root()

        self.logger.debug('dbroot has: %s',self.dbroot)

        if not 'names' in self.dbroot:
            self.dbroot['names'] = BTrees.OOBTree.BTree()
            transaction.commit()

        if not 'flavors' in self.dbroot:
            self.dbroot['flavors'] = BTrees.OOBTree.BTree()
            transaction.commit()

    def close(self):
        self.connection.close()
        self.db.close()

    def get_id_from_name(self, flavor_name):
        '''Check if the flavor name has a flavor ID. If not, create it.
        Then return the flavor ID.'''
        self.logger.debug('flavor_name: %s',flavor_name)
        name.get(self.dbroot['names'], flavor_name)
