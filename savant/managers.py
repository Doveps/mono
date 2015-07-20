import logging

from . import sets

class Manager(object):
    '''A Manager takes one or more sets as input, and turns them into
    configuration management files. For now we assume it will write Ansible
    code.'''

    def __init__(self, db, set_ids, flavor):
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)
        self.db = db
        self.flavor = flavor
        self.sets = {}

        for set_id in set_ids:
            self.sets[set_id] = sets.Set(self.db, set_id)

    def write(self, directory_path):
        self.logger.debug('Writing to %s',directory_path)
