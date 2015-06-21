import logging
import hashlib

from . import sets
from . import diffs

class Comparison(object):
    '''A Comparison is a collection of diffs, for example as generated and
    exported by the bassist.'''

    def __init__(self, db, id=None, diffs=None):
        '''Always provide either an id or diffs.'''

        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)
        self.db = db

        if id is None:
            assert diffs is not None
            self.id_from_diffs(diffs)

        if diffs is None:
            assert id is not None
            assert id in self.db.dbroot['comparisons']
            self.id = id

        self.diffs = self.db.dbroot['comparisons'][self.id]
        self.assignments = None

    def id_from_diffs(self, diffs):
        # generate a hash of the content so it can't get added twice
        encoded = hashlib.sha1(str(diffs))
        self.id = encoded.hexdigest()
        self.logger.debug('diff hash: %s',self.id)

        # because IDs are hashed from contents, no need to set again
        if self.id in self.db.dbroot['comparisons']:
            return

        self.db.dbroot['comparisons'][self.id] = diffs
        self.db.commit()

    def has_diff(self, diff):
        if diff.system not in self.diffs:
            return False
        if diff.action not in self.diffs[diff.system]:
            return False
        if diff.name not in self.diffs[diff.system][diff.action]:
            return False
        return True

    def get_diff_ids(self):
        '''Return all diff IDs that are in this comparison. These do *not*
        contain any of the details in the comparison db from bassist about each
        diff.'''

        ids = []
        for system_name, system_dict in self.diffs.items():
            for action_name, action_dict in system_dict.items():
                for name in action_dict.keys():
                    ids.append(action_name +'|'+ system_name +'|'+ name)
        return ids

    def get_systems(self):
        return self.diffs.keys()

    def get_sets(self):
        '''Did we find any sets assigned to this comparison?'''

        if self.assignments is not None:
            return

        self.assignments = {}

        for diff_id in self.get_diff_ids():
            diff_obj = diffs.Diff(diff_id)
            in_sets = sets.find_with_diff(diff_obj, self.db)
            if len(in_sets) == 0:
                self.assignments[diff_id] = None
            else:
                self.assignments[diff_id] = in_sets

    def all_unassigned(self):
        '''Are all diffs unassigned?'''
        self.get_sets()
        for diff_id in self.get_diff_ids():
            if self.assignments[diff_id] is not None:
                return False
        return True

    def all_assigned(self):
        '''Are all diffs assigned?'''
        self.get_sets()
        for diff_id in self.get_diff_ids():
            if self.assignments[diff_id] is None:
                return False
        return True

    def __repr__(self):
        return '<%s %s>'%(type(self).__name__, self.diffs)

    def __len__(self):
        total = 0
        for sys_name, system in self.diffs.items():
            total += len(system['subtract']) + len(system['add'])
        return total

def all(db):
    '''Return a list of all comparison ids.'''
    return(db.dbroot['comparisons'].keys())

def find_with_diff(diff, db):
    '''Find one or more ids of comparisons that contain a diff.'''
    results = []
    for comparison_id in all(db):
        comparison_obj = Comparison(db, comparison_id)
        if comparison_obj.has_diff(diff):
            results.append(comparison_id)

    return(results)
