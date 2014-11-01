import os

from . import log_file

class ParserHostException(Exception):
    pass

class Host(object):
    def __init__(self, path):
        self.path = path
        self.parsers = []

        for entry in os.listdir(self.path):
            full = os.path.join(self.path, entry)
            if not os.path.isfile(full):
                continue

            retrieved_file = log_file.get_from_name(full)
            if retrieved_file is None:
                continue

            self.parsers.append(retrieved_file)
