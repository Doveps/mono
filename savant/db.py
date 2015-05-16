import os
import logging

import ZODB
import BTrees.OOBTree
import transaction

class DB(object):
    '''Encapsulate access to the inferences database.'''

    def __init__(self, path):
        self.path = os.path.join(path, 'inferences.zodb')
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)
        self.db = ZODB.DB(self.path)
        self.connection = self.db.open()
        self.dbroot = self.connection.root()

        self.logger.debug('dbroot has: %s',self.dbroot)

        for root in ['comparisons', 'sets', 'playbooks']:
            if not root in self.dbroot:
                self.dbroot[root] = BTrees.OOBTree.BTree()
                transaction.commit()

    # careful!
    # http://eli.thegreenplace.net/2009/06/12/safely-using-destructors-in-python
    # http://pydev.blogspot.com.br/2015/01/creating-safe-cyclic-reference.html
    def __del__(self):
        self.close()

    def close(self):
        self.connection.close()
        self.db.close()

    def commit(self):
        transaction.commit()
