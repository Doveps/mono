# Copyright (c) 2015 Kurt Yoder
# See the file LICENSE for copying permission.
import logging
import os
import errno

from .. import sets
from . import ansible

class ManagerException(Exception):
    pass

class Manager(object):
    '''A Manager takes as input one or more sets and a basic flavor name, and
    uses these to generate files in configuration management tool languages.

    For example: given set "add package Apache2" and flavor "Ubuntu-14.04",
    allow me to create Ansible files that perform this action.'''

    def __init__(self, db, set_ids, flavor):
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)
        self.db = db
        self.flavor = flavor
        self.sets = {}

        # Ansible, Chef, Puppet, Shell, etc
        self.writers = {}

        for set_id in set_ids:
            self.sets[set_id] = sets.Set(self.db, set_id)

    def make_dir(self, directory_path):
        self.logger.debug('Writing to %s',directory_path)
        try:
            os.makedirs(directory_path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    def write(self, directory_path, tool_name):
        '''Arguments: the directory to create the files in, and the name of the
        configuration management tool to use.

        For example: '/home/foo/output', and 'ansible'.'''

        self.make_dir(directory_path)

        # make a subdirectory for the configuration manager tool's output
        creation_path = os.path.join(directory_path, tool_name)
        self.make_dir(creation_path)

        try:
            tool_module = globals()[tool_name]
        except KeyError:
            raise ManagerException, 'Configuration management tool "%s" is not supported' %tool_name

        tool_class_name = tool_name.capitalize()
        ToolPointer = getattr(tool_module, tool_class_name)
        tool = ToolPointer(creation_path, self.flavor.metadata['facts'])

        for set_id, set_obj in self.sets.items():
            self.logger.debug('Translating set into %s: %s',tool_name,set_id)
            tool.translate_set(set_obj)

        tool.write()
        self.writers[tool_name] = tool

    def get_report(self):
        out_str = ''
        for tool_name, tool_obj in self.writers.items():
            out_str += 'Wrote %s\n'%tool_obj.descriptor
            out_str += tool_obj.get_report()
        return out_str
