from . import common

class DebsStdoutLog(common.Log):

    def parse(self):
        self.logger.debug('parsing')

        #with open(self.path, 'r') as f:
        #    self.lines = f.readlines()
