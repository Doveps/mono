import logging

class System(object):
    '''Compare two systems data objects. It is valid to pass a
    mismatched data type, or None as the second data object. In this
    case, the types will evaluate as different.'''
    def __init__(self, data1, data2=None):
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)

        self.data1 = data1
        self.data2 = data2

        assert self.data1 is not None

        self.logger.debug('received data1: %s',data1)
        self.logger.debug('received data2: %s',data2)

        self.matches = {}

        if type(self.data1) is not type(self.data2):
            self.set_mismatch('type')
            return

        self.set_match('type')

        self.find_missing()

        self.logger.debug('different? %s', self.different())

    def different(self):
        for val in self.matches.values():
            if val is False:
                return True

        return False

    def set_mismatch(self, kind):
        self.matches[kind] = False

    def set_match(self, kind):
        self.matches[kind] = True

    def find_missing(self):
        self.only_in_data2 = {}
        for key, val in self.data2.items():
            if key not in self.data1:
                self.only_in_data2[key] = val
                self.set_mismatch('data2')
        if not self.only_in_data2:
            self.set_match('data2')
        self.logger.debug('only in data2: %s',
                sorted(self.only_in_data2.keys()))

        self.only_in_data1 = {}
        for key, val in self.data1.items():
            if key not in self.data2:
                self.only_in_data1[key] = val
                self.set_mismatch('data1')
        if not self.only_in_data1:
            self.set_match('data1')
        self.logger.debug('only in data1: %s',
                sorted(self.only_in_data1.keys()))

