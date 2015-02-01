import os
import logging
import hashlib

import ZODB
import BTrees.OOBTree
import transaction

class DB(object):
    def __init__(self, path):
        self.path = os.path.join(path, 'inferences.zodb')
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)
        self.db = ZODB.DB(self.path)
        self.connection = self.db.open()
        self.dbroot = self.connection.root()

        self.logger.debug('dbroot has: %s',self.dbroot)

        if not 'sets' in self.dbroot:
            self.dbroot['sets'] = BTrees.OOBTree.BTree()
            transaction.commit()

        if not 'diffs' in self.dbroot:
            self.dbroot['diffs'] = BTrees.OOBTree.BTree()
            transaction.commit()

    # careful!
    # http://eli.thegreenplace.net/2009/06/12/safely-using-destructors-in-python
    # http://pydev.blogspot.com.br/2015/01/creating-safe-cyclic-reference.html
    def __del__(self):
        self.close()

    def add_diff(self, diff):
        # generate a hash of the content so it can't get added twice
        encoded = hashlib.sha1(str(diff))
        hexdigest = encoded.hexdigest()
        self.logger.debug('diff hash: %s',hexdigest)
        if hexdigest in self.dbroot['diffs']:
            return
        self.dbroot['diffs'][hexdigest] = diff.data
        transaction.commit()

    def close(self):
        self.connection.close()
        self.db.close()
