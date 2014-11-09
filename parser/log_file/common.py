import logging

class ParserLogException(Exception):
    pass

class Log(object):
    def __init__(self, path):
        self.path = path
        self.logger = logging.getLogger(self.__module__)

    def get_line_count(self):
        self.line_count = None
        with open(self.path, 'r') as f:
            self.line_count = len(f.readlines())
        self.logger.debug('line count: %d', self.line_count)
