# Copyright (c) 2015 Kurt Yoder
# See the file LICENSE for copying permission.
from . import common

class UpstartInit(common.NaiveRepr):
    def __init__(self, state):
        self.state = state

class Upstart(common.NaiveRepr):
    def __init__(self, wanted, state, pid):
        self.wanted = wanted
        self.state = state
        self.pid = pid

class Service(common.NaiveRepr):
    def __init__(self, name):
        self.name = name
        self.upstart = None
        self.upstart_init = None

    def add_upstart(self, wanted, state, pid):
        self.upstart = Upstart(wanted, state, pid)

    def add_upstart_init(self, state):
        self.upstart_init = UpstartInit(state)

    def merge(self, other):
        if other.upstart and not self.upstart:
            self.upstart = other.upstart
        if other.upstart_init and not self.upstart_init:
            self.upstart_init = other.upstart_init

class Services(common.MergeableDict):
    pass
