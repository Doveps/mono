import logging
logger = logging.getLogger(__name__)
import urllib

from . import diffs

cache = {}

class Set(object):
    '''A Set is one or more diffs from a Comparison object. Diffs result from a
    change made to an OS. For example: installing a package.'''

    def __init__(self, db, id):
        self.db = db
        self.id = id

        logger.debug('id is %s',self.id)
        self.info = diffs.Diff(self.id)

        # system/action lookup dict, for quicker lookups than a list
        self.diff_lookups = {}

        if self.id in self.db.dbroot['sets']:
            self.diffs = self.db.dbroot['sets'][self.id]

            for system_name, actions in self.diffs.items():
                self.diff_lookups[system_name] = {}
                for action_name, names in actions.items():
                    self.diff_lookups[system_name][action_name] = {}
                    for name in names:
                        self.diff_lookups[system_name][action_name][name] = True
        else:
            self.diffs = {}

    def commit(self):
        self.db.dbroot['sets'][self.id] = self.diffs
        self.db.commit()

    def quote(self):
        '''Return URL-safe version of my id.'''
        return urllib.quote(self.id, '')

    def add_diff(self, diff):
        if diff.system not in self.diffs:
            self.diffs[diff.system] = {}
            self.diff_lookups[diff.system] = {}
        if diff.action not in self.diffs[diff.system]:
            self.diffs[diff.system][diff.action] = []
            self.diff_lookups[diff.system][diff.action] = {}
        if diff.name not in self.diffs[diff.system][diff.action]:
            self.diffs[diff.system][diff.action].append(diff.name)
            self.diff_lookups[diff.system][diff.action][diff.name] = True

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
        if diff.system not in self.diff_lookups:
            return False
        if diff.action not in self.diff_lookups[diff.system]:
            return False
        if diff.name not in self.diff_lookups[diff.system][diff.action]:
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
    for set_id in all(db):
        if not set_id in cache:
            cache[set_id] = Set(db, set_id)
        set_obj = cache[set_id]
        if set_obj.has_diff(diff):
            results.append(set_id)

    return(results)
