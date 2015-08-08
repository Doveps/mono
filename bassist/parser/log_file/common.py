import logging
import time

class ParserLogException(Exception):
    pass

class Log(object):
    def __init__(self, path):
        self.path = path
        self.log = self.__module__.split('.')[-1]
        self.logger = logging.getLogger(self.__module__ + '.' + type(self).__name__)

        self.data = None
        self.name = None

    def parse(self):
        '''The default parse method does nothing. It should be
        overridden by a subclass method.'''
        self.logger.debug('skipping parse due to empty method')
        pass

    def record(self, flavor):
        '''The default record method assumes that both attributes "data"
        and "name" have been populated. "data" should contain a zodb
        persistent object, and "name" should contain the name of the
        database key in the zodb. It then invokes "record" on the
        flavor.'''

        assert self.name is not None
        assert self.data is not None

        self.logger.debug('recording %d %s',len(self.data),self.name)

        start_time = time.time()

        flavor.record_system(self.name, self.data)

        self.logger.debug('completed recording in %d seconds',
                time.time() - start_time)

    def diff(self, flavor):

        assert self.name is not None
        assert self.data is not None

        return flavor.diff_system(self.name, self.data)

    def __repr__(self):
        return '%s: %d'%(self.__class__.__name__, len(self.data))
