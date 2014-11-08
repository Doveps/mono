import os
import logging

from . import log_file

class ParserHostException(Exception):
    pass

class Host(object):
    def __init__(self, path):
        self.path = path
        self.logger = logging.getLogger(__name__)
        self.parsers = []

        for entry in os.listdir(self.path):
            full = os.path.join(self.path, entry)
            self.logger.debug('examining: %s', full)

            if not os.path.isfile(full):
                continue
            self.logger.debug('it is a file')

            retrieved_file = log_file.get_from_name(full)
            if retrieved_file is None:
                continue

            self.logger.debug('appending parser')
            self.parsers.append(retrieved_file)
