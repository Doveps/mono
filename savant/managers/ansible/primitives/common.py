import logging

class Common(object):
    def __init__(self, set, facts):
        self.set = set
        self.facts = facts
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)

    def update_data(self, data):
        '''Stub function, to be overridden by subclasses.'''
        pass

