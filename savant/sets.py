import logging

class Set(object):
    '''A Set is all or part of Comparison object data, which is inferred to
    result from a change made to an OS. For example: installing a package.'''

    def __init__(self, db, id):
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)
        self.db = db
        self.id = id

        # identify the action and system
        parts = self.id.split('|', 2)
        assert len(parts) == 3
        self.action = parts[0]
        self.system = parts[1]
        self.name = parts[2]

        #self.logger.debug('set hash: %s',self.id)

    def add_data(self, data):
        self.db.dbroot['sets'][self.id] = data
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
