# Copyright (c) 2015 Kurt Yoder
# See the file LICENSE for copying permission.
import logging
logger = logging.getLogger(__name__)
import hashlib

from . import sets
from . import diffs

class Comparison(object):
    '''A Comparison is a collection of diffs, for example as generated and
    exported by the bassist.'''

    def __init__(self, db, id=None, diffs=None):
        '''Always provide either an id or diffs.'''

        self.db = db

        if id is None:
            assert diffs is not None
            self.id_from_diffs(diffs)

        if diffs is None:
            assert id is not None
            assert id in self.db.dbroot['comparisons']
            self.id = id

        self.diffs = self.db.dbroot['comparisons'][self.id]
        self.diffs_in_set = None
        self.set_ids = None

    def id_from_diffs(self, diffs):
        # generate a hash of the content so it can't get added twice
        encoded = hashlib.sha1(str(diffs))
        self.id = encoded.hexdigest()
        logger.debug('diff hash: %s',self.id)

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

    def get_set_ids(self):
        self.find_diffs_in_sets()
        return self.set_ids

    def find_diffs_in_sets(self):
        '''Find all sets that diffs are assigned to.'''

        if self.diffs_in_set is not None:
            assert self.set_ids is not None
            return

        self.diffs_in_set = {}
        self.set_ids = []

        for diff_id in self.get_diff_ids():
            diff_obj = diffs.Diff(diff_id)
            set_ids = sets.find_with_diff(diff_obj, self.db)

            self.diffs_in_set[diff_id] = set_ids

            for set_id in set_ids:
                if set_id in self.set_ids:
                    continue
                self.set_ids.append(set_id)

        logger.debug('my diffs are in sets: %s',self.set_ids)

    def diff_is_assigned(self, diff_id):
        '''Is a given diff assigned to a set?'''
        self.find_diffs_in_sets()
        assert diff_id in self.diffs_in_set
        if len(self.diffs_in_set[diff_id]) == 0:
            return False
        return True

    def all_unassigned(self):
        '''Are all diffs unassigned?'''
        self.find_diffs_in_sets()
        for diff_id in self.get_diff_ids():
            if self.diff_is_assigned(diff_id):
                return False
        return True

    def all_assigned(self):
        '''Are all diffs assigned?'''
        self.find_diffs_in_sets()
        for diff_id in self.get_diff_ids():
            if not self.diff_is_assigned(diff_id):
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
