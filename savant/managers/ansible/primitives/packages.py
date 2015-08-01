from . import common

class Packages(common.Common):
    def update_data(self, data):
        self.logger.debug(self.set.id)
        # first iteration: assume we should install the given package

