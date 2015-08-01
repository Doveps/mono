import logging
import os
import errno

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

        self.get_file_data()

    def get_file_data(self):
        self.file_data = {}

        # TODO: actually load files! for now we are just creating/overwriting
        if self.required_file is None:
            return

        self.file_data[self.required_file] = []

    def __repr__(self):
        return str(self.file_data)
