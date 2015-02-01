import logging

from . import stripped
from ..inferences import db

class Sets(object):
    def __init__(self, diff, db_dir):
        self.diff = stripped.Stripped(diff)
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)
        self.db = db.DB(db_dir)

        self.logger.debug('diff %s', self.diff)

        self.db.add_diff(self.diff)
