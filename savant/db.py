# Copyright (c) 2015, 2016 Kurt Yoder
# See the file LICENSE for copying permission.
import logging

import py2neo
import keyring

_db = None

class DBPassword(object):
    name = 'savant_db'
    user = 'neo4j'

    def format(self):
        '''Return the user and password in a format suitable for
        including into a Graph() setup string. If no password has been
        set, return empty.'''
        password = self.get()
	print password
	print DBPassword.user
        if password == '':
            return('')
        return('%s:%s@'%(DBPassword.user,password))

    def get(self):
        '''Get the password for the DB.'''
        return(keyring.get_password(DBPassword.name, DBPassword.user))

    def set(self, new_password):
        '''Set a password for the DB, creating or overwriting any
        existing value.'''
        keyring.set_password(DBPassword.name, DBPassword.user, new_password)

class DB(object):
    '''Access to the savant Graph DB will always happen via this
    object.'''

    def __init__(self):
        connection = 'http://'+DBPassword().format()+'localhost:7474/db/data/'
        self.graph = py2neo.Graph(connection)

# http://stackoverflow.com/questions/6829675
def get_db():
    '''Ensure the db connection is global and re-usable.'''
    global _db
    if not _db:
        _db = DB()
    return _db

__all__ = [ 'get_db' ]
