import os
import logging

from . import log_file
from . import json_file

class ParserHostException(Exception):
    pass

class Host(object):
    def __init__(self, path):
        self.path = path
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)
        self.parsers = []

        for entry in os.listdir(self.path):
            full = os.path.join(self.path, entry)
            self.logger.debug('examining: %s', full)

            if not os.path.isfile(full):
                continue
            self.logger.debug('it is a file')

            parser = self.find_parser(full)
            if parser is None:
                continue

            self.logger.debug('appending parser')
            self.parsers.append(parser)

    def find_parser(self, full_path):

        # log file?
        parser = log_file.get_parser(full_path)
        if parser is not None:
            self.logger.debug('retrieved log parser')
            return parser

        # json file?
        parser = json_file.get_parser(full_path)
        if parser is not None:
            self.logger.debug('retrieved json parser')
            return parser

        return None
