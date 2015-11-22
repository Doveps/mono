# Copyright (c) 2015 Kurt Yoder
# See the file LICENSE for copying permission.
import os
import logging

from . import db

class FlavorDirectoryException(Exception):
    pass

class Directory(object):
    def __init__(self, path):
        self.path = path
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)

        if not os.path.isdir(self.path):
            raise FlavorDirectoryException(
                    'Path %s is either not readable or not a directory'%self.path)

        # open all flavor objects
        self.db = db.DB(path)
