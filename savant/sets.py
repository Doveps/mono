import logging

from . import diffs

class Set(object):
    '''A Set is one or more diffs from a Comparison object. Diffs result from a
    change made to an OS. For example: installing a package.'''

    def __init__(self, db, id):
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)
        self.db = db
        self.id = id

        self.logger.debug('id is %s',self.id)
        self.info = diffs.Diff(self.id)

        if self.id in self.db.dbroot['sets']:
            self.diffs = self.db.dbroot['sets'][self.id]
        else:
            self.diffs = {}

    def commit(self):
        self.db.dbroot['sets'][self.id] = self.diffs
        self.db.commit()

    def add_diff(self, diff):
        if diff.system not in self.diffs:
            self.diffs[diff.system] = {}
        if diff.action not in self.diffs[diff.system]:
            self.diffs[diff.system][diff.action] = []
        if diff.name not in self.diffs[diff.system][diff.action]:
            self.diffs[diff.system][diff.action].append(diff.name)

    def update_diffs(self, diff_ids):
        for diff_id in diff_ids:
            diff = diffs.Diff(diff_id)
            self.add_diff(diff)

        self.commit()

    def delete_diff(self, diff):
        assert self.has_diff(diff)

        # ZODB doesn't like to replace in place, so copy and then update
        diffs = self.diffs

        diffs[diff.system][diff.action].remove(diff.name)
        if len(diffs[diff.system][diff.action]) == 0:
            del(diffs[diff.system][diff.action])
        if len(diffs[diff.system]) == 0:
            del(diffs[diff.system])

        self.diffs = diffs
        self.commit()

    def has_diff(self, diff):
        if diff.system not in self.diffs:
            return False
        if diff.action not in self.diffs[diff.system]:
            return False
        if diff.name not in self.diffs[diff.system][diff.action]:
            return False
        return True

    def get_diff_ids(self):
        ids = []
        for system_name, system_dict in self.diffs.items():
            for action_name, actions in system_dict.items():
                for name in actions:
                    ids.append(action_name +'|'+ system_name +'|'+ name)
        return ids

    def delete(self):
        assert self.id in self.db.dbroot['sets']
        del self.db.dbroot['sets'][self.id]
        self.db.commit()

    def __len__(self):
        length = 0
        for action in self.diffs.values():
            for system in action.values():
                length += len(system)
        return length

def all(db):
    '''Return a list of the set_ids of all sets.'''
    return(db.dbroot['sets'].keys())

def find_with_diff(diff, db):
    '''Find one or more set ids of sets that contain a diff.'''
    results = []
    for set_id in db.dbroot['sets'].keys():
        set_obj = Set(db, set_id)
        if set_obj.has_diff(diff):
            results.append(set_id)

    return(results)
