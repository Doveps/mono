import logging

class Set(object):
    '''A Set is all or part of Comparison object data, which is inferred to
    result from a change made to an OS. For example: installing a package.'''

    def __init__(self, comparison, db):
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)
        self.db = db

        encoded = hashlib.sha1(str(comparison))
        self.id = encoded.hexdigest()
        self.logger.debug('set hash: %s',self.id)

        if hexdigest in self.db.dbroot['diffs']:
            return

        self.db.dbroot['diffs'][hexdigest] = comparison
        self.db.commit()
