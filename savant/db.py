# Copyright (c) 2015, 2016 Kurt Yoder
# See the file LICENSE for copying permission.
import logging

from py2neo import Graph

_db = None

class DB(object):
    '''Access to the savant Graph DB will always happen via this
    object.'''

    def __init__(self):
        self.graph = Graph()

    def stuff(self):
        logging.warn('got here')

# http://stackoverflow.com/questions/6829675
def get_db():
    '''Ensure the db connection is global and re-usable.'''
    global _db
    if not _db:
        _db = DB()
    return _db

__all__ = [ 'get_db' ]
