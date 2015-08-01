import logging

class Common(object):
    def __init__(self, set_obj, facts):
        self.set = set_obj
        self.facts = facts
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)

    def update_directives(self, data):
        '''Stub function, to be overridden by subclasses.'''
        pass

