import logging

class Common(object):
    def __init__(self, facts):
        self.facts = facts
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)

    def update_directives(self, name, handlers):
        '''Stub function, to be overridden by subclasses.'''
        self.logger.debug('not yet supported')

