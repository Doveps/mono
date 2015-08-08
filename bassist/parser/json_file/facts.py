import logging
import json

class FactsJSON(object):
    keys = ['lsb', 'machine', 'os_family', 'pkg_mgr', 'system', 'userspace_bits']

    def __init__(self, path):
        self.path = path
        self.log = self.__module__.split('.')[-1]
        self.logger = logging.getLogger(self.__module__ + '.' + type(self).__name__)

        self.data = {}
        self.name = 'facts'

    def parse(self):
        self.logger.debug('parsing facts')

        with open(self.path, 'r') as f:
            data = json.load(f)

        for key in FactsJSON.keys:
            self.data[key] = data['ansible_'+key]

    def record(self, flavor):
        self.logger.debug('recording %d %s', len(self.data), self.name)
        flavor.record_metadata(self.name, self.data)

    def __repr__(self):
        return '%s: %d'%(self.__class__.__name__, len(self.data))
