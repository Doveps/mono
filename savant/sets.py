import logging

from . import diffs

class Set(object):
    '''A Set is all or part of Comparison object data, which is inferred to
    result from a change made to an OS. For example: installing a package.'''

    def __init__(self, db, id):
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)
        self.db = db
        self.id = id

        self.logger.debug('id is %s',self.id)
        self.info = diffs.Diff(self.id)

    def delete_diff(self, diff):
        # for some reeason, zodb doesn't like deletes from its arrays?!
        # so operate on a new array instead, and then copy it in place
        current = self.get_diffs()
        assert diff in current
        current.remove(diff)
        self.update_diffs(current)

    def update_diffs(self, data):
        self.db.dbroot['sets'][self.id] = data
        self.db.commit()

    def get_diffs(self):
        return self.db.dbroot['sets'][self.id]

    def delete(self):
        del self.db.dbroot['sets'][self.id]
        self.db.commit()

    def __len__(self):
        return len(self.db.dbroot['sets'][self.id])

def find(delta, db):
    '''Find one or more sets containing a delta.'''
    results = []
    for set_id, set_choices in db.dbroot['sets'].items():
        if delta in set_choices:
            results.append(set_id)

    return(results)

def all(db):
    '''Return a list of the set_ids of all sets.'''
    return(db.dbroot['sets'].keys())

def get(set_id, db):
    '''Return a single set.'''
    assert set_id in db.dbroot['sets']
    return(Set(db, set_id))

def delete(set_id, db):
    '''Delete a single set.'''
    assert set_id in db.dbroot['sets']
    Set(db, set_id).delete()
