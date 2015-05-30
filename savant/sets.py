import logging

class Set(object):
    '''A Set is all or part of Comparison object data, which is inferred to
    result from a change made to an OS. For example: installing a package.'''

    def __init__(self, db, id):
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)
        self.db = db
        self.id = id

        #self.logger.debug('set hash: %s',self.id)

    def add_data(self, data):
        self.db.dbroot['sets'][self.id] = data
        self.db.commit()

def find(delta, db):
    '''Find one or more sets containing a delta.'''
    results = []
    for set_id, set_choices in db.dbroot['sets'].items():
        if delta in set_choices:
            results.append(set_id)

    return(results)
