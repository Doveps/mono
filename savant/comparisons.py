import logging
import hashlib

from . import sets

class Comparison(object):
    '''A Comparison is a collection of diffs, for example as generated and
    exported by the bassist.'''

    def __init__(self, bassist_diffs, db):
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)
        self.data = bassist_diffs
        self.db = db

        # generate a hash of the content so it can't get added twice
        encoded = hashlib.sha1(str(self.data))
        self.id = encoded.hexdigest()
        self.logger.debug('diff hash: %s',self.id)

        if self.id in self.db.dbroot['comparisons']:
            return

        self.db.dbroot['comparisons'][self.id] = self.data
        self.db.commit()

    def assigned(self):
        '''Did we find any assignments for this comparison?'''

        # TODO: replace this stub!
        return False

    def __repr__(self):
        return '<%s %s>'%(type(self).__name__, self.data)

    def __len__(self):
        total = 0
        for sys_name, system in self.data.items():
            total += len(system['subtract']) + len(system['add'])
        return total

def all(db):
    '''Return a list of all comparison ids.'''
    return(db.dbroot['comparisons'].keys())

def get(db, id):
    '''Get a comparison by its id.'''
    assert id in db.dbroot['comparisons']
    return(db.dbroot['comparisons'][id])
