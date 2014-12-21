import logging

class ParserLogException(Exception):
    pass

class Log(object):
    def __init__(self, path):
        self.path = path
        self.log = self.__module__.split('.')[-1]
        self.logger = logging.getLogger(self.__module__ + '.' + type(self).__name__)

    def parse(self):
        '''The default parse method does nothing. It should be
        overridden by a subclass method.'''
        self.logger.debug('skipping parse due to empty method')
        pass

    def record(self, flavor):
        '''The default record method does nothing. It should be
        overridden by a subclass method.'''
        self.logger.debug('skipping record due to empty method')
        pass
