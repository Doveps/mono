from . import common

class FilesStdoutLog(common.Log):

    def parse(self):
        self.logger.debug('parsing')
