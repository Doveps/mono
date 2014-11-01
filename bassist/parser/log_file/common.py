class ParserLogFileException(Exception):
    pass

class LogFile(object):
    def __init__(self, path):
        self.path = path
