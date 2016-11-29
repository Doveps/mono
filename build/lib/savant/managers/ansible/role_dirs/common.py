# Copyright (c) 2015 Kurt Yoder
# See the file LICENSE for copying permission.
import logging
import os
import errno

import yaml

class Directory(object):
    '''This kind of object knows how to manipulate files from top-level Ansible
    role directories.'''

    def __init__(self, path):
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)

        # ...tasks_dir.Tasks => tasks
        my_dir = type(self).__name__.lower()
        self.path = os.path.join(path, my_dir)

        # ensure role directory exists
        try:
            os.makedirs(self.path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

        self.added = 0
        self.get_file_data()

    def get_file_data(self):
        self.file_data = {}

        # TODO: actually load files! for now we are just creating/overwriting
        if self.required_file is None:
            return

        self.file_data[self.required_file] = []

    def write(self):
        for file_name, file_data in self.file_data.items():
            full_path = os.path.join(self.path, file_name)
            with open(full_path, 'w') as fh:
                # add the yaml prefix
                fh.write('---\n')
                if len(file_data) == 0:
                    fh.write('# empty\n')
                    continue
                fh.write(
                        yaml.safe_dump( file_data, indent=2,
                            default_flow_style=False ))

    def get_report(self):
        '''This should be overridden by subclass, so return empty.'''
        return ''

    def __repr__(self):
        return str(self.file_data)
