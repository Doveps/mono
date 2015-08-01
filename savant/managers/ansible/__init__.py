import logging
import os
import errno
import importlib

import yaml

from . import primitives

class Role(object):
    '''This object encapsulates all knowledge about how to build Ansible
    playbooks.'''
    # from http://docs.ansible.com/ansible/playbooks_best_practices.html
    top_dirs = ['tasks', 'handlers', 'templates', 'files', 'vars', 'defaults',
            'meta']

    def __init__(self, path, facts):
        self.path = path
        self.facts = facts
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)

        # The data object will contain all of the objects to be converted to yaml
        self.data = {}

        assert os.path.isdir(self.path)
        for dir_name in Role.top_dirs:
            self.create_dir(dir_name)
            self.load_dir(dir_name)

    def create_dir(self, dir_name):
        '''Create top-level directories.'''
        try:
            os.makedirs(os.path.join(self.path, dir_name))
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    def load_dir(self, dir_name):
        '''Load any existing yaml files into my internal data store.'''
        self.data[dir_name] = []

        # TODO: actually load them! for now we are just initiating empty structs

    def translate_set(self, set_obj):
        PrimitiveClass = primitives.get_class(set_obj.info.system)
        primitive = PrimitiveClass(set_obj, self.facts)
        primitive.update_data(self.data)
