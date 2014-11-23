import logging

import persistent

class ParserLogException(Exception):
    pass

class Log(persistent.Persistent):
    def __init__(self, path):
        self.path = path
        self.logger = logging.getLogger(self.__module__ + '.' + type(self).__name__)

    def get_line_count(self):
        self.line_count = None
        with open(self.path, 'r') as f:
            self.line_count = len(f.readlines())
        self.logger.debug('line count: %d', self.line_count)

    def parse(self):
        '''The default parse method does nothing. It should be
        overridden by a subclass method.'''
        self.logger.debug('skipping parse due to empty method')
        pass

    def __getstate__(self):
        """logger can not be pickled, so exclude it."""
        out_dict = self.__dict__.copy()
        del out_dict['logger']
        return(out_dict)

    def __setstate__(self, dict):
        """Restore logger which was excluded from pickling."""
        self.__dict__.update(dict)
        self.logger = logging.getLogger(self.__module__ + '.' + type(self).__name__)
