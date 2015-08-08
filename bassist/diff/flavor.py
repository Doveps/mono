import logging

from . import common
from . import system

class Flavor(common.Diff):
    '''Compare two flavors containing systems data objects. It is valid
    to pass a mismatched type, or None as the second flavor object. In
    this case, the flavors will evaluate as different.'''
    def __init__(self, flavor1, flavor2=None):
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)

        self.flavor1 = flavor1
        self.flavor2 = flavor2

        assert self.flavor1 is not None

        self.logger.debug('received flavor1: %s',flavor1)
        self.logger.debug('received flavor2: %s',flavor2)

        self.matches = {}

        if type(self.flavor1) is not type(self.flavor2):
            self.set_mismatch('type')
            return

        self.set_match('type')

        self.find_missing()
        self.compare_systems()

        self.logger.debug('different? %s', self.different())

    def compare_systems(self):
        self.system_diffs = {}
        for key, val in self.flavor1.systems.items():
            if key in self.only_in_flavor1: continue
            diff = system.System(val, self.flavor2.systems[key])
            if diff.different():
                self.system_diffs[key] = diff
                self.set_mismatch('systems')
        if not self.system_diffs:
            self.set_match('systems')
        self.logger.debug('system diffs: %s',
                sorted(self.system_diffs.keys()))

    def find_missing(self):
        self.only_in_flavor2 = {}
        for key, val in self.flavor2.systems.items():
            if key not in self.flavor1.systems:
                self.only_in_flavor2[key] = val
                self.set_mismatch('flavor2')
        if not self.only_in_flavor2:
            self.set_match('flavor2')
        self.logger.debug('only in flavor2: %s',
                sorted(self.only_in_flavor2.keys()))

        self.only_in_flavor1 = {}
        for key, val in self.flavor1.systems.items():
            if key not in self.flavor2.systems:
                self.only_in_flavor1[key] = val
                self.set_mismatch('flavor1')
        if not self.only_in_flavor1:
            self.set_match('flavor1')
        self.logger.debug('only in flavor1: %s',
                sorted(self.only_in_flavor1.keys()))

    def export(self):
        data = {}

        for sys_name, system in self.system_diffs.items():
            data[sys_name] = {'subtract': {}, 'add': {}}
            for diff_name, diff_obj in system.only_in_data1.items():
                data[sys_name]['subtract'][diff_name] = diff_obj
            for diff_name, diff_obj in system.only_in_data2.items():
                data[sys_name]['add'][diff_name] = diff_obj
        return data


