# Copyright (c) 2015 Kurt Yoder
# See the file LICENSE for copying permission.
from . import common

class Group(common.NaiveRepr):
    def __init__(self, password, gid):
        self.password = password
        self.gid = gid
        self.users = None

    def add_users(self, users):
        self.users = users

class Groups(common.MergeableDict):
    pass
