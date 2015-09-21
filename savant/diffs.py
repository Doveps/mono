import logging

class Diff(object):
    '''This is a simple object containing parts of a diff: action, system,
    name. Instantiate it by passing in a single string with all three parts,
    separated by a pipe.'''

    def __init__(self, id):
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)
        self.id = id

        self.logger.debug('received id: %s',self.id)

        # identify the action and system
        parts = self.id.split('|', 2)
        assert len(parts) == 3
        self.action = parts[0]
        self.system = parts[1]
        self.name = parts[2]

    def __repr__(self):
        return self.action+'|'+self.system+'|'+self.name
